#!/usr/bin/env python3
import json

import PIL.Image
import cv2
import glob
import logging
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
from PIL.Image import Exif
import pyproj
import piexif
import pyexiv2
from typing import Tuple, Union


DELTA_STR = "\u0394"  # String to print the delta character

DEGREE_CONSTANT = 111_139  # This is outdated and incorrect


class ImageFormatError(Exception):
    def __init__(self, msg):
        # error_message = "Wrong Image format."
        super().__init__(msg)


def get_gsd(altitude_m, focal_length_real_mm=8.6, sensor_width_mm=12.8333, img_width=5472):
    """
    Returns the GSD in cm based on camera focal length.
    Default values taken from: https://community.pix4d.com/t/dji-phantom-4-pro-v2-0-gsd-and-camera-parameters/7478/2
    :param altitude_m:
    :param focal_length_real_mm: real focal length, not 35 mm equivalent.
    :param sensor_width_mm:
    :param img_width:
    :param img_height:
    :return:
    """
    gsd = (sensor_width_mm * altitude_m * 100) / (focal_length_real_mm * img_width)
    logging.info(f"GSD: {gsd}")
    return gsd


def gsd_m2ea(altitude_m, img_width, img_height = None):
    focal_length_real = 24 / 1.5
    sensor_width = 6.40  # https://en.wikipedia.org/wiki/Image_sensor_format#Table_of_sensor_formats_and_sizes
    gsd = get_gsd(altitude_m, focal_length_real, sensor_width, img_width)
    return gsd


def get_img_footprint_wh(gsd, img_width, img_height):
    fp_w = (gsd * img_width) / 100
    fp_h = (gsd * img_height) / 100
    return (fp_w, fp_h)


# def calc_latlong_shift_from_px_shift_DEPRECATED(px_offset_yx: Tuple[int, int], gsd_cm: float,
#                                      yaw_angle_deg: float = 0.0, degree_constant=DEGREE_CONSTANT) -> Tuple[float, float]:
#     """
#     NOT PRECISE ENOUGH. USE IMPROVED FORMULA!
#     Returns the shift in latitude, longitude (y, x)
#     :param px_offset_yx:
#     :param gsd_cm:
#     :param yaw_angle_deg:
#     :param degree_constant: Amount of meters that constitute 1 degree shift of either latitude or longitude.
#     :return:
#     """
#     if yaw_angle_deg is None:
#         return None, None
#     delta_y_abs, delta_x_abs = calc_abs_px_shift_yx(px_offset_yx, yaw_angle_deg)
#     delta_lat = (- delta_y_abs * gsd_cm) / (degree_constant * 100)
#     delta_long = (delta_x_abs * gsd_cm) / (degree_constant * 100)
#
#     logging.debug(f"Px offset: {px_offset_yx}")
#     logging.debug(f"GSD: {gsd_cm}")
#     logging.info(f"Yaw angle deg.: {yaw_angle_deg}")
#     logging.debug(f"Abs. px shift yx: {delta_y_abs, delta_x_abs}")
#     logging.info(f"Delta lat long: {delta_lat, delta_long}")
#     return delta_lat, delta_long


def transform_px_shift_to_m_shift(px_shift_yx, gsd_cm) -> tuple:
    """
    Converts a yx pixel shift to a yx meter shift.
    :param px_shift_yx: y shift, x shift. y increases downward, x inreases to the right.
    :param gsd_cm: ground sampling distance
    :return:  y shift (m), x shift (m). y increases downward, x inreases to the right.
    """
    delta_x, delta_y = px_shift_yx
    delta_x_m = delta_x * gsd_cm / 100
    delta_y_m = delta_y * gsd_cm / 100
    logging.info(f"Real world shift in meters: {delta_x_m:.4f} (x), {delta_y_m:.4f} (y)")
    return delta_y_m, delta_x_m


def get_real_world_latlong_shift_from_px_shift(px_shift_yx: Tuple[int, int], gsd_cm: float,
                                     latitude: float, yaw_angle_deg: float = 0.0):
    """
    Not sure if this also works on other hemispheres.\n
    :param px_offset_yx: y increases down, x increases towards the right
    :param gsd_cm:
    :param latitude: latitude where the image was taken.
    :param yaw_angle_deg: UAV yaw angle
    :return: (lat shift, lon shift). Lat increases northwards.
    """
    px_shift_angle = get_px_shift_angle(px_shift_yx)
    abs_shift_angle = transform_angle_to_180_range(px_shift_angle + yaw_angle_deg)
    shift_distance_px = get_shift_len(px_shift_yx)
    actual_px_shift_yx = get_real_world_px_shift(shift_distance_px, abs_shift_angle)
    real_world_yx_shift_in_m = transform_px_shift_to_m_shift(actual_px_shift_yx, gsd_cm)

    latlon_per_m = get_latlon_per_m(latitude)
    lat_shift = - real_world_yx_shift_in_m[0] * latlon_per_m[0]  # Minus because the shift increased downwards (i.e. south)
    lon_shift = real_world_yx_shift_in_m[1] * latlon_per_m[1]
    return lat_shift, lon_shift


def transform_angle_to_180_range(angle_deg) -> float:
    """
    :param angle_deg:
    :return: float in [-180 : 180]
    """
    angle_out = None
    # Adjust for > 360 (unlikely, but who knows).
    if angle_deg < 0:
        angle_deg = angle_deg % -360
    elif angle_deg > 0:
        angle_deg = angle_deg % 360
    elif abs(angle_deg) == 360:
        angle_deg = 0

    if abs(angle_deg) in [0, 180]:
        angle_out = angle_deg
    # Negative degrees:
    elif -180 < angle_deg < 0:
        # print("In left half")
        angle_out = angle_deg
    elif angle_deg < -180:
        # print("Over left half")
        angle_out = 180 + (angle_deg % -180)
    # Positive degrees:
    elif 0 < angle_deg < 180:
        # print("In right half)")
        angle_out = angle_deg
    elif angle_deg > 180:
        # print("Over right half")
        angle_out = -180 + (angle_deg % 180)
    else:
        raise ArithmeticError("Could not calculate world angle.")
    logging.info(f"Angle within 180 range: {angle_out}")
    return angle_out


def get_meridian_parallel_radii(lat_deg, a=6378137, e2=6.6943799901413165e-3) -> tuple:
    """

    :param lat_deg:
    :param a:
    :param e2:
    :return: meridian radius, parallel radius
    """
    u = 1 - e2 * math.sin(math.radians(lat_deg)) ** 2
    meridian_radius = ((1 - e2) / u) * (a / math.sqrt(u))
    parallel_radius = math.cos(math.radians(lat_deg)) * (a / math.sqrt(u))
    # Apparently this was wrong, the values need to be flipped:
    meridian_radius, parallel_radius = parallel_radius, meridian_radius

    logging.info(f"Meridian radius: {meridian_radius:,.1f} m | Parallel radius: {parallel_radius:,.1f} m")
    return meridian_radius, parallel_radius


def get_latlon_m(lat):
    lon_lat_radii = get_meridian_parallel_radii(lat)
    lon_m, lat_m = [r * math.pi / 180 for r in lon_lat_radii]
    logging.info(f"At {lat}° latitude: {lat_m:,.2f} m per latitude, {lon_m:,.2f} m per longitude.")
    return lat_m, lon_m


def get_latlon_per_m(lat_deg) -> Tuple[float, float]:
    m_per_lat, m_per_lon = get_latlon_m(lat_deg)
    return 1 / m_per_lat, 1 / m_per_lon


# def calc_px_shift_angle_TOBEDEPRECATED(px_shift_yx: Tuple[int, int]) -> float:
#     """
#     Returns the angle of the pixel shift in degrees.
#     NOTE THAT 0° is located at 09:00!
#     :param px_shift_yx:
#     :return:
#     """
#     angle = None
#     if px_shift_yx == (0, 0):
#         raise ArithmeticError("No pixel shift. Both shifts are zero.")
#     delta_y, delta_x = px_shift_yx
#     # Cover right angles:
#     if delta_y == 0 and delta_x < 0:
#         angle = 0.0
#     elif delta_y < 0 and delta_x == 0:
#         angle = 90.0
#     elif delta_y == 0 and delta_x > 0:
#         angle = 180.0
#     elif delta_y > 0 and delta_x == 0:
#         angle = 270.0
#     # Cover angles that are not in [0, 90, 180, 270, 360]
#     elif delta_y < 0 and delta_x < 0:
#         logging.info("Top-left quadrant.")
#         angle = trigonometry_angle_from_adjacent_and_opposite(abs(delta_x), abs(delta_y))
#     elif delta_y < 0 and delta_x > 0:
#         logging.info("Top-right quadrant.")
#         angle = 90 + (90 - trigonometry_angle_from_adjacent_and_opposite(delta_x, abs(delta_y)))
#     elif delta_y > 0 and delta_x > 0:
#         logging.info("Bottom-right quadrant.")
#         angle = 180 + trigonometry_angle_from_adjacent_and_opposite(delta_x, delta_y)
#     elif delta_y > 0 and delta_x < 0:
#         logging.info("Bottom-left quadrant")
#         angle = 270 + (90 - trigonometry_angle_from_adjacent_and_opposite(abs(delta_x), delta_y))
#     else:
#         raise ArithmeticError(f"Could not calculate angle for shift {px_shift_yx}")
#     return angle


def get_px_shift_angle(px_shift_yx: tuple) -> float:
    """
    Returns the angle of the pixel shift. North (up) is 0, down is 180 or -180. Left is -90, right is 90. \n
    :param px_shift_yx: (y shift, x shift). Y increases downward. X increases to the right.
    :return: float in [-180.0 : 180.0]
    """
    if px_shift_yx == (0, 0):
        logging.info("No px shift.")
        return 0

    y_shift, x_shift = px_shift_yx
    shift_angle = None
    # If one of them is zero:
    if y_shift == 0 and x_shift != 0:
        if x_shift < 0:
            logging.info("px shift angle: Straight left.")
            shift_angle = -90  # Straight left
        else:
            logging.info("px shift quadrant: Straight right.")
            shift_angle = 90  # Straight right
    elif x_shift == 0 and y_shift != 0:
        if y_shift < 0:
            logging.info("px shift angle: Straight up.")
            shift_angle = 0  # Straight up
        else:
            logging.info("px shift angle: Straight down.")
            shift_angle = 180  # Straight down
    # Go over the quadrants:
    # TL:
    elif x_shift < 0 and y_shift < 0:
        logging.info("px shift quadrant: TL.")
        shift_angle = - math.degrees(math.atan(abs(x_shift)/abs(y_shift)))
    # BL:
    elif x_shift < 0 < y_shift:
        logging.info("px shift quadrant: BL.")
        shift_angle = -90 - math.degrees(math.atan(y_shift / abs(x_shift)))
    # TR:
    elif y_shift < 0 < x_shift:
        logging.info("px shift quadrant: TR.")
        shift_angle = math.degrees(math.atan(x_shift / abs(y_shift)))
    # BR:
    elif x_shift > 0 and y_shift > 0:
        logging.info("px shift quadrant: BR.")
        shift_angle = 90 + math.degrees(math.atan(y_shift/x_shift))
    else:
        raise ArithmeticError("Could not calculate offset angle.")
    logging.info(f"px shift angle = {shift_angle}")
    return shift_angle


def get_real_world_px_shift(shift_distance, angle) -> tuple:
    """
    Y increases downwards
    :param shift_distance:
    :param angle:
    :return: yx shift. Y increases downwards.
    """
    dy, dx = None, None
    # Cover the four cardinal directions
    if shift_distance == 0:
        return 0, 0
    elif angle == 0:
        dy, dx = -shift_distance, 0
    elif angle == 90:
        dy, dx = 0, shift_distance
    elif angle == -90:
        dy, dx = 0, -shift_distance
    elif abs(angle) == 180:
        dy, dx = shift_distance, 0
    # Cover the values in between:
    # TL
    # ToDo: CHECK THESE:
    elif -90 < angle < 0:
        dx = - math.sin(math.radians(abs(angle))) * shift_distance
        dy = - math.cos(math.radians(abs(angle))) * shift_distance
    # BL:
    elif -180 < angle < -90:
        angle_subset = angle + 90  # "remove" top left quadrant from the angle
        dx = - math.cos(math.radians(abs(angle_subset))) * shift_distance
        dy = math.sin(math.radians(abs(angle_subset))) * shift_distance
    # TR:
    elif 0 < angle < 90:
        dx = math.sin(math.radians(angle)) * shift_distance
        dy = - math.cos(math.radians(angle)) * shift_distance
    # BR:
    elif 90 < angle < 180:
        angle_subset = angle - 90  # "Remove TR quadrant from angle value
        dx = math.cos(math.radians(angle_subset)) * shift_distance
        dy = math.sin(math.radians(angle_subset)) * shift_distance
    logging.info(f"Actual px xy shift (incorporating UAV yaw): {dx:.2f}, {dy:.2f} (rounded)")
    return dy, dx


def get_px_delta_from_hypotenuse_and_angle(hypotenuse: float, alpha_deg):
    """
    Calculates the x- and y-shift between points a and b of a right triangle from hypotenuse length and alpha
    angle value (in degrees). Assumes that CA is the X axis and CB is the Y axis.
    :param hypotenuse: length of the hypotenuse
    :param alpha_deg:
    :return:
    """
    if hypotenuse is None or alpha_deg is None:
        return None, None
    delta_y = - math.sin(math.radians(alpha_deg)) * hypotenuse
    delta_x = - math.cos(math.radians(alpha_deg)) * hypotenuse
    logging.info(f"{DELTA_STR}y: {delta_y}, {DELTA_STR}x: {delta_x}")
    return delta_y, delta_x


def get_shift_len(px_shift_yx):
    """Calculates total length of shift (i.e. hypotenuse) based on delta x and delta y."""
    dy, dx = px_shift_yx
    shift_len = math.sqrt(dy ** 2 + dx ** 2)
    logging.info(f"shift len: {shift_len:.2f} px (rounded)")
    return shift_len


def geolocate_point(pixel_xy: Tuple[int, int], img_dims_wh: Tuple[int, int], img_lat_lon: Tuple[float, float],
                    gsd_cm: float, drone_yaw_deg: float) -> tuple:
    """
    Calculates the latitude/longitude of a given point.
    :param pixel_xy: point location in image.
    :param img_dims_wh: Image width and height in pixels.
    :param img_lat_lon: Img. latitude and longitude in decimal degrees.
    :param gsd_cm: Ground sampling distance (cm).
    :param drone_yaw_deg: drone rotation in degrees. Straight north = 0.
    :return: (latitude, longitude) in decimal degrees (WGS84).
    """
    px_x, px_y = pixel_xy
    img_width, img_height = img_dims_wh
    img_latitude, img_longitude = img_lat_lon

    img_center_x = int(img_width * 0.5)
    img_center_y = int(img_height * 0.5)

    delta_x = px_x - img_center_x
    delta_y = px_y - img_center_y

    delta_lat, delta_lon = get_real_world_latlong_shift_from_px_shift(px_shift_yx=(delta_y, delta_x), gsd_cm=gsd_cm,
                                                                      latitude=img_latitude,
                                                                      yaw_angle_deg=drone_yaw_deg)
    if delta_lat is not None and delta_lon is not None:
        point_lat = img_latitude + delta_lat
        point_lon = img_longitude + delta_lon
        return point_lat, point_lon
    return None, None


def geolocate_point_on_img(pixel_xy: Tuple[int, int],
                           fpath_img: str, altitude_m: Union[float, int],
                           focal_length_mm=8.6, sensor_width_mm=12.8333) -> Tuple[float, float]:
    """
    Calculates the latitude/longitude of a given point on an image.
    :param altitude_m:
    :param sensor_width_mm:
    :param pixel_xy: point location in image.
    :param img_dims_wh: Image width and height in pixels.
    :param img_lat_lon: Img. latitude and longitude in decimal degrees.
    :param gsd_cm: Ground sampling distance (cm).
    :param drone_yaw_deg: drone rotation in degrees. Straight north = 0.
    :return: (latitude, longitude) in decimal degrees (WGS84).
    """

    img_height, img_width, channels = cv2.imread(fpath_img).shape
    (img_latitude, img_longitude), coords_found = get_coordinates_from_img(fpath_img)
    drone_yaw_deg = get_uav_yaw(fpath_img)
    gsd_cm = get_gsd(altitude_m, focal_length_mm, sensor_width_mm, img_width, img_height)

    lat_lon = geolocate_point(pixel_xy, (img_width, img_height), (img_latitude, img_longitude), gsd_cm, drone_yaw_deg)

    return lat_lon


def dd_to_dms(dd: float) -> Tuple[int, int, float]:
    """
    Converts a decimal degree value into degrees, minutes and decimal seconds.
    :param dd: decimal degrees
    :return: Tuple (dd, mm, ss.ss)
    """
    degrees = int(dd)  # int always rounds down
    dminutes = (dd - degrees) * 60
    minutes = int(dminutes)
    seconds = (dminutes - minutes) * 60
    return degrees, minutes, seconds


def dms_to_dd(deg_min_sec: tuple):
    if deg_min_sec is None:
        return None

    assert len(deg_min_sec) == 3
    _deg, _min, _sec = deg_min_sec
    dd_coordinate = float(_deg) + float(_min) / 60 + float(_sec) / 3600
    return dd_coordinate


def dd_coords_to_string(coords_dd: tuple):
    if coords_dd[0] is None or coords_dd[1] is None:
        return "_no_coords_"
    lat_suffix = "N"
    lon_suffix = "E"
    lat, lon = coords_dd
    if lat < 0:
        lat_suffix = "S"
    if lon < 0:
        lon_suffix = "W"
    str_out = f"_{abs(lat)}{lat_suffix}_{abs(lon)}{lon_suffix}".replace('.', '-')
    return str_out


def get_hemispheres(latlong_dd: Tuple[float, float]) -> tuple:
    """

    :param latlong_dd: Coordinates in decimal degrees.
    :return: Tuple with the N/S and E/W hemisphere, e.g. ("N", "E").
    """
    lat, lon = latlong_dd
    hemis_lat = None
    hemis_lon = None
    if lat >= 0:
        hemis_lat = "N"
    elif lat < 0:
        hemis_lat = "S"
    if lon >= 0:
        hemis_lon = "E"
    elif lon < 0:
        hemis_lon = "W"
    return hemis_lat, hemis_lon


def get_uav_yaw(fpath_img: str):
    """
    Extracts UAV yaw from DJI jpeg images. This does not work for images from the FLIR camera.
    :param fpath_img: image filepath
    :return: yaw degrees (float)
    """
    yaw_degrees = None
    img_metadata = get_metadata_bytes(fpath_img)
    if img_metadata is not None:
        logging.debug(type(img_metadata))
        try:
            yaw_degrees = img_metadata.read_xmp()["Xmp.drone-dji.FlightYawDegree"]
        except KeyError:
            logging.info(f"[ WARNING ] No UAV yaw for {fpath_img}.")
            yaw_degrees = None
        else:
            yaw_degrees = float(yaw_degrees)
    return yaw_degrees


def inject_uav_yaw(fpath_img: str, uav_yaw: Union[float, str]):
    """
    Injects uav_yaw value into the image xmp metadata. Overwrites existing data.
    :param fpath_img: path to image
    :param uav_yaw: yaw. in [-180, 180]
    :return:
    """
    yaw_data = {"Xmp.drone-dji.FlightYawDegree": str(uav_yaw)}
    with pyexiv2.Image(fpath_img) as img:
        img.modify_xmp(yaw_data)


def inject_coord_info(fpath, latlong_dd, altitude_m):
    if not fpath.lower().endswith(("jpg", "jpeg")):
        raise ImageFormatError("Img needs to be jpeg or jpg")
    # 34853 GPSInfo
    lat_dd, lon_dd = latlong_dd
    lat_dms, lon_dms = dd_to_dms(lat_dd), dd_to_dms(lon_dd)
    hem_lat, hem_lon = get_hemispheres(latlong_dd)
    img = Image.open(fpath)
    exif_raw = img.info.get("exif")  # Get: None if KeyError
    if exif_raw is not None:
        exif = piexif.load(exif_raw)
    else:
        exif = {}
    exif["GPS"] = {0: (2, 3, 0, 0),
                   1: bytes(hem_lat, encoding="utf8"),
                   2: ((lat_dms[0], 1), (lat_dms[1], 1), (int(lat_dms[2] * 10_000), 10_000)),
                   3: bytes(hem_lon, encoding="utf8"),
                   4: ((lon_dms[0], 1), (lon_dms[1], 1), (int(lon_dms[2] * 10_000), 10_000)),
                   5: 0,
                   6: (altitude_m * 1000, 1000)
                   }
    exif_b = piexif.dump(exif)
    piexif.insert(exif_b, fpath, fpath)


def get_all_img_coordinates(fdir_img) -> pd.DataFrame:
    """
    Extracts the coordinates for all image files in one folder.
    :param img_path:
    :return:
    """
    img_list = sorted(os.listdir(fdir_img))
    # Exclude non-files (i.e. directories)
    img_list = [img for img in img_list if os.path.isfile(os.path.join(fdir_img, img))]

    logging.info(img_list)
    img_df = pd.DataFrame({"file_name": img_list})
    img_df["path"] = [os.path.join(fdir_img, fname) for fname in img_df["file_name"]]
    latitudes = []
    longitudes = []
    for fpath in img_df["path"]:
        logging.info(f"fpath: {fpath}")
        coords = get_coordinates_from_img(fpath)
        if coords is not None:
            lat = get_coordinates_from_img(fpath)[0]
            lon = get_coordinates_from_img(fpath)[1]
            latitudes.append(lat)
            longitudes.append(lon)
    img_df["latitude"] = latitudes
    img_df["longitude"] = longitudes
    return img_df


def get_coordinates_from_img(fpath_img) -> Tuple[Tuple[float, float], bool]:
    """
    Returns (lat, long) of the image.

    :param fpath_img:
    :return: ((lat, lon), coords_found)
    """
    lat, lon = None, None
    coords_found = False
    coords_dict = {"latlon": (None, None), "coords_found": False}
    exif_raw = get_raw_exif(fpath_img)
    if exif_raw is not None:
        geoinfo = get_geo_info_from_exif(exif_raw)
        if geoinfo:
            lat = geoinfo["latitude"]
            lon = geoinfo["longitude"]
            coords_found = True
    return (lat, lon), coords_found


def get_metadata_bytes(fpath_img) -> pyexiv2.ImageData:
    try:
        with open(fpath_img, "rb") as f:
            img_bytes = f.read()
    except FileNotFoundError:
        logging.error(f"Could not find file {fpath_img}")
        return None
    else:
        img_metadata = pyexiv2.ImageData(img_bytes)
        return img_metadata


def get_raw_exif(fpath: str) -> PIL.Image.Exif:
    with Image.open(fpath) as im:
        exif = im.getexif()  # Returns PIL.Image.Exif
    return exif


def get_raw_exif_b(fpath: str) -> bytes:
    img = Image.open(fpath)
    exif = img.info.get("exif")  # Returns bytes
    return exif


def get_geo_info_from_exif(raw_exif: Exif) -> dict:
    """
    Extracts the gps info from raw exif data and returns a dictionary
    :param raw_exif:
    :return:
    """
    geo_readable = get_readable_geoinfo(raw_exif)
    #
    # try:
    #     geo_readable = extract_readable_geoinfo(raw_exif)
    # except:
    #     logging.debug(f"Could not transform raw exif into readable exif.")
    if geo_readable is not None:
        try:
            geo_out = {"crs": "NONE",
                       "hemisphere_N_S": geo_readable["GPSLatitudeRef"],
                       "hemisphere_E_W": geo_readable["GPSLongitudeRef"],
                       "latitude": dms_to_dd(geo_readable["GPSLatitude"]),
                       "longitude": dms_to_dd(geo_readable["GPSLongitude"])}
            geo_out = {"crs": "NONE",
                       "hemisphere_N_S": geo_readable.get("GPSLatitudeRef"),
                       "hemisphere_E_W": geo_readable.get("GPSLongitudeRef"),
                       "latitude": dms_to_dd(geo_readable.get("GPSLatitude")),
                       "longitude": dms_to_dd(geo_readable.get("GPSLongitude"))}
        except KeyError:
            print("Could not get GPS info for writing into tile.")
        else:
            return geo_out
    return {}


def get_readable_geoinfo(raw_exif):
    geo_readable = None
    if raw_exif is not None:
        for key, value in TAGS.items():
            # logging.info(key, value)
            if value == "GPSInfo":
                gps_info = raw_exif.get_ifd(key)
                geo_readable = {GPSTAGS.get(key, key): value for key, value in gps_info.items()}
                break
    return geo_readable


def print_exif_data(fpath):
    raw_exif = get_raw_exif(fpath)
    for tag_no, name in TAGS.items():
        info_package = raw_exif.get_ifd(tag_no)
        package_contents = {GPSTAGS.get(tag_no, tag_no): value for key, value in info_package.items()}
        print(f"{tag_no}\t{name}\t{package_contents}")


def point_picker(img_fpath: str) -> Tuple[int, int]:
    """
    Lets the user pick a point on the image using the mouse and returns the x and y coordinates as a tuplle
    :param img_fpath:
    :return: (x, y)
    """
    img = plt.imread(img_fpath)
    plt.imshow(img)
    point_coords = plt.ginput(1)[0]
    point_coords = int(point_coords[0]), int(point_coords[1])
    print(f"Picked x,y coordinates: {point_coords}")
    return point_coords


def test_1():
    print("Test 01:")
    gsd = 10
    drone_yaw = 0
    img_dims_wh = (520_000, 400_000)
    pt_xy = (515_520, 380_120)
    img_lat_long = (35.98188, 14.33238)
    point_coordinates = geolocate_point(pt_xy, img_dims_wh, img_lat_long, gsd, drone_yaw)
    print(point_coordinates)

    print("Test 02:")
    gsd = 10
    drone_yaw = 35.18060113378763
    img_dims_wh = (800_000, 400_000)
    pt_xy = (400_000 + 312_624, 200_000)
    img_lat_long = (35.98188, 14.33238)
    point_coordinates = geolocate_point(pt_xy, img_dims_wh, img_lat_long, gsd, drone_yaw)
    print(point_coordinates)

    print(f"Test w/ GCP")
    fpath_img_500 = "/media/findux/DATA/Documents/Malta_II/surveys/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0500.JPG"
    fpath_img_504 = "/media/findux/DATA/Documents/Malta_II/surveys/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0504.JPG"
    gcp_49_504 = (794, 3031)
    gcp_49_500 = (2892, 3185)


def test_2_circle(fpath_results_csv: str):
    altitude = 100
    latlon_img = (35.9, 14.4)
    img_w = 5472
    img_h = 3648
    point_xy = (1536, 624)
    gsd = get_gsd(altitude, img_width=img_w)

    points = {"location": [],
              "coords": []}

    points["location"].append("center")
    points["coords"].append(latlon_img)

    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=0))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=45))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=90))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=135))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=175))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-45))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-90))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-135))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-175))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-180))

    points = pd.DataFrame(points)
    points[["latitude", "longitude"]] = pd.DataFrame(points["coords"].tolist(), index=points.index)
    points.drop("coords", axis=1, inplace=True)
    points.to_csv(fpath_results_csv, index=False)





# def get_abs_angle(px_shift_yx, yaw_deg) -> float:
#     """
#     Calculates absolute angle of the shift, based on original pixel shift and drone yaw.
#     :param px_shift_yx:
#     :param yaw_deg: UAV yaw angle in degrees
#     :return: absolute angle of the shift in degrees, or None if yaw_deg is None.
#     """
#     if yaw_deg is None:
#         return None
#     # assert abs(yaw) not in [0, 90, 180, 270, 360]  # Because in these cases the angle is not needed.
#     assert px_shift_yx != (0, 0)
#     logging.info(f"Yaw: {yaw_deg}")
#     _px_angle = calc_px_shift_angle_TOBEDEPRECATED(px_shift_yx)
#     abs_angle = _px_angle + yaw_deg
#     logging.info(f"Abs angle {abs_angle}")
#     return transform_to_positive_degrees(abs_angle)


# def calc_abs_px_shift_yx(px_shift_yx: tuple, yaw_deg: float) -> tuple:
#     """Takes the pixel shift inside the image and the drone yaw and gives the 'real-world' shift (yx) in pixels."""
#     if px_shift_yx == (0, 0):
#         return px_shift_yx
#     abs_angle = get_abs_angle(px_shift_yx, yaw_deg)
#     shift_len = get_shift_len(px_shift_yx)
#     abs_delta_y, abs_delta_x = get_px_delta_from_hypotenuse_and_angle(shift_len, abs_angle)
#     return abs_delta_y, abs_delta_x


# def trigonometry_angle_from_adjacent_and_opposite(adjacent, opposite) -> float:
#     """
#     Returns the angle between adjacent and hypotenuse of a right triangle (in degrees).
#     :param adjacent: length of adjacent edge
#     :param opposite: length of opposite edge
#     :return: angle in degrees (btw. hypotenuse and adjacent edge).
#     """
#     angle = math.degrees(math.atan(opposite / adjacent))
#     return angle


# def get_abs_deg_12c(deg_raw):
#     abs_360_deg = deg_raw % 360
#     if abs_360_deg > 180:
#         return abs_360_deg - 360
#     else:
#         return abs_360_deg


# def get_m_per_lat_lon_degree(latitude) -> tuple:
#     _m1 = 111132.92  # latitude calculation term 1
#     _m2 = -559.82  # latitude calculation term 2
#     _m3 = 1.175  # latitude calculation term 3
#     _m4 = -0.0023  # latitude calculation term 4
#     _p1 = 111412.84  # longitude calculation term 1
#     _p2 = -93.5  # longitude calculation term 2
#     _p3 = 0.118  # longitude calculation term 3
#     m_per_lat = _m1 + _m2 * math.cos(2 * latitude) + _m3 * math.cos(4 * latitude) + _m4 * math.cos(6 * latitude)
#     m_per_lon = _p1 * math.cos(latitude) + _p2 * math.cos(3 * latitude) + _p3 * math.cos(5 * latitude)
#     return m_per_lat, m_per_lon


# def get_m_per_lat_lon_degree_rad(latitude) -> tuple:
#     _m1 = 111132.92  # latitude calculation term 1
#     _m2 = -559.82  # latitude calculation term 2
#     _m3 = 1.175  # latitude calculation term 3
#     _m4 = -0.0023  # latitude calculation term 4
#     _p1 = 111412.84  # longitude calculation term 1
#     _p2 = -93.5  # longitude calculation term 2
#     _p3 = 0.118  # longitude calculation term 3
#     m_per_lat = _m1 \
#                 + _m2 * math.cos(2 * math.radians(latitude)) \
#                 + _m3 * math.cos(4 * math.radians(latitude)) \
#                 + _m4 * math.cos(6 * math.radians(latitude))
#     m_per_lon = _p1 * math.cos(math.radians(latitude)) \
#                 + _p2 * math.cos(3 * math.radians(latitude)) \
#                 + _p3 * math.cos(5 * math.radians(latitude))
#     return m_per_lat, m_per_lon


# def get_m_per_latlon_wikipedia(latitude):
#     """https://en.wikipedia.org/wiki/Geographic_coordinate_system#Length_of_a_degree"""
#     lat = math.radians(latitude)
#     m_per_lat = 111_132.02 + 559.82 * math.cos(lat)
#     m_per_lon = 111412 * math.cos(lat) - 93.5 * math.cos(3 * lat) + 0.118 * math.cos(5 * lat)
#     return m_per_lat, m_per_lon
#
#
# def m_per_deg_quickanddirty(latitude):
#     """Quick and dirty method: https://gis.stackexchange.com/a/2964"""
#     m_lat = 111_111
#     m_lon = 111_111 * math.cos(math.radians(latitude))
#     return m_lat, m_lon


# def m_per_deg(lat_deg):
#     radius_meridian, radius_parallel = get_meridian_parallel_radii(lat_deg)
#     radius_meridian = radius_meridian



# def get_px_shift_angle_c12(px_shift_xy: Union[Tuple, np.array]) -> float:
#     """0° is straight up, 12:00 on a clock.
#     :returns:  float between -180 and 180"""
#     delta_x, delta_y = px_shift_xy
#     # No shift
#     if (delta_x, delta_y) == (0, 0):
#         print("No px. shift, therefore no angle.")
#         return 0
#     # Cover the 90 degree angles
#     if delta_x == 0 and delta_y < 0:
#         return 0
#     elif delta_x == 0 and delta_y > 0:
#         return 180
#     elif delta_y == 0 and delta_x < 0:
#         return -90
#     elif delta_y == 0 and delta_x > 0:
#         return 90
#     # Cover the other quadrants:
#     elif delta_x < 0 and delta_y < 0:
#         logging.debug("Top-left quadrant")
#         return - math.degrees(math.atan(abs(delta_x) / abs(delta_y)))
#     elif delta_y < 0 < delta_x:
#         logging.debug("Top-right quadrant")
#         return math.degrees(math.atan(abs(delta_x) / abs(delta_y)))
#     elif delta_x < 0 < delta_y:
#         logging.debug("Bottom-left quadrant")
#         return -90 - (90 - math.degrees(math.atan(abs(delta_y) / abs(delta_x))))
#     elif delta_x > 0 and delta_y > 0:
#         logging.debug("Bottom-right quadrant")
#         return 90 + (90 - math.degrees(math.atan(abs(delta_y) / abs(delta_x))))
#     else:
#         print("No px_shift angle extracted.")
#         return 0


# def transform_to_positive_degrees(raw_degree):
#     """Transforms a degree value that can be negative or above 360 into a degree value between of (0<= value < 360)"""
#     sign = 1
#     if raw_degree < 0:
#         raw_degree = 360 - abs(raw_degree) % 360
#         sign *= -1
#     actual = raw_degree % 360
#     return actual


# def get_coordinates_from_img(fpath_img) -> Tuple[tuple, bool]:
#     """
#     Returns (lat, long) of the image.
#     :param fpath_img:
#     :return: tuple (lat, lon). Returns None if no coordinates could be extracted
#     """
#     exif_raw = get_raw_exif(fpath_img)
#     if exif_raw is not None:
#         geoinfo = get_geo_info_from_exif(exif_raw)
#         if geoinfo:
#             return (geoinfo["latitude"], geoinfo["longitude"]), True
#     else:
#         return (None, None), False

if __name__ == "__main__":

    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)30s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)


    # logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s]\t%(message)s")
    # print(calc_latlong_shift_from_px_shift(px_offset_yx=(111_139_00, 111_139_00), gsd_cm=1))
    # print(calc_latlong_shift_from_px_shift(px_offset_yx=(-111_139_00, 111_139_00), gsd_cm=1))
        # for lat in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]:
        #     m = get_latlon_m(lat)
        #     print(f"{m[1]:,.0f}\t{m[0]:,.0f}")
        # print()
        # for lat in [0, 15, 30, 45, 60, 75, 90]:
        #     m = get_latlon_m(lat)
        #     print(f"{m[1]:,.0f}\t{m[0]:,.0f}")

    # # TL
    # print("Top-left:")
    # x = -1824
    # y = -912
    # print(-90 + math.degrees(math.atan(abs(y) / abs(x))))
    # print(- math.degrees(math.atan(abs(x) / abs(y))))
    #
    # x = -180
    # y = -912
    # print(-90 + math.degrees(math.atan(abs(y) / abs(x))))
    # # BL
    # print("Bottom-left:")
    # x = -1824
    # y = -912
    # print(-90 - math.degrees(math.atan(abs(y) / abs(x))))
    # x = -180
    # y = -912
    # print(-90 - math.degrees(math.atan(abs(y) / abs(x))))
    # # TR:
    # print("Top-right:")
    # x = 1824
    # y = -912
    # print(math.degrees(math.atan(x / abs(y))))
    # x = 180
    # y = -912
    # print(math.degrees(math.atan(x / abs(y))))
    # # BR:
    # print("Bottom-right:")
    # x = 1824
    # y = 912
    # print(90 + math.degrees(math.atan(y / x)))
    # x = 180
    # y = 912
    # print(90 + math.degrees(math.atan(y / x)))

    # print(get_px_delta_from_hypotenuse_and_angle(2039, 116))
    # print(math.sqrt(200 ** 2 + 200 ** 2))
    altitude = 100
    latlon_img = (35.9, 14.4)
    img_w = 5472
    img_h = 3648
    point_xy = (1536, 624)
    gsd = get_gsd(altitude, img_width=img_w)

    points = {"location": [],
              "coords": []}

    points["location"].append("center")
    points["coords"].append(latlon_img)

    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=0))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=45))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=90))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=135))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=175))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-45))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-90))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-135))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-175))
    points["location"].append("shifted")
    points["coords"].append(geolocate_point(point_xy, (img_w, img_h), latlon_img, gsd, drone_yaw_deg=-180))


    points = pd.DataFrame(points)
    points[["latitude", "longitude"]] = pd.DataFrame(points["coords"].tolist(), index=points.index)
    points.drop("coords", axis=1, inplace=True)
    points.to_csv("/home/findux/Desktop/test_coord_circle.csv")