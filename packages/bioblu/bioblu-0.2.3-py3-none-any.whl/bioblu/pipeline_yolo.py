#!/usr/bin/env

import cv2
import logging
import os
import pandas as pd
from typing import List, Union

from bioblu.ds_manage import img_cutting
from bioblu.ds_manage import ds_annotations
from bioblu.ds_manage import geoprocessing
from bioblu.main import YOLO_IMG_FORMATS
from bioblu.yolo import yolo_tools


# def create_output_dir(output_dir, overwrite=False):
#     tiles_dir: str = ""
#     if os.path.isdir(output_dir):
#         if len(os.listdir(output_dir)) > 0 and not overwrite:
#             raise FileExistsError(f"[ ERROR ] Output dir exists and is not empty (pass overwrite=True to main): {output_dir}")
#     else:
#         tiles_dir: str = os.path.join(output_dir, "image_tiles")
#         os.makedirs(tiles_dir)
#     return tiles_dir


def get_yolo_reqs_path(yolo_dir, file_name = "requirements.txt") -> str:
    found_paths: list = []
    for root, dirs, files in os.walk(yolo_dir):
        if file_name in files:
            path_to_file: str = os.path.join(root, file_name)
            found_paths.append(path_to_file)
    if len(found_paths) > 1:
        raise FileExistsError(f"There are multiple {file_name} files: {found_paths}")
    if found_paths:
        return found_paths[0]
    return ""


def install_requirements(fpath_reqs, quiet=False):
    install_command: str = f"python3 -m pip install -r {fpath_reqs}"
    if quiet:
        install_command += " -q"
    os.system(install_command)


def install_yolo_requirements(yolo_fdir, install_quietly=False):
    print("Installing yolo requirements...")
    reqs_path: str = get_yolo_reqs_path(yolo_fdir)
    install_requirements(reqs_path, quiet=install_quietly)
    print("Done installing yolo requirements.")


def get_paths_to_annotations(fpath_target_dir) -> List[str]:
    annotations_dir: str = os.path.join(fpath_target_dir, "predictions", "labels")
    annotation_fpaths: List[str] = [os.path.join(annotations_dir, fpath) for fpath in sorted(os.listdir(annotations_dir))
                                    if fpath.lower().endswith("txt")]
    return annotation_fpaths


def get_paths_to_images(fpath_tiles_dir) -> List[str]:
    img_fpaths: List[str] = [os.path.join(fpath_tiles_dir, fname) for fname in sorted(os.listdir(fpath_tiles_dir))
                            if fname.lower().endswith(YOLO_IMG_FORMATS)]
    return img_fpaths


def files_have_same_basename(fpath_1, fpath_2) -> bool:
    print(f"Original paths to compare: {fpath_1}, {fpath_2}")
    # Remove path
    file_1 = os.path.split(fpath_1)[-1]
    file_2 = os.path.split(fpath_2)[-1]
    # Remove extension
    file_1 = os.path.splitext(file_1)[0]
    file_2 = os.path.splitext(file_2)[0]
    logging.debug(f"Checking base names: {file_1} against {file_2}")
    return file_1 == file_2


# def filenames_correspond(fpaths_a: List[str], fpaths_b: List[str]):
#     assert len(fpaths_a) == len(fpaths_b)
#     for path_a, path_b in zip(fpaths_a, fpaths_b):
#         if not files_have_same_basename(path_a, path_b):
#             return False
#     return True


def geolocate_yolo_predictions_on_img(fpath_img: str, fpath_annotations: str, class_names: List[str],
                                      altitude_m, sensor_width, focal_length_r, gsd_cm=None):

    # Make sure image and annotation file correspond:
    if not files_have_same_basename(fpath_img, fpath_annotations):
        print(f"Basenames do not correspond: {fpath_img}, {fpath_annotations}")
    img_height, img_width, _ = cv2.imread(fpath_img).shape

    if gsd_cm is None:
        gsd_cm = geoprocessing.get_gsd(altitude_m, focal_length_real_mm=focal_length_r,
                                       sensor_width_mm=sensor_width, img_width=img_width)

    materials_dict = {i: name for i, name in enumerate(class_names)}
    materials_dict = {0: "trash"}
    annotation_boxes = ds_annotations.load_yolo_annotations_as_BBoxes(fpath_annotations_txt=fpath_annotations,
                                                                      img_fpath=fpath_img,
                                                                      materials_dict=materials_dict)
    predictions = []
    for bbox in annotation_boxes:
        current_prediction = {}
        box_lat_lon = geoprocessing.geolocate_point_on_img(pixel_xy=bbox.box_center_xy, fpath_img=fpath_img,
                                                           altitude_m=altitude, focal_length_mm=focal_length_r,
                                                           sensor_width_mm=sensor_width, gsd_cm=gsd_cm)
        current_prediction = {"image_name": fpath_img,
                              "box_center_xy": bbox.box_center_xy,
                              "box_width_cm": bbox.box_dims_wh[0] * gsd_cm,
                              "box_height_cm": bbox.box_dims_wh[1] * gsd_cm,
                              "box_latitude_deg": box_lat_lon[0],
                              "box_longitude_deg": box_lat_lon[1],
                              "material": bbox.material,
                              "confidence": bbox.confidence}
        predictions.append(current_prediction)

    return predictions


def main(fdir_src_images, focal_length, altitude, sensor_width, fpath_yolo_weights, fdir_yolov5, fdir_output,
         overwrite=False, tiles_per_row=3, tiles_per_col=2, install_reqs_quietly=False,
         use_orig_img_size=True, save_prediction_images=True, conf_threshold=0.6, iou_threshold=0.6, save_csv=True,
         cut_tiles=True):

    # ToDo: implement every n'th image!

    print("Starting yolo pipeline")
    assert os.path.isdir(fdir_src_images)
    assert os.path.isdir(fdir_yolov5)

    install_yolo_requirements(fdir_yolov5, install_reqs_quietly)

    # Create target directories
    os.makedirs(fdir_output, exist_ok=overwrite)
    prediction_img_sources = fdir_src_images

    # Cutting images to tiles
    gsd_dict = {}
    if cut_tiles:
        prediction_img_sources = os.path.join(fdir_output, "image_tiles")
        os.makedirs(prediction_img_sources, exist_ok=overwrite)
        fdir_imgs, gsd_dict = img_cutting.new_tile_cutter(fdir_src_images, nrows=tiles_per_col, ncols=tiles_per_row,
                                                          altitude_m=altitude, target_dir=prediction_img_sources,
                                                          focal_length_mm=focal_length, sensor_width_mm=sensor_width,
                                                          save_csv=True, keep_file_type=True, inject_gps_exif=True,
                                                          inject_uav_yaw=True)
    # Predict on the created tiles:
    fpath_yolo_detect = os.path.join(fdir_yolov5, "detect.py")
    # Create the detection command
    inference_command = f"python3 {fpath_yolo_detect} --weights {fpath_yolo_weights} --source {prediction_img_sources} " \
                        f"--name predictions --save-txt --save-conf --conf-thres {conf_threshold} " \
                        f" --iou-thres {iou_threshold}"

    if use_orig_img_size:
        largest_img_dim: Union[int, float] = img_cutting.get_larges_img_dim(prediction_img_sources)
        inference_command += f" --img-size {largest_img_dim}"
    if not save_prediction_images:
        inference_command += " --nosave"
    if fdir_output:
        inference_command += f" --project {fdir_output}"
    if overwrite:
        inference_command += " --exist-ok"

    print("Running predictions...")
    # Execute the prediction command
    os.system(inference_command)
    # Note: Not every image gets an annotation file. Only images with detections produce an output, so there will be
    # fewer annotation files than images.

    fdir_annotations = os.path.join(fdir_output, "predictions", "labels")
    logging.info(f"Prediction labels dir: {fdir_annotations}")
    # sys.path.insert(0, yolo_dir)
    class_names: list = yolo_tools.get_class_names_from_weights_file(fpath_yolo_weights, fdir_yolov5)
    # class_names = ["trash"]
    img_fpaths = [os.path.join(prediction_img_sources, fpath) for fpath in sorted(os.listdir(prediction_img_sources))
                  if fpath.lower().endswith(YOLO_IMG_FORMATS)]
    txt_fpaths = [os.path.join(fdir_annotations, fpath) for fpath in sorted(os.listdir(fdir_annotations))
                  if fpath.lower().endswith("txt")]
    logging.debug(f"Number of img paths: {len(img_fpaths)} | Number of annot. paths: {len(txt_fpaths)}")
    assert len(txt_fpaths) <= len(img_fpaths)

    # Go over the predictions and geolocate them.
    predictions = []
    logging.info(f"Prediction img sources: {prediction_img_sources}")
    for annotations_fpath in txt_fpaths:
        img = ds_annotations.get_corresponding_file(annotations_fpath, prediction_img_sources)
        gsd_cm = None
        if gsd_dict:
            for img_path, gsd in zip(*tuple(gsd_dict.values())):
                if img_path == img:
                    gsd_cm = gsd

        img_predictions = geolocate_yolo_predictions_on_img(img, annotations_fpath, class_names, altitude_m=altitude,
                                                            sensor_width=sensor_width, focal_length_r=focal_length,
                                                            gsd_cm=gsd_cm)
        predictions.extend(img_predictions)

    predictions_df = pd.DataFrame(predictions)
    if save_csv:
        predictions_df.to_csv(os.path.join(fdir_output, "prediction_results.csv"))
    return predictions_df


if __name__ == "__main__":
    loglevel = logging.DEBUG
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    # logging.disable()

    # ToDo: use argparse

    focal_length = 8.6
    sensor_width = 12.8333
    altitude = 7
    yolo_weights = "/media/findux/DATA/Documents/Malta_II/results/4535_2022-04-10_021001/train/exp/weights/best.pt"
    yolo_fdir = "/media/findux/DATA/Documents/Malta_II/yolov5/"
    img_dir = "/media/findux/DATA/Documents/Malta_II/2022-06-21_catania_update/test_images/images_yolo/images/test/"
    target_dir = "/media/findux/DATA/Documents/Malta_II/2022-06-21_catania_update/yolo_results"

    main(img_dir, focal_length, altitude, sensor_width, yolo_weights, yolo_fdir, target_dir, overwrite=True,
         install_reqs_quietly=True, save_prediction_images=True, conf_threshold=0.25, iou_threshold=0.45, cut_tiles=False)
