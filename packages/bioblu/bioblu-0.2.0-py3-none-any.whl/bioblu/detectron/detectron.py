#!/usr/bin/env python3

from copy import copy
import datetime
import json
import logging
import os
import shutil
import sys
import torch
from typing import List, Tuple, Union

import cv2
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import termcolor

from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import (
    build_detection_test_loader,
    build_detection_train_loader,
    dataset_mapper,
    MetadataCatalog,
    DatasetCatalog,
)
from detectron2.data import transforms as T
from detectron2.engine import DefaultPredictor, DefaultTrainer
from detectron2.evaluation import COCOEvaluator, DatasetEvaluators, DatasetEvaluator
from detectron2.evaluation import inference_on_dataset
from detectron2.structures import BoxMode
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import Visualizer

from bioblu.ds_manage import ds_convert, ds_annotations, bbox_conversions
from bioblu.main import IMG_FORMATS


class CustomTrainer(DefaultTrainer):
    """
    Customized child of the DefaultTrainer class so that it accepts customized DataMapper.
    Except from the below method it inherits all other functionalities of the DefaultTrainer class.
    """
    def __init__(self, cfg):
        DefaultTrainer.__init__(self, cfg)  # Init parent DefaultTrainer

    @classmethod
    def build_train_loader(cls, cfg, mapper=None):
        if mapper is None:
            return build_detection_train_loader(cfg)
        return build_detection_train_loader(cfg, mapper=mapper)  # This takes a custom DataMapper now


class EvalCounter(DatasetEvaluator):
    """Custom counter to return the number of detected instances, as described in
    https://detectron2.readthedocs.io/en/latest/tutorials/evaluation.html
    """
    def reset(self):
        self.count = 0

    def process(self, inputs, outputs):
        for output in outputs:
            self.count += len(output["instances"])

    def evaluate(self):
        # save self.count somewhere, or print it, or return it.
        return {"count": self.count}


class ImageInfoGetter(DatasetEvaluator):
    """
    !!!EXPERIMENTAL!!!\n
    Custom Evaluator that adds the image info to the evaluation results.
    https://detectron2.readthedocs.io/en/latest/tutorials/evaluation.html
    """
    def reset(self):
        self.images = []

    def process(self, inputs, outputs):
        for output in outputs:
            # add image and image id
            current_img = {"image_id": output.get("image_id"),
                           "file_path": output.get("file_path")}
            self.images.append(current_img)

    def evaluate(self):
        # save self.count somewhere, or print it, or return it.
        return {"Images": self.images}


def load_json(json_fpath: str) -> dict:
    """Returns json data as a dict."""
    with open(json_fpath, 'r') as f:
        data = json.load(f)
    logging.debug(f'Loaded json object (type): {type(data)}')
    return data


def parse_augs(brightness_minmax: Tuple[float, float] = None,
               flip_v: float = None, flip_h: float = None,
               rot_minmax: Tuple[Union[float, int], Union[float, int]] = None) -> List:
    """
    Takes the arguments for the augmentations and returns the detectron-readable augmentations list.
    Returns a list of augmentations, or (if no arguments are given) an empty list.
    :param brightness_minmax:
    :param flip_v:
    :param flip_h:
    :param rot_minmax:
    :return:
    """
    augs = []
    if brightness_minmax is not None:
        bmin, bmax = brightness_minmax
        augs.append(T.RandomBrightness(bmin, bmax))
    if flip_v is not None:
        augs.append(T.RandomFlip(prob=flip_v, horizontal=False, vertical=True))
    if flip_h is not None:
        augs.append(T.RandomFlip(prob=flip_h, horizontal=True, vertical=False))
    if rot_minmax is not None:
        augs.append(T.RandomRotation(list(rot_minmax)))
    return augs


def create_detectron_img_dict_list(detectron_json_fpath, bbox_format = BoxMode.XYWH_ABS) -> List[dict]:
    """
    Creates a list of dictionaries to be used in detectron's DatasetCatalog.
    :param detectron_json_fpath:
    :return:
    """
    json_data = load_json(detectron_json_fpath)
    images = json_data.get("images", [])
    logging.debug(f"Images: {images}")
    annotations = json_data.get("annotations", [])
    dict_list = []
    for img in images:
        current_img = {"file_name": img["file_name"],
                       "image_id": img["id"],
                       "width": img["width"],
                       "height": img["height"],
                       "annotations": []}
        for annotation in annotations:
            if annotation["image_id"] == current_img["image_id"]:
                current_img["annotations"].append({"segmentation": [],
                                                   "area": None,  # ToDo: Check if this might have to be box area.
                                                   "iscrowd": 0,
                                                   "category_id": annotation["category_id"],
                                                   "bbox_mode": bbox_format,
                                                   "bbox": annotation["bbox"]})
        dict_list.append(current_img)
    return dict_list


def visualize_detectron_prediction(prediction: dict, save_as=None, show_img=True, color_mode="RGB"):
    """
    Takes a detectron prediction output dict (for one image) and visualizes it.
    :param prediction: needs to have keys ["instances", "img_name", "img_fpath""]
    :param save_as:
    :param show_img:
    :return:
    """
    if show_img or save_as is not None:
        metadata = MetadataCatalog.get("placeholder_name")
        metadata.thing_classes = list(prediction["materials_dict"].values())
        img = cv2.imread(prediction["img_fpath"])
        if color_mode == "RGB":
            img = img[:, :, ::-1]
        img_name = prediction.get("img_name", default="Img. name not found")
        v = Visualizer(img, metadata, scale=1.2)
        out = v.draw_instance_predictions(prediction["instances"].to("cpu"))
        if save_as is not None:
            out_dir = os.path.split(save_as)[0]
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir)
            out.save(save_as)
        if show_img:
            cv2.namedWindow(img_name, cv2.WINDOW_NORMAL)
            cv2.imshow(img_name, out.get_image()[:, :, ::-1])
            cv2.waitKey(0)


def visualize_detectron_set(fpath_json: str, materials_dict: dict = None):
    fdir, fname_json = os.path.split(fpath_json)
    set_name = fname_json.rsplit('.')[0]
    ds_name = fdir.split(os.sep)[-2]

    if materials_dict is None:
        materials_dict = get_detectron_set_materials(fpath_json)

    cfg = get_cfg()
    DatasetCatalog.register(set_name, lambda: create_detectron_img_dict_list(fpath_json))
    metadata = MetadataCatalog.get("placeholder_name")
    metadata.set(thing_classes=list(materials_dict.values()))
    cfg.DATASETS.TRAIN = (set_name,)

    dataset_dict = create_detectron_img_dict_list(fpath_json)

    # Based on the colab notebook:
    for d in dataset_dict:
        cv2.destroyAllWindows()
        img = cv2.imread(d["file_name"])
        _, img_name = os.path.split(d["file_name"])
        visualizer = Visualizer(img, metadata=metadata, scale=0.5)
        out = visualizer.draw_dataset_dict(d)
        cv2.imshow(f"{ds_name}, {set_name}, {img_name}", out.get_image())
        cv2.waitKey(0)


def visualize_full_detectron_ds(fdir_ds_root, materials_dict=None):
    json_paths = ds_annotations.get_all_fpaths_by_extension(os.path.join(fdir_ds_root, "annotations"), (".json",))
    for fpath in json_paths:
        visualize_detectron_set(fpath)


def get_detectron_set_materials(fpath_json) -> dict:
    materials_dict = {}
    set_dict = ds_annotations.load_json(fpath_json)
    for annot in set_dict["annotations"]:
        id = annot["category_id"]
        category_name = ""
        for cat in set_dict["categories"]:
            if cat["id"] == id:
                category_name = cat["name"]
        if id not in materials_dict.keys():
            materials_dict[id] = category_name
        else:
            if materials_dict[id] != category_name:
                raise AssertionError(f"Mismatch between material category {id}: {category_name} vs {materials_dict[id]}")
            else:
                logging.info(f"Material '{id}: {category_name}' already added.")
    return materials_dict


def get_detectron_materials_from_all_sets(fdir_detectron_root):
    json_fpaths = ds_annotations.get_all_fpaths_by_extension(fdir_detectron_root, (".json",))
    material_dict = {}
    for fpath in json_fpaths:
        current_mats = get_detectron_set_materials(fpath)
        for k, v in current_mats.items():
            if k not in material_dict:
                material_dict[k] = v
            else:
                if not material_dict[k] == v:
                    raise AssertionError(f"Materials mismatch: {v} and {material_dict[k]} have the same id {k}")
    return material_dict


def unpack_2d_tensor(input_tensor: tf.Tensor) -> np.array:
    return np.array([row.detach().numpy() for row in input_tensor])


def serialize_instance(prediction_result: dict) -> dict:
    """Turns a prediction result created by detectron2 into a dict that can be saved as json."""
    # Detectron2 boxes are stored as (x1, y1, x2, y2) tensors.
    instances = prediction_result["instances"]
    prediction_dict = {"img_name": prediction_result.get("img_name"),
                       "img_fpath": prediction_result.get("img_fpath"),
                       "instances": {"pred_boxes": unpack_2d_tensor(instances.get("pred_boxes")).tolist(),
                                     "box_centers": instances.get("pred_boxes").get_centers().detach().numpy().tolist(),
                                     "scores": unpack_2d_tensor(instances.get("scores")).tolist(),
                                     "pred_classes": unpack_2d_tensor(instances.get("pred_classes")).tolist(),
                                     },
                       "cfg": prediction_result.get("cfg"),
                       }
    return prediction_dict


def run_training(yolo_ds_root_dir: str,
                 model_yaml: str,
                 output_dir: str,
                 materials_dict: dict = None,
                 json_train: str = None,
                 json_val: str = None,
                 iterations: int = None,
                 ds_cfg_savename: str = "ds_catalog_train.json",
                 ds_name_train: str = "instances_detectron_train",
                 ds_name_val: str = "instances_detectron_val",
                 img_size_minmax: Tuple[int, int] = None,
                 device: str = "cuda",
                 filter_out_empty_imgs: bool = False,
                 max_detections_per_img: int = 2000,
                 number_of_workers: int = None,  # 2
                 imgs_per_batch: int = None,  # 16
                 base_lr: float = None,
                 lr_decay: list = None,
                 roi_heads_batch_size_per_img: int = None,
                 roi_heads_iou_thresh: float = None,  # 0.5
                 roi_heads_nms_thresh: float = None,  # 0.7
                 roi_heads_score_thresh_train: float = None,  # 0.05
                 roi_heads_score_thresh_test: float = None,
                 rpn_nms_thresh: float = None,
                 rpn_batch_size_per_img: int = None,  # 256
                 retinanet_score_thresh_test: float = None,  # 0.05
                 retinanet_nms_thresh_test: float = None,  # 0.5
                 retinanet_iou_threshs: list = None,
                 augmentations: list = None,
                 color_mode: str = None,
                 **kwargs):
    """
    :param yolo_ds_root_dir:
    :param model_yaml: Must include parent dir, e.g. "COCO-Detection/faster_rcnn_R_101_C4_3x.yaml".
    :param output_dir:
    :param materials_dict:
    :param json_train: defaults to "{detectron_ds_target_dir}/"annotations/{ds_name_train}.json"
    :param json_val: defaults to "{detectron_ds_target_dir}/"annotations/{ds_name_val}.json"
    :param iterations:
    :param ds_cfg_savename:
    :param ds_name_train: defaults to instances_detectron_train
    :param ds_name_val: defaults to instances_detectron_val
    :param img_size_minmax:
    :param device: "cpu" or "cuda". Defaults to "cuda"
    :param filter_out_empty_imgs:
    :param max_detections_per_img:
    :param number_of_workers:
    :param imgs_per_batch:
    :param base_lr:
    :param lr_decay:
    :param roi_heads_batch_size_per_img:
    :param roi_heads_eval_thresh:
    :param roi_heads_iou_thresh:
    :param roi_heads_nms_thresh:
    :param roi_heads_score_thresh_train:
    :param roi_heads_score_thresh_test:
    :param rpn_nms_thresh:
    :param rpn_batch_size_per_img:
    :param retinanet_score_thresh_test:
    :param retinanet_nms_thresh_test:
    :param retinanet_iou_threshs:
    :param augmentations:
    :return:

    Model options (only for detection, other methods are not listed here):

    COCO-Detection/faster_rcnn_R_101_C4_3x.yaml
    COCO-Detection/faster_rcnn_R_101_DC5_3x.yaml
    COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml
    COCO-Detection/faster_rcnn_R_50_C4_1x.yaml
    COCO-Detection/faster_rcnn_R_50_C4_3x.yaml
    COCO-Detection/faster_rcnn_R_50_DC5_1x.yaml
    COCO-Detection/faster_rcnn_R_50_DC5_3x.yaml
    COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml
    COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml
    COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml
    COCO-Detection/fast_rcnn_R_50_FPN_1x.yaml
    COCO-Detection/fcos_R_50_FPN_1x.py
    COCO-Detection/retinanet_R_101_FPN_3x.yaml
    COCO-Detection/retinanet_R_50_FPN_1x.py
    COCO-Detection/retinanet_R_50_FPN_1x.yaml
    COCO-Detection/retinanet_R_50_FPN_3x.yaml
    COCO-Detection/rpn_R_50_C4_1x.yaml
    COCO-Detection/rpn_R_50_FPN_1x.yaml
    """

    if not os.path.isdir(yolo_ds_root_dir):
        raise FileNotFoundError(f"Yolo style root dir does not exist: {yolo_ds_root_dir}")

    detectron_ds_target_dir = os.path.join(yolo_ds_root_dir.rstrip("/") + "_detectron")

    # Assign default values where arguments are None
    if json_train is None:
        json_train = os.path.join(detectron_ds_target_dir, "annotations", ds_name_train + ".json")
    if json_val is None:
        json_val = os.path.join(detectron_ds_target_dir, "annotations", ds_name_val + ".json")
    if augmentations is None:
        augmentations = []
    if retinanet_iou_threshs is None:
        retinanet_iou_thresh = [0.4, 0.5]
    if materials_dict is None:
        materials_dict = {0: "trash"}
    if img_size_minmax is None:
        img_size_minmax = (1300, 1850)

    print("------------------------------------ TRAINING SETTINGS ----------------------------------------------------")
    print(f"Training on dataset {yolo_ds_root_dir}")
    print(f"Using model {model_yaml}")
    print(f"Running on device: {device}")
    print(f"Img. size (min, max): {img_size_minmax}")
    print("-----------------------------------------------------------------------------------------------------------")

    ds_convert.cvt_yolo_to_detectron(yolo_ds_root_dir)

    setup_logger()  # Detectron2 logger
    ds_convert.cvt_yolo_to_detectron(yolo_ds_root_dir, materials_dict=materials_dict)
    # Extract image dict lists from jsons
    logging.info("Img. dict lists extracted.")
    # Register classes
    classes = materials_dict
    logging.info("Classes registered.")

    cfg = get_cfg()

    # MODEL
    cfg.merge_from_file(model_zoo.get_config_file(model_yaml))
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(model_yaml)
    cfg.MODEL.DEVICE = device

    # Here and below: If arguments are provided, update cfg, otherwise leave that section untouched.
    if color_mode is not None:
        cfg.INPUT.FORMAT = color_mode

    # OUTPUT
    cfg.OUTPUT_DIR = output_dir

    # DATASETS
    DatasetCatalog.register(ds_name_train, lambda: create_detectron_img_dict_list(json_train))
    DatasetCatalog.register(ds_name_val, lambda: create_detectron_img_dict_list(json_val))
    MetadataCatalog.get(ds_name_train).set(thing_classes=list(classes.values()))
    MetadataCatalog.get(ds_name_val).set(thing_classes=list(classes.values()))
    cfg.DATASETS.TRAIN = (ds_name_train,)
    cfg.DATASETS.TEST = (ds_name_val,)
    if number_of_workers is not None:
        cfg.DATALOADER.NUM_WORKERS = number_of_workers
    cfg.DATALOADER.FILTER_EMPTY_ANNOTATIONS = filter_out_empty_imgs
    cfg.TEST.DETECTIONS_PER_IMAGE = max_detections_per_img  # set max detections per img
    cfg.INPUT.MIN_SIZE_TRAIN = (img_size_minmax[0],)  # minimum image size for the train set
    cfg.INPUT.MAX_SIZE_TRAIN = img_size_minmax[1]  # maximum image size for the train set
    cfg.INPUT.MIN_SIZE_TEST = img_size_minmax[0]  # minimum image size for the test set
    cfg.INPUT.MAX_SIZE_TEST = img_size_minmax[1]  # maximum image size for the test set

    # cfg.DATASETS.PROPOSAL_FILES_TRAIN =     # ToDo: Perhaps add the proposal files?

    # RPN
    if rpn_nms_thresh is not None:
        cfg.MODEL.RPN.NMS_THRESH = rpn_nms_thresh
    if rpn_batch_size_per_img is not None:
        cfg.MODEL.RPN.BATCH_SIZE_PER_IMAGE = rpn_batch_size_per_img

    # ROI_HEADS
    if roi_heads_batch_size_per_img is not None:
        cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = roi_heads_batch_size_per_img
    if roi_heads_nms_thresh is not None:
        cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = roi_heads_nms_thresh
    if roi_heads_iou_thresh is not None:
        cfg.MODEL.ROI_HEADS.IOU_THRESHOLDS = [roi_heads_iou_thresh]
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(materials_dict.keys()) # Number of classes, not num_classes+1!
    if roi_heads_score_thresh_train is not None:
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = roi_heads_score_thresh_train  # 0.5  # set threshold for this model

    # RETINANET
    cfg.MODEL.RETINANET.NUM_CLASSES = len(materials_dict.keys())
    if retinanet_score_thresh_test is not None:
        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = retinanet_score_thresh_test
    if retinanet_nms_thresh_test is not None:
        cfg.MODEL.RETINANET.NMS_THRESH_TEST = retinanet_nms_thresh_test
    if retinanet_iou_threshs is not None:
        cfg.MODEL.RETINANET.IOU_THRESHOLDS = retinanet_iou_threshs

    # SOLVER
    if imgs_per_batch is not None:
        cfg.SOLVER.IMS_PER_BATCH = imgs_per_batch
    if base_lr is not None:
        cfg.SOLVER.BASE_LR = base_lr
    if lr_decay is not None:
        cfg.SOLVER.STEPS = tuple(lr_decay)  # [] to not decay learning rate
    if iterations is not None:
        cfg.SOLVER.MAX_ITER = iterations

    logging.info("cfg set up completed.")

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    logging.info("Output dir created")

    # Save dataset catalog entries:
    ds_cat = DatasetCatalog.get(ds_name_train)
    savefile = os.path.join(cfg.OUTPUT_DIR, ds_cfg_savename)
    with open(savefile, "w") as f:
        json.dump(ds_cat, f, indent=4)
        logging.info(f"Dataset Catalog (training) saved as {savefile}")

    # save training config cfg to yaml
    cfg_save_path = os.path.join(cfg.OUTPUT_DIR, "cfg.yaml")
    cfg_save_string = cfg.dump()
    with open(cfg_save_path, "w") as f:
        f.write(cfg_save_string)
    print(f"Saved model/training cfg in {cfg_save_path}")

    logging.info(cfg)

    # Set up trainer
    if augmentations:
        print(f"Setting up CustomTrainer using a DatasetMapper that contains augmentations: {augmentations}")
        trainer = CustomTrainer(cfg)
        mapper_w_augs = dataset_mapper.DatasetMapper(cfg, augmentations=augmentations)
        trainer.build_train_loader(cfg, mapper_w_augs)
    else:
        print("No augmentations provided. Using default trainer.")
        trainer = DefaultTrainer(cfg)

    # Visualise augs
    # ToDo

    logging.debug("Done setting up trainer.")
    trainer.resume_or_load(resume=False)

    logging.debug("Starting training.")
    trainer.train()
    print("Done training. Proceeding to evaluation.")

    # ToDo: move evaluation into its own function.
    # Prep evaluation
    # pretrained_model = "/content/drive/MyDrive/colab_outputs/2022-04-30_1030/model_final.pth"
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")  # path to the model we just trained
    print(f"Evaluating model {os.path.join(cfg.OUTPUT_DIR, 'model_final.pth')}")
    if roi_heads_score_thresh_test is not None:
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = roi_heads_score_thresh_test  # set a custom testing threshold
    print(f"Using roi score threshold {cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST}")
    predictor = DefaultPredictor(cfg)

    # Evaluate
    evaluator = COCOEvaluator(ds_name_val,
                              tasks=("bbox",),
                              use_fast_impl=False,  # use a fast but unofficial implementation to compute AP
                              output_dir=output_dir)
    val_loader = build_detection_test_loader(cfg, ds_name_val)
    evaluation_results = inference_on_dataset(predictor.model, val_loader, evaluator)
    print(evaluation_results)

    # Save evaluation results
    eval_results_savepath = os.path.join(cfg.OUTPUT_DIR, "training_evaluation_results.txt")
    with open(eval_results_savepath, "w") as f:
        f.write(json.dumps(evaluation_results, indent=4))
    print("Done training and evaluating.")

    return evaluation_results


def evaluate_using_cfg():
    pass


def evaluate(fpath_model_dir: str, fpath_json_val: str, output_dir=None, materials_dict: dict = None,
             device: str = "cpu", filter_out_empty_imgs: bool = False, ds_name_val: str = "instances_detectron_val",
             color_mode="RGB", build_evaluator_from_trainer=False,
             roi_heads_score_thresh_test: float = None, roi_heads_iou_thresh: float = None,
             ):

    # ToDo: Write which dataset is used here!
    print(f"Evaluating against {fpath_json_val}")
    if materials_dict is None:
        materials_dict = {0: "trash"}

    # Output dir adjustments
    tstamp = format(datetime.datetime.now(), "%Y-%m-%d_%H%M")
    if output_dir is None:
        model_fdir, model_fname = os.path.split(fpath_model_dir)
        output_dir = os.path.join(model_fdir, f"evaluation_{tstamp}")
    if os.path.exists(output_dir):
        output_dir = output_dir.rstrip("/") + tstamp

    # Set up config  ToDo: Maybe turn this setup into its own function
    cfg = get_cfg()
    cfg.merge_from_file(os.path.join(fpath_model_dir, "cfg.yaml"))
    cfg.MODEL.WEIGHTS = os.path.join(fpath_model_dir, "model_final.pth")
    cfg.MODEL.DEVICE = device
    cfg.INPUT.FORMAT = color_mode
    cfg.OUTPUT_DIR = output_dir
    cfg.DATALOADER.FILTER_EMPTY_ANNOTATIONS = filter_out_empty_imgs

    DatasetCatalog.register(fpath_json_val, lambda: create_detectron_img_dict_list(fpath_json_val))
    MetadataCatalog.get(fpath_json_val).set(thing_classes=list(materials_dict.values()))
    cfg.DATASETS.TEST = (fpath_json_val,)

    if roi_heads_score_thresh_test is not None:
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = roi_heads_score_thresh_test
    if roi_heads_iou_thresh is not None:
        cfg.MODEL.ROI_HEADS.IOU_THRESHOLDS = [roi_heads_iou_thresh]

    cfg.OUTPUT_DIR = output_dir
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

    # copy evaluation json:
    shutil.copy(fpath_json_val, os.path.join(output_dir, "evaluation_set.json"))

    # Save dataset info (including wich image the image id corresponds to):
    catalog_dst = os.path.join(output_dir, "dataset_catalog.json")
    with open(catalog_dst, 'w') as f:
        f.write(json.dumps(DatasetCatalog.get(fpath_json_val), indent=4))

    if build_evaluator_from_trainer:
        trainer = DefaultTrainer(cfg)
        evaluator = trainer.build_evaluator()
    else:
        evaluator = COCOEvaluator(fpath_json_val,
                                  tasks=("bbox",),
                                  use_fast_impl=False,  # use a fast but unofficial implementation to compute AP
                                  output_dir=output_dir)
    predictor = DefaultPredictor(cfg)

    val_loader = build_detection_test_loader(cfg, fpath_json_val)

    # for idx in val_loader:
    #     print(idx)

    print(termcolor.colored("Evaluating ...", "green"))

    # evaluation_results = inference_on_dataset(predictor.model, val_loader, evaluator)
    evaluation_results = inference_on_dataset(predictor.model, val_loader, DatasetEvaluators([evaluator,
                                                                                              EvalCounter()]))
    evaluation_results["Evaluation set"] = fpath_json_val

    fpath_results_json = os.path.join(output_dir, "evaluation_metrics.json")
    with open(fpath_results_json, "w") as f:
        f.write(json.dumps(evaluation_results, indent=4))

    # # Add image info to predictions/inferences  # Thats not so straightforward, bc it's a  list of dicts.
    # fpath_coco_results = os.path.join(output_dir, "coco_instances_results.json")
    # coco_instances_results = load_json(fpath_coco_results)
    # img_info = load_json(fpath_json_val)
    # coco_instances_results["images"] = img_info["images"]
    # with open(fpath_coco_results, "w") as f:
    #     f.write(json.dumps(coco_instances_results, indent=4))

    print("Finished evaluation.")
    return evaluation_results


def visualize_predictions_and_ground_truth(fpath_eval_set, fpath_coco_predictions, materials_dict):
    eval_set = ds_annotations.load_json(fpath_eval_set)
    predictions = ds_annotations.load_json(fpath_coco_predictions)

    ground_truth_categories = set([annot["category_id"] for annot in eval_set["annotations"]])
    predicted_categories = set([pred["category_id"] for pred in predictions])
    logging.info(f"Categories in ground truth: {ground_truth_categories}")
    logging.info(f"Categories in predictions: {predicted_categories}")
    if not predicted_categories == ground_truth_categories == set(materials_dict.keys()):
        print(f"WARNING: Catergories in ground truths ({ground_truth_categories}), predictions ({predicted_categories}),"
              f" and materials dict ({set(materials_dict.keys())})")
    # TODO: Implement colours per class

    images = eval_set.get("images")
    annotations = eval_set.get("annotations")
    if images is None or annotations is None:
        raise LookupError("Could not extract images or annotations from evaluation_set json.")

    for image in images:
        img_id = image["id"]
        img_path = image["file_name"]
        img_dir, img_name = os.path.split(img_path)

        # img = cv2.imread(img_path)
        img = plt.imread(img_path)
        fig, ax = plt.subplots()
        ax.imshow(img)

        # Draw ground truths:
        ground_truths = 0
        for annotation in annotations:
            if annotation["image_id"] == img_id:
                bbox = annotation["bbox"]
                logging.debug(f"Bbox: {bbox}")
                rect_fill = patches.Rectangle(bbox[:2], bbox[2], bbox[3], facecolor=(188/255, 255/255, 20/255, 75/255),
                                              edgecolor=(188/255, 255/255, 20/255, 1))  # Rectangle(xy, width, height)
                ax.add_patch(copy(rect_fill))
                ground_truths += 1

        # Draw predictions:
        inferences = 0
        for pred in predictions:
            if pred["image_id"] == img_id:
                bbox = pred["bbox"]
                confidence = pred["score"]
                material_id = pred["category_id"]
                x, y = bbox[:2]
                plt.text(x, y, f"{confidence:.4f}  {materials_dict[material_id]}", color="white", backgroundcolor=(0.01, 0.01, 0.01, 0.1))
                pred_rect = patches.Rectangle(bbox[:2], bbox[2], bbox[3], color='red', fill=None)
                ax.add_patch(copy(pred_rect))
                inferences += 1

        print_text = f'{img_name}  |  Img. ID: {img_id}  |  GT: {ground_truths} | PRED: {inferences} | Eval: {fpath_eval_set}'
        plt.text(0, -30, print_text)
        fig.canvas.manager.full_screen_toggle()
        plt.show()


def get_TP(eval_json, inferences_json, iou_thresh: float = 0.5, pred_conf_thresh = None):
    """

    :param eval_json: json of the set that the validation has been run on (could be validation test, or eventually your test set)
    :param inferences_json: output from the evaluation run. Default name: coco_prediction_results.json
    :param iou_thresh: IoU(prediction, ground_truth) >= iou_thresh = TP
    :param pred_conf_thresh:
    :return: avg_tp_rate, TP_per_img, GT_per_img, TP_prop
    """
    print("Calculating true positive rate...")
    eval_dict = ds_annotations.load_json(eval_json)
    images = eval_dict["images"]
    all_ground_truths = eval_dict["annotations"]
    all_predictions = ds_annotations.load_json(inferences_json)

    TP_per_img = []
    GT_per_img = []
    TP_prop = []

    # Go over each img
    for image in images:
        # print(f"Analysing img {image['file_name']}")
        img_tp = 0
        img_gt = 0
        img_ground_truths = [gt for gt in all_ground_truths if gt["image_id"] == image["id"]]
        img_predictions = [p for p in all_predictions if p['image_id'] == image["id"]]

        # Filter out low-confidence predictions
        if pred_conf_thresh is not None:
            img_predictions = [p for p in img_predictions if p["score"] >= pred_conf_thresh]

        # Go over each GT box
        for gt in img_ground_truths:
            # print(f"Evaluating ground truth {gt['bbox']}")
            # x, x, w, h to x0, y0, x1, y1:
            gt_bbox = ds_annotations.cvt_xywh_box_to_dict(gt["bbox"])
            # Go over each prediction
            for pred in img_predictions:
                # x, x, w, h to x0, y0, x1, y1:
                pred_bbox = ds_annotations.cvt_xywh_box_to_dict(pred["bbox"])
                iou = ds_annotations.get_iou(gt_bbox, pred_bbox)
                # Check if the overlap is above the threshold
                if iou >= iou_thresh:
                    img_tp += 1
            img_gt += 1
        TP_per_img.append(img_tp)
        GT_per_img.append(img_gt)
        if img_gt > 0:
            TP_prop.append(img_tp / img_gt)

    avg_tp_rate = np.mean(np.array(TP_prop))

    return avg_tp_rate, TP_per_img, GT_per_img, TP_prop


def get_FP(eval_json: str, inferences_json: str, iou_thresh: float = 0.5, pred_conf_thresh = None):
    """
    This is not based on the the common FP = FP / (FP + TN) formula.
    Instead, what is calculated is the proportion of the prediction that were false positives (i.e. with no GT box
    underneath with an IoU >= threshold.
    :param eval_json: File to evaluate against (i.e. ground truths)
    :param inferences_json: inferences from those images.
    :param iou_thresh: Every inference that does not have IoU w/ ground truth >= than this threshold: False positive.
    :return: (avg_FP_rate, FP_abs per img, FP_rate per img)
    """
    print("Calculating false positive rate...")
    eval_dict = ds_annotations.load_json(eval_json)
    images = eval_dict["images"]
    all_ground_truths = eval_dict["annotations"]
    all_predictions = ds_annotations.load_json(inferences_json)

    FP_per_img = []
    preds_per_img = []
    FP_ratios = []

    # Go over each image
    for image in images:
        img_id = image["id"]
        img_ground_truths = [g for g in all_ground_truths if g["id"] == img_id]

        img_predictions = [p for p in all_predictions if p["image_id"] == img_id]
        # Filter out low confidence predictions
        if pred_conf_thresh is not None:
            img_predictions = [p for p in img_predictions if p["score"] >= pred_conf_thresh]

        inferences_per_img = len(img_predictions)

        # Go over all predictions in that img:
        FP_current_img = 0
        for pred in img_predictions:
            assert pred["image_id"] == img_id
            pred_bbox_dict = ds_annotations.cvt_xywh_box_to_dict(pred["bbox"""])
            overlaps_with_a_gt = False
            for gt in img_ground_truths:
                gt_bbox_dict = ds_annotations.cvt_xywh_box_to_dict(gt["bbox"])
                iou = ds_annotations.get_iou(pred_bbox_dict, gt_bbox_dict)
                if iou >= iou_thresh:
                    overlaps_with_a_gt = True
            if not overlaps_with_a_gt:
                FP_current_img += 1

        logging.debug(f"Inferences: {inferences_per_img}, FP: {FP_current_img}")


        FP_per_img.append(FP_current_img)
        preds_per_img.append(inferences_per_img)
        if inferences_per_img > 0:
            FP_ratios.append(FP_current_img / inferences_per_img)

    avg_fp = np.mean(np.array(FP_ratios))

    return avg_fp, FP_per_img, FP_ratios


def get_FN():
    pass


def get_predictions_per_gt():
    # return {"img": str, "obj_i": int, predictions_n: int}
    pass


def plot_rates(eval_json, pred_json, iou_thresh=0.5, pred_conf_thresh=None):
    avg_TP, TP_per_img, GT_per_img, TP_ratio_per_img = get_TP(eval_json, eval_json, iou_thresh, pred_conf_thresh)
    avg_FP, FP_per_img, FP_ratio_per_img = get_FP(eval_json, pred_json, iou_thresh, pred_conf_thresh)

    print(len(TP_per_img))
    print(len(GT_per_img))
    print(len(FP_per_img))
    print(len(FP_per_img))



if __name__ == "__main__":
    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    # logging.disable()


    # model_fdir = "/media/findux/DATA/Documents/Malta_II/results/5763_2022-05-26_183938/"
    # json_val = "/home/findux/Desktop/yolo_test_dir_detectron/annotations/instances_detectron_val.json"
    # print(load_json(json_val)["images"])

    # evaluate(model_fdir, json_val, materials_dict={0: "trash"}, roi_heads_iou_thresh=0.6)

    # fpath_eval = "/media/findux/DATA/Documents/Malta_II/results/5763_2022-05-26_183938/evaluation/instances_predictions.pth"
    # load_predictions(fpath_eval)

    # inst_pred_json = "/media/findux/DATA/Documents/Malta_II/results/5763_2022-05-26_183938/evaluation/coco_instances_results.json"
    # ds_annotations.make_json_readable(inst_pred_json)

    # inst_preds = "/media/findux/DATA/Documents/Malta_II/results/5763_2022-05-26_183938/evaluation/instances_predictions.pth"
    # extract_predictions(inst_preds)

    # Evaluate
    # model_fdir = "/media/findux/DATA/Documents/Malta_II/results/5644_2022-05-21_204705/"
    # json_val = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_06_detectron/annotations/instances_detectron_val.json"
    # evaluate(model_fdir, json_val, materials_dict={0: "trash"}, color_mode="RGB",)

    # # Visualize eval
    # eval_set = "/media/findux/DATA/Documents/Malta_II/results/5763_2022-05-26_183938/evaluation_2022-06-08_1657/evaluation_set.json"
    # coco_res = "/media/findux/DATA/Documents/Malta_II/results/5763_2022-05-26_183938/evaluation_2022-06-08_1657/coco_instances_results.json"
    # eval_set = "/media/findux/DATA/Documents/Malta_II/results/5644_2022-05-21_204705/evaluation_2022-06-09_1215/evaluation_set.json"
    # coco_res = "/media/findux/DATA/Documents/Malta_II/results/5644_2022-05-21_204705/evaluation_2022-06-09_1215/coco_instances_results.json"
    # visualize_predictions_and_ground_truth(eval_set, coco_res, {0: "trash"})

    # TP/FP rate
    # eval_json = "/media/findux/DATA/Documents/Malta_II/results/5644_2022-05-21_204705/evaluation_2022-06-09_1215/evaluation_set.json"
    # predictions = "/media/findux/DATA/Documents/Malta_II/results/5644_2022-05-21_204705/evaluation_2022-06-09_1215/coco_instances_results.json"
    # print(get_TP(eval_json=eval_json, inferences_json=predictions)[0])
    # print(get_FP(eval_json=eval_json, inferences_json=predictions))

    # fdir_ds05 = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_05_mini_gnejna_detectron/"
    # print(get_all_detectron_materials(fdir_ds05))
    # plot_rates(eval_json, predictions)

    # model_dir = "/media/findux/DATA/Documents/Malta_II/results/5239_2022-05-07_052041/"
    # eval_json = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_01_paradise_bay_detectron/annotations/instances_detectron_test.json"
    # visualize_detectron_set(eval_json, materials_dict={0: "trash"})

    # visualize_full_detectron_ds("/media/findux/DATA/Documents/Malta_II/datasets/dataset_08_detectron/")
    # evaluate(model_dir, eval_json, materials_dict={0: "trash"}, color_mode="RGB")


    # Evaluate the test test set:
    test_set_json = "/media/findux/DATA/Documents/Malta_II/datasets/tp_fp_fn_tests_yolo_detectron/annotations/instances_detectron_test.json"
    model_to_evaluate = "/media/findux/DATA/Documents/Malta_II/results/5763_2022-05-26_183938/"
    evaluate(model_to_evaluate, test_set_json, materials_dict={0: "trash"})