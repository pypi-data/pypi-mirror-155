#!/usr/bin/env

import os

import bioblu


def get_yolo_reqs_path(yolo_dir, file_name = "requirements.txt") -> str:
    found_paths = []
    for root, dirs, files in os.walk(yolo_dir):
        if file_name in files:
            path_to_file = os.path.join(root, file_name)
            found_paths.append(path_to_file)
    if len(found_paths) > 1:
        raise FileExistsError(f"There are multiple {file_name} files: {found_paths}")
    if found_paths:
        return found_paths[0]
    return ""


def install_requirements(fpath_reqs, quiet=False):
    install_command = f"python3 -m pip install -r {fpath_reqs}"
    if quiet:
        install_command += " -q"
    os.system(install_command)


def prepare_directories(image_dir, output_dir=None, overwrite=False):

    tiles_dir = ""
    if output_dir is not None:
        if os.path.isdir(output_dir):
            if len(os.listdir(output_dir)) > 0 and not overwrite:
                raise FileExistsError(f"[ ERROR ] Output dir exists and is not empty. Pass overwrite=True. {output_dir}")
        else:
            tiles_dir = os.path.join(output_dir, "image_tiles")
            os.makedirs(tiles_dir)
    return tiles_dir


def install_yolo_requirements(yolo_fdir, install_quietly=False):
    print("Installing yolo requirements...")
    reqs_path = get_yolo_reqs_path(yolo_fdir)
    install_requirements(reqs_path, quiet=install_quietly)
    print("Done installing yolo requirements.")


def main(image_dir, focal_length, altitude, sensor_width, yolo_weights, yolo_dir, output_dir=None,
         overwrite_output_dir=False, tiles_per_row=3, tiles_per_col=2, install_reqs_quietly=False,
         use_orig_img_size=True):

    print("Starting yolo pipeline")
    assert os.path.isdir(image_dir)
    assert os.path.isdir(yolo_dir)

    install_yolo_requirements(yolo_dir, install_reqs_quietly)

    tiles_dir = prepare_directories(image_dir, output_dir, overwrite=overwrite_output_dir)

    # Cutting images to tiles

    # tiles_dir = new_tile_cutter(image_dir, nrows=tiles_per_col, ncols=tiles_per_row, altitude_m=altitude,
    #                             target_dir=tiles_dir, focal_length_mm=focal_length, sensor_width_mm=sensor_width,
    #                             save_csv=True, keep_file_type=True, inject_gps_exif=True, inject_uav_yaw=True)



    # Predict on the created tiles:
    fpath_yolo_detect = os.path.join(yolo_dir, "detect.py")
    inference_command = f"python3 {fpath_yolo_detect} --weights {yolo_weights} --source {tiles_dir}"
    if use_orig_img_size:
        largest_img_dim = bioblu
        inference_command += " --size "


if __name__ == "__main__":

    # ToDo: use argparse

    img_dir = "/media/findux/DATA/Documents/Malta_II/tests/pipeline/"
    focal_length = 8.6
    sensor_width = 12.8333
    altitude = 7
    yolo_weights = "/media/findux/DATA/Documents/Malta_II/results/4535*/train/exp/weights/best.pt"
    yolo_fdir = "/media/findux/DATA/Documents/Malta_II/yolov5/"
    target_dir = "/home/findux/Desktop/pipeline_test"

    # main(img_dir, focal_length, altitude, sensor_width, yolo_weights
    yolo_reqs = get_yolo_reqs_path(yolo_fdir)