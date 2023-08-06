#!/usr/bin/env python3

import copy
import math

import PIL.Image
import cv2
import gc
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import piexif
from PIL import Image
from PIL import UnidentifiedImageError
from piexif import InvalidImageDataError
import re
import sys
import termcolor
from typing import Tuple, List, Union

from bioblu.main import IMG_FORMATS, YOLO_IMG_FORMATS
from bioblu.ds_manage import geoprocessing, ds_annotations

# ToDo: 1.) General: Add place and date to tile names.
#       2.) Tile class: Add annotations attribute, as well as a create_yolo_annotation_file method


def get_larges_img_dim(fdir):
    largest_dim = 0
    img_paths = ds_annotations.get_all_fpaths_by_extension(fdir, YOLO_IMG_FORMATS)
    for fpath in img_paths:
        width, height, _ = cv2.imread(fpath).shape
        if max(width, height) > largest_dim:
            largest_dim = max(width, height)
    return largest_dim


#
# class Tile(object):
#     def __init__(self, array: np.array,
#                  timestamp: datetime,
#                  location: str,
#                  tile_position_yx: Tuple[int, int],
#                  tile_center_abs_yx: Tuple[int, int],
#                  tile_name: str,
#                  total_tiles_yx: Tuple[int, int],
#                  dims_orig_img_yx: Tuple[int, int],
#                  orig_center: Tuple[int, int],
#                  fpath_orig_img: str,
#                  gsd_cm: float,
#                  fpath_tile: str,
#                  dims_tile_yx: Tuple[int, int] = None,
#                  orig_img_coords_lat_lon: Tuple = (None, None),
#                  yaw_angle_deg: float = None,
#                  tile_coords_lat_lon: Tuple = (None, None),
#                  use_gps=True):
#         """
#
#         :param array:
#         :param timestamp:
#         :param location:
#         :param tile_position_yx:
#         :param tile_center_abs_yx:
#         :param tile_name:
#         :param total_tiles_yx:
#         :param dims_tile_yx:
#         :param dims_orig_img_yx:
#         :param orig_center:
#         :param orig_img_coords_lat_lon:
#         :param fpath_orig_img:
#         :param gsd_cm:
#         :param fpath_tile:
#         :param yaw_angle_deg: If this is not provided, the drone yaw will be extracted from the original image.
#         :param tile_coords_lat_lon:
#         """
#         # self.array = array
#         self.array = None
#         if array is not None:
#             self.array = array
#         self.timestamp = timestamp
#         self.tile_position_yx = tile_position_yx
#         self.tile_name = tile_name
#         self.location = location
#         self.fpath_tile = fpath_tile
#         self.total_tiles_yx = total_tiles_yx
#         self.gsd_cm = gsd_cm
#         self.dims_tile_yx = dims_tile_yx
#         self.tile_center_abs_yx = tile_center_abs_yx
#         self.fpath_orig_img = fpath_orig_img
#         self.fname_orig_img = os.path.split(self.fpath_orig_img)[-1]
#         self.dims_orig_img_yx = dims_orig_img_yx
#         self.orig_center = orig_center
#         self.latitude_orig_img = orig_img_coords_lat_lon[0]
#         self.longitude_orig_img = orig_img_coords_lat_lon[1]
#         self.offset_yx = calculate_offset_yx(self.tile_center_abs_yx, self.orig_center)
#         self.latitude_tile = None
#         self.longitude_tile = None
#         self.yaw_angle_deg = yaw_angle_deg
#         if self.yaw_angle_deg is None:
#             self.yaw_angle_deg = geoprocessing.get_uav_yaw(self.fpath_orig_img)
#         if tile_coords_lat_lon is None \
#                 and use_gps \
#                 and self.yaw_angle_deg is not None \
#                 and self.longitude_orig_img is not None:
#             _orig_coords = np.array((self.latitude_orig_img, self.longitude_orig_img)).flatten()
#             _shift_lat_lon = geoprocessing.calc_real_world_latlong_shift_from_px_shift(self.offset_yx, self.gsd_cm,
#                                                                                        self.yaw_angle_deg)
#             _shift_lat_lon = np.array(_shift_lat_lon).flatten()
#             _tile_coords = _orig_coords + _shift_lat_lon
#             _tile_coords = _tile_coords.flatten()
#             self.latitude_tile, self.longitude_tile = tuple(_tile_coords)
#
#             logging.info(f"Orig. img coords: {_orig_coords}")
#             logging.info(f"Tile orig. offset (px): {self.offset_yx}")
#             logging.info(f"Tile: {self.tile_name} lat/lon shift: {_shift_lat_lon}")
#             logging.info(f"Tile coords lat lon: {_tile_coords}")
#         else:
#             self.latitude_tile, self.longitude_tile = tile_coords_lat_lon
#         logging.info(f"Tile {self.tile_name} offset: {self.offset_yx}")
#
#     def show(self):
#         print(type(self.array))
#         cv2.imshow(self.tile_name, self.array)
#         cv2.waitKey()
#         # img = Image.fromarray(self.array)
#         # plt.imshow(img)
#         # plt.text(0, -15, "IMG: " + self.fname_orig_img + "  |  Tile: " + self.tile_name)
#         # plt.show()
#
#     def as_dict(self, exclude_array=True):
#         tile_dict = copy.copy(self.__dict__)
#         if exclude_array:
#             tile_dict["array"] = "Not stored. Pass exclude_array=False to keep array values."
#         return tile_dict
#
#     def __repr__(self):
#         return f"tile_name = {self.tile_name}\n" \
#                f"timestamp = {self.timestamp}\n" \
#                f"tile_position_yx = {self.tile_position_yx}\n" \
#                f"latitude_tile = {self.latitude_tile}\n" \
#                f"longitude_tile = {self.longitude_tile}\n" \
#                f"latitude_orig_img = {self.latitude_orig_img}\n" \
#                f"longitude_orig_img = {self.longitude_orig_img}\n" \
#                f"dims_tile_yx = {self.dims_tile_yx}\n" \
#                f"tile_center = {self.tile_center_abs_yx}\n" \
#                f"total_tiles_yx = {self.total_tiles_yx}\n" \
#                f"dims_orig_img_yx = {self.dims_orig_img_yx}\n" \
#                f"orig_center = {self.orig_center}\n" \
#                f"fpath_orig_img = {self.fpath_orig_img}\n" \
#                f"gsd_cm = {self.gsd_cm}\n" \
#                f"fpath_tile = {self.fpath_tile}\n" \
#                f"Tile({self.array}"
#
#     def save_to_file(self, use_gps=True):
#         img = None  # Failed attempt to solve the memory leak.
#         if self.array is not None:
#             try:
#                 exif_dict = piexif.load(self.fpath_orig_img)
#             except InvalidImageDataError:
#                 print(f"piexif could not get exif data because not TIFF or JPEG: {self.fpath_orig_img}")
#                 # img = Image.fromarray(self.array)
#                 # img.save(fp=self.fpath_tile)
#                 cv2.imwrite(self.fpath_tile, self.array)
#             else:
#                 if use_gps \
#                         and self.latitude_tile is not None\
#                         and self.longitude_tile is not None\
#                         and self.latitude_orig_img is not None:
#                     # Create exif data of tile coordinates
#                     img = Image.fromarray(self.array)
#                     tile_lat = geoprocessing.dd_to_dms(self.latitude_tile)
#                     tile_lon = geoprocessing.dd_to_dms(self.longitude_tile)
#                     tile_lat_exif = (tile_lat[0], 1), (tile_lat[1], 1), (int(tile_lat[2] * 10000), 10000)
#                     tile_lon_exif = (tile_lon[0], 1), (tile_lon[1], 1), (int(tile_lon[2] * 10000), 10000)
#                     exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = tile_lat_exif
#                     exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = tile_lon_exif
#                     exif_bytes = piexif.dump(exif_dict)
#                     img.save(self.fpath_tile, exif=exif_bytes)
#                 else:
#                     cv2.imwrite(self.fpath_tile, self.array)
#         else:
#             print(f"Tile not saved (no array): {self.tile_name}")
#
#     def clear_array(self):
#         self.array = None
#
#
# class TileSet(List):
#     def __init__(self, tiles: List[Tile] = None):
#         list.__init__()
#         if tiles is None:
#             tiles = []
#         self.tiles = tiles
#
#     def to_df(self):
#         pass  # ToDo: Do this!
#
#     def __iter__(self):
#         for elem in self.tiles:
#             yield elem
#
#     def append(self, tile: Tile):
#         self.insert(len(self.tiles), tile)
#
#
# def show_global_vars():
#     for k, v in globals().items():
#         print(f"{k.ljust(20)} {v}")

#
# def calculate_center(dimensions_yx: Tuple[int, int]) -> Tuple[int, int]:
#     """
#     Returns the center pixels (y, x)
#     :param dimensions_yx:
#     :return: tuple
#     """
#     return int(0.5 * dimensions_yx[0]), int(0.5 * dimensions_yx[1])


def calculate_offset_yx(tile_center_yx: Tuple[int, int], img_center_yx: Tuple[int, int]):
    """
    Calculates the pixel offset of a tile_position_yx center from the original image center.
    :param tile_center_yx:
    :param img_center_yx:
    :return: np.array
    """
    y_offset = tile_center_yx[0] - img_center_yx[0]
    x_offset = tile_center_yx[1] - img_center_yx[1]
    logging.info(f"y_offset, x_offset: {y_offset, x_offset}")
    return y_offset, x_offset

#
# def cut_img(fpath_img, tile_target_dir, altitude_m, location: str = None,
#             horizontal_tiles=3, vertical_tiles=2,
#             tile_extension=".tif", use_gps=True) -> List[Tile]:
#     """
#     Cuts image into tiles and returns a list of Tile objects. Note that this does not save the tiles to a file.
#     :param fpath_img:
#     :param tile_target_dir:
#     :param horizontal_tiles:
#     :param vertical_tiles:
#     :param altitude_m:
#     :param location: Place of recording
#     :param show_overview:
#     :param show_single_tiles:
#     :param tile_extension: File type to be used when storing the image tile. (e.g. ".tif"
#     :return:
#     """
#     if location is None:
#         location = "no_location_specified"
#
#     img_name = os.path.split(fpath_img)[-1]
#     tiles = []
#     try:
#         img = cv2.imread(fpath_img)
#         # with Image.open(fpath_img) as imfile:
#         #     img = copy.copy(imfile)
#         #     imfile.close()
#     except (UnidentifiedImageError, IsADirectoryError):
#         print(f"Could not open file '{img_name}' as an image.")
#         # imfile.close()
#         return None
#     else:
#         original_coordinates_lat_long = (None, None)
#         if use_gps:
#             original_coordinates_lat_long, coords_found = geoprocessing.get_coordinates_from_img(fpath_img)
#         img_array = np.array(img)
#         timestamp = get_creation_timestamp(Image.open(fpath_img))
#         height, width, channels = img_array.shape
#         logging.info(f"Orig img. dims: {height, width}")
#         img_center = calculate_center((height, width))
#         logging.info(f"Img. center: {img_center}")
#         gsd = geoprocessing.calc_gsd(altitude_m)
#         logging.info(f"GSD: {gsd}")
#         for y_tile in range(vertical_tiles):
#             for x_tile in range(horizontal_tiles):
#                 logging.info(f"Working on tile {y_tile}-{x_tile}".ljust(120, "-").upper())
#                 tile_width = int(width / horizontal_tiles)
#                 tile_height = int(height / vertical_tiles)
#                 logging.info(f"Tile: height, width: {tile_height, tile_width}")
#                 xmin = tile_width * x_tile
#                 xmax = tile_width * (x_tile + 1)
#                 ymin = tile_height * y_tile
#                 ymax = tile_height * (y_tile + 1)
#                 tile = img_array[ymin:ymax+1, xmin:xmax+1, :]
#                 tile_center_yx = (int(ymin + 0.5 * tile_height),
#                                   int(xmin + 0.5 * tile_width))
#                 logging.info(f"Tile center: {tile_center_yx}")
#                 tile_position = str(y_tile) + "-" + str(x_tile)
#                 tile_name = img_name.split(".")[0] + "_" + tile_position  # + tile_extension More versatile w/o ext.
#                 tile_fpath = os.path.join(tile_target_dir, location + '_' + tile_name + tile_extension)
#                 current_tile = Tile(array=tile, timestamp=timestamp, location=location,
#                                     tile_position_yx=(y_tile, x_tile), tile_center_abs_yx=tile_center_yx,
#                                     tile_name=location + '_' + tile_name,
#                                     total_tiles_yx=(vertical_tiles, horizontal_tiles),
#                                     dims_tile_yx=(ymax - ymin, xmax - xmin), dims_orig_img_yx=(height, width),
#                                     orig_center=img_center, orig_img_coords_lat_lon=original_coordinates_lat_long,
#                                     fpath_orig_img=fpath_img, gsd_cm=gsd,
#                                     fpath_tile=tile_fpath, use_gps=use_gps)
#                 tiles.append(current_tile)
#     return tiles
#
#
# def create_tiles(img_dir: str, horizontal_tile_count, vertical_tile_count, altitude_m, location: str = None,
#                  extension=".tif", save_tiles_csv=True, save_tiles_images=True, target_dir=None,
#                  use_gps=True, **kwargs) -> None:
#     """
#     Takes an image folder and cuts every image in it accordingly. Tiles are either saved in a tiles_YYYY_MM_DD subfolder,
#     or in a specified location.
#     NOTE: This can cause the machine to run out of memory when too many images are in the folder. In this case, create
#     multiple folders with fewer images and run the script on each folder separately.
#     :param img_dir:
#     :param horizontal_tile_count:
#     :param vertical_tile_count:
#     :param altitude_m:
#     :param location: Location name
#     :param extension:
#     :param save_tiles_csv:
#     :param save_tiles_images:
#     :param target_dir:
#     :param use_gps:
#     :return:
#     """
#     img_list = sorted(os.listdir(img_dir))
#     print(img_list)
#     img_list = [fname for fname in img_list if not os.path.isdir(os.path.join(img_dir, fname))]
#     img_list = [fname for fname in img_list if fname.lower().endswith(IMG_FORMATS)]
#     current_date = format(datetime.now(), "%Y-%m-%d")
#     if target_dir is None:
#         target_dir = os.path.join(img_dir, location + '_tiles_' + current_date)
#     if not os.path.isdir(target_dir):
#         os.mkdir(target_dir)
#     for i, img_fname in enumerate(img_list):
#         current_tiles = []
#         print(f"Cutting img {i + 1}/{len(img_list)}: {img_fname}")
#         fpath_img = os.path.join(img_dir, img_fname)
#         current_tiles = cut_img(fpath_img, target_dir, altitude_m, location,
#                                 horizontal_tiles=horizontal_tile_count, vertical_tiles=vertical_tile_count,
#                                 tile_extension=extension, use_gps=use_gps)
#         logging.debug([t.tile_name for t in current_tiles])
#         if current_tiles is not None:
#             fpath_df = os.path.join(target_dir, "tiles.csv")
#             if save_tiles_images:
#                 for j, tile in enumerate(current_tiles):
#                     tile.save_to_file(use_gps=use_gps)
#                     tile.clear_array()
#             if save_tiles_csv:
#                 if os.path.exists(fpath_df):
#                     tiles_df = pd.read_csv(fpath_df)
#                 else:
#                     tiles_df = pd.DataFrame(columns=current_tiles[0].as_dict().keys())
#                 current_tiles_df = tile_list_to_df(current_tiles)
#                 tiles_df = pd.concat([tiles_df, current_tiles_df], ignore_index=True)
#                 tiles_df.to_csv(fpath_df, index=False)
#                 tiles_df = []
#         if i % 25 == 0:
#             termcolor.cprint("NOTE: Read create_tiles() docstring regarding memory leak!", "red")
#
#         # Trying to fix memory leak:
#         del current_tiles
#         current_tiles, current_tiles_df, tiles_df = [], [], []
#         gc.collect()
#
#         logging.debug(f"Number of tracked objects: {len(gc.get_objects())}")
#         #
#         # print(sys.getsizeof(img_list))
#         # print(sys.getsizeof(tiles_df))
#         # print(sys.getsizeof(current_tiles))
#         # print(sys.getsizeof(current_tiles_df))
#
#
# def get_creation_timestamp(img: Image) -> datetime:
#     try:
#         _tstamp = img.getexif()[306]
#     except KeyError:
#         print("Could not extract creation timestamp.")
#         _tstamp = None
#     else:
#         logging.debug(_tstamp)
#         _regex_tstamp = re.compile(r'(\d\d\d\d\:\d\d\:\d\d) (\d\d\:\d\d\:\d\d)')
#         _matches = _regex_tstamp.search(_tstamp)
#         logging.debug(_matches)
#         _year, _month, _day = [int(val) for val in _matches.group(1).split(":")]
#         _hh, _mm, _ss = [int(val) for val in _matches.group(2).split(":")]
#         _tstamp = datetime(_year, _month, _day, _hh, _mm, _ss)
#     return _tstamp
#
#
# def tile_list_to_df(tile_list: List[Tile], exclude_array=True) -> pd.DataFrame:
#     tiles_df = None  # Attempt to fix memory leak
#     tiles_df = pd.DataFrame(columns=tile_list[0].as_dict().keys())
#     for tile in tile_list:
#         tiles_df = tiles_df.append(tile.as_dict(exclude_array=exclude_array), ignore_index=True)
#     return tiles_df


def new_tile_cutter(fdir: str, nrows: int, ncols: int,
                             altitude_m: Union[float, int],
                             target_dir: str = "",
                             location_name: str = "",
                             focal_length_mm: float = 8.6, sensor_width_mm: float = 12.8333,
                             save_csv: bool = True, keep_file_type: bool = False, file_type: str = ".JPG",
                             inject_gps_exif: bool = True, inject_uav_yaw: bool = True) -> str:
    """
    New, streamlined tile cutter, with no memory leak.
    :param fdir:
    :param nrows:
    :param ncols:
    :param altitude_m:
    :param target_dir:
    :param location_name:
    :param focal_length_mm:
    :param sensor_width_mm:
    :param save_csv:
    :param keep_file_type: Overrides parameter file_type
    :param file_type:
    :param inject_gps_exif: Only works if the saved tiles are jpg or jpeg
    :param inject_uav_yaw:
    :return:
    """
    if location_name:
        location_name += "_"  # Add underscore
    img_paths = [os.path.join(fdir, fname) for fname in sorted(os.listdir(fdir)) if fname.lower().endswith(IMG_FORMATS)]
    img_count = len(img_paths)

    tiles_dir = target_dir
    if not tiles_dir:
        tstamp = format(datetime.now(), "%Y-%m-%d")
        tiles_dir = os.path.join(fdir, f"tiles_{tstamp}")

    if not os.path.isdir(tiles_dir):
        os.makedirs(tiles_dir)

    tiles_df = None
    for i, fpath in enumerate(img_paths):
        print(f"Processing img. {i+1}/{img_count}: {fpath}")
        img_base_name = os.path.split(fpath)[-1].split(".")[0]
        img_coordinates, coords_found = geoprocessing.get_coordinates_from_img(fpath)
        print(img_coordinates)
        uav_yaw = geoprocessing.get_uav_yaw(fpath)
        print(uav_yaw)
        img = cv2.imread(fpath)
        img_height, img_width, channels = img.shape
        img_center_xy = (np.array([img_width, img_height]) / 2).astype(int)
        logging.debug(f"Img. center xy: {img_center_xy}")
        colwidth, rowheight = img_width / ncols, img_height / nrows

        for col in range(ncols):
            tile_center_latlong = (0, 0)  # To keep pycharm from complaining
            start_px_h = int(col * colwidth)
            end_px_h = int((col + 1) * colwidth)
            for row in range(nrows):
                start_px_v = int(row * rowheight)
                end_px_v = int((row + 1) * rowheight)
                logging.info(f"x, y: {(start_px_h, start_px_v)} to {end_px_h, end_px_v}")
                tile = img[start_px_v:end_px_v, start_px_h:end_px_h, :]
                coords_string = "_no_coords"
                if coords_found:
                    img_gsd_cm = geoprocessing.get_gsd(altitude_m=altitude_m, focal_length_real_mm=focal_length_mm,
                                                       sensor_width_mm=sensor_width_mm, img_width=img_width)
                    tile_center_xy = np.array([start_px_h + int(0.5 * colwidth), start_px_v + int(0.5 * rowheight)])
                    tile_center_latlong = geoprocessing.geolocate_point(pixel_xy=tuple(tile_center_xy),
                                                                        img_dims_wh=(img_width, img_height),
                                                                        img_lat_lon=img_coordinates,
                                                                        gsd_cm=img_gsd_cm, drone_yaw_deg=uav_yaw)
                    coords_string = geoprocessing.dd_coords_to_string(tile_center_latlong)

                if keep_file_type:
                    file_type = os.path.split(fpath)[-1].split('.')[-1]
                tile_name = f"{location_name}{img_base_name}_{row}-{col}{coords_string}.{file_type.strip().strip('.')}"
                tile_path = os.path.join(tiles_dir, tile_name)
                tile_img = PIL.Image.fromarray(tile[:, :, ::-1])
                tile_img.save(tile_path)
                cv2.imwrite(tile_path, tile)

                if save_csv and coords_found:
                    tile_info = {"img_path": [fpath], "tile_name": [tile_name],
                                 "img_lat": [img_coordinates[0]], "img_lon": [img_coordinates[1]],
                                 "tile_lat": [tile_center_latlong[0]], "tile_lon": [tile_center_latlong[1]],
                                 "uav_yaw_deg": uav_yaw}
                    if tiles_df is None:
                        tiles_df = pd.DataFrame(tile_info)
                    else:
                        tiles_df = tiles_df.append(pd.DataFrame(tile_info))
                    if inject_gps_exif:
                        try:
                            geoprocessing.inject_coord_info(tile_path, tile_center_latlong, 10)
                        except geoprocessing.ImageFormatError:
                            logging.info("Could not inject GPS info into exif data.")
                    if inject_uav_yaw and uav_yaw is not None:
                        geoprocessing.inject_uav_yaw(tile_path, uav_yaw)
    if save_csv:
        tiles_df.to_csv(os.path.join(tiles_dir, "tiles.csv"))
    print("Done.")
    return tiles_dir


if __name__ == "__main__":
    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)30s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    # logging.disable()

    # fpath_img = "/media/findux/DATA/Documents/Malta_II/surveys/Messina/DJI/frames/" \
    #             "Messina_tiles_2022-05-18/Messina_DJI_0003_out_67_1-0.tif"
    # img = cv2.imread(fpath_img)
    #
    # tile = Tile(array=img, timestamp=None, location="Messina",tile_position_yx=(1, 0), tile_center_abs_yx=(2, 2),
    #             tile_name="testtile", total_tiles_yx=(3, 3), dims_orig_img_yx=(123, 12332), orig_center=(20, 20),
    #             fpath_orig_img="/fuck/the/duck/", gsd_cm=2.3, fpath_tile="asjh")
    # print(tile)
    # tile.show()

    # fpath = "/media/findux/DATA/Documents/Malta_II/datasets/cecilia_martin/selection/test/"
    # fpath = "/media/findux/DATA/Documents/Malta_II/datasets/cecilia_martin/selection/"
    # fpath = "/media/findux/DATA/Documents/Malta_II/surveys/2022-05-03_Ramla/DJI_0154-002_24_frame_interval/"
    # fpath = "/media/findux/DATA/Documents/Malta_II/tests/geolocation_and_cutting/"
    # fpath = "/media/findux/DATA/Documents/Malta_II/tests/geolocation_one_img/"
    # new_tile_cutter(fpath, 2, 3, altitude_m=10, save_csv=True, keep_file_type=True)

    get_larges_img_dim("/home/findux/Desktop/pipeline_test/")