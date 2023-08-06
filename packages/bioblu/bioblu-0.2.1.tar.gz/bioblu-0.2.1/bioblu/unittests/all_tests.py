#!/usr/bin/env python3

from numpy.testing import assert_allclose
import os
import pathlib
import unittest

from bioblu.ds_manage import geoprocessing, img_cutting, ds_annotations
from bioblu.ds_manage.ds_annotations import BBox


class GeoprocessingTests(unittest.TestCase):

    def test_world_angle(self):
        self.assertEqual(geoprocessing.transform_angle_to_180_range())
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(30), 30)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(-30), -30)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(179), 179)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(-179), -179)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(180), 180)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(-180), -180)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(0), 0)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(190), -170)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(-190), 170)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(0), 0)
        self.assertEqual(geoprocessing.get_world_angle_zeronorth(360), 0)

    # def test_trigonometry(self):
    #     self.assertAlmostEqual(geoprocessing.trigonometry_angle_from_adjacent_and_opposite(40, 14.558809370648094), 20.0)
    #     self.assertAlmostEqual(geoprocessing.trigonometry_angle_from_adjacent_and_opposite(40, 69.28203230275507), 60.0)
    #     self.assertAlmostEqual(geoprocessing.trigonometry_angle_from_adjacent_and_opposite(20, 20), 45.0)

    def test_extract_coordinates(self):
        unittest_dirloc = pathlib.Path(__file__).parent.resolve()
        img_path = os.path.join(unittest_dirloc, "DJI_0503_resized.JPG")
        coords, coords_found = geoprocessing.get_coordinates_from_img(img_path)
        self.assertEqual(coords, (35.981887472222226, 14.332385416666666))

    def test_dd_to_dms(self):
        assert_allclose(geoprocessing.dd_to_dms(156.742), (156, 44, 31.2))
        assert_allclose(geoprocessing.dd_to_dms(42.3601), (42, 21, 36.36))
        assert_allclose(geoprocessing.dd_to_dms(0.000856), (0, 0, 3.0816))

    def test_px_shift_angle_zeronorth(self):
        self.assertEqual(geoprocessing.get_px_shift_angle((-90, 0)), 0)
        self.assertEqual(geoprocessing.get_px_shift_angle((90, 0)), 180)
        self.assertEqual(geoprocessing.get_px_shift_angle((-90, -90)), -45)
        self.assertEqual(geoprocessing.get_px_shift_angle((-90, 90)), 45)
        self.assertEqual(geoprocessing.get_px_shift_angle((90, -90)), -135)
        self.assertEqual(geoprocessing.get_px_shift_angle((90, 90)), 135)

    def test_yx_shift_from_angle(self):
        self.assertAlmostEqual(geoprocessing.get_real_world_px_shift(282.842712474619, 45)[0], -200)
        self.assertAlmostEqual(geoprocessing.get_real_world_px_shift(282.842712474619, 45)[1], 200)

        self.assertAlmostEqual(geoprocessing.get_real_world_px_shift(282.842712474619, 135)[0], 200)
        self.assertAlmostEqual(geoprocessing.get_real_world_px_shift(282.842712474619, 135)[1], 200)

        self.assertAlmostEqual(geoprocessing.get_real_world_px_shift(282.842712474619, -45)[0], -200)
        self.assertAlmostEqual(geoprocessing.get_real_world_px_shift(282.842712474619, -45)[1], -200)

        self.assertAlmostEqual(geoprocessing.get_real_world_px_shift(282.842712474619, -135)[0], 200)
        self.assertAlmostEqual(geoprocessing.get_real_world_px_shift(282.842712474619, -135)[1], -200)

    def test_px_shift_angle(self):
        self.assertEqual(geoprocessing.get_px_shift_angle((-20, -20)), -45)
        self.assertEqual(geoprocessing.get_px_shift_angle((-20, 20)), 45)
        self.assertEqual(geoprocessing.get_px_shift_angle((20, 20)), 135)
        self.assertEqual(geoprocessing.get_px_shift_angle((20, -20)), -135)
        self.assertEqual(geoprocessing.get_px_shift_angle((0, 20)), 90)
        self.assertEqual(geoprocessing.get_px_shift_angle((20, 0)), 180)

    def test_dms_to_dd(self):
        assert_allclose(geoprocessing.dms_to_dd((156, 11, 12.3)), 156.186759999)
        assert_allclose(geoprocessing.dms_to_dd((0, 0, 0.255)), 0.0000708333333)
        assert_allclose(geoprocessing.dms_to_dd((0, 0, 0.001)), 0.0000002777778)

    # def test_latlon_shift_from_px_shift(self):
    #     assert_allclose(geoprocessing.calc_real_world_latlong_shift_from_px_shift((-111_139, 111_139), 100, ), (1.0, 1.0))
    #     assert_allclose(geoprocessing.calc_real_world_latlong_shift_from_px_shift((111_139, 111_139), 100, ), (-1.0, 1.0))
    #     assert_allclose(geoprocessing.calc_real_world_latlong_shift_from_px_shift((111_139, -111_139), 100, ), (-1.0, -1.0))
    #     assert_allclose(geoprocessing.calc_real_world_latlong_shift_from_px_shift((-111_139, -111_139), 100, ), (1.0, -1.0))

    # def test_abs_angle_calculation(self):
    #     self.assertEqual(geoprocessing.get_real_world_angle_angle_zero_north())


class ImageCuttingTests(unittest.TestCase):
    def test_calculate_center(self):
        self.assertEqual(img_cutting.calculate_center((400, 200)), (200, 100))
        self.assertEqual(img_cutting.calculate_center((703, 200)), (351, 100))
        self.assertEqual(img_cutting.calculate_center((923, 305)), (461, 152))

    def test_cut_to_shape(self):
        pass


class AnnotationsTests(unittest.TestCase):
    def test_box_sliced_detection(self):
        box = BBox([0.5, 0.5, 0.2, 0.2], "plastic", "yolo", 4000, 3000)
        vcuts, hcuts = ds_annotations.get_cut_locations(2, 1, (4000, 3000))
        self.assertTrue(ds_annotations.box_is_sliced(box, vcuts, hcuts))

    def test_cut_locations(self):
        self.assertEqual(ds_annotations.get_cut_locations(1, 2, (300, 300)), ([150], [100, 200]))
        self.assertEqual(ds_annotations.get_cut_locations(3, 2, (4000, 3000)), ([1000, 2000, 3000], [1000, 2000]))
        self.assertEqual(ds_annotations.get_cut_locations(2, 1, (733, 357)), ([244, 488], [178]))

    def test_box_locator(self):
        self.assertEqual(ds_annotations.get_box_location(BBox([0.2, 0.2, 0.1, 0.12], "plastic", "yolo", 5472, 3648), 2, 1), (0, 0))
        self.assertEqual(ds_annotations.get_box_location(BBox([0.5, 0.2, 0.1, 0.12], "plastic", "yolo", 5472, 3648), 2, 1), (0, 1))
        self.assertEqual(ds_annotations.get_box_location(BBox([0.5, 0.7, 0.1, 0.12], "plastic", "yolo", 5472, 3648), 2, 1), (1, 1))
        self.assertEqual(ds_annotations.get_box_location(BBox([0.8, 0.7, 0.1, 0.12], "plastic", "yolo", 5472, 3648), 2, 1), (1, 2))

    def test_dict_creation(self):
        materials = ["trash", "pandas"]
        example_dict = {0: "trash", 1: "pandas"}
        self.assertEqual(ds_annotations.create_materials_dict(materials), example_dict)


class BBoxTests(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
