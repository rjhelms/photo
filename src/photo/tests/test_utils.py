# pylint: disable=invalid-name
"""
Tests for photo.utils
"""
import uuid

from django.test import TestCase

from photo import utils


# pylint: disable=too-few-public-methods
class DummyInstance:
    """
    Dummy instance object for passing into UploadToPathAndRename
    """
    pk = None

class UploadToPathAndRenameTestCase(TestCase):
    """
    Tests for utils.UploadToPathAndRename
    """
    def setUp(self):
        self.upload_to_path_and_rename = utils.UploadToPathAndRename('test')
        self.instance = DummyInstance()

    def test_extension_preserved(self):
        """
        Verify that UploadToPathAndRename preserves file extensions.
        """
        result = self.upload_to_path_and_rename(self.instance, "filename.jpg")
        ext = result.split('.')[-1]
        self.assertEqual(ext, 'jpg', "New filename has wrong extension")

    def test_path_appended(self):
        """
        Verify that UploadToPathAndRename appends specified path.
        """
        result = self.upload_to_path_and_rename(self.instance, "filename.jpg")
        path = result.split('/')[0]
        self.assertEqual(path, 'test', "New filename has wrong path")

    def test_instance_with_no_pk(self):
        """
        Verify handling when instance does not have a primary key
        """
        result = self.upload_to_path_and_rename(self.instance, "filename.jpg")
        generated_uuid_string = result.split('/')[1].split('.')[0]
        generated_uuid = uuid.UUID(generated_uuid_string, version=4)
        self.assertNotEqual(generated_uuid, self.instance.pk,
                            "New filename did not get a random UUID")

    def test_instance_with_uuid_pk(self):
        """
        Verify handling when instance has a UUID primary key
        """
        self.instance.pk = uuid.uuid4()
        result = self.upload_to_path_and_rename(self.instance, "filename.jpg")
        generated_uuid_string = result.split('/')[1].split('.')[0]
        generated_uuid = uuid.UUID(generated_uuid_string, version=4)
        self.assertEqual(generated_uuid, self.instance.pk,
                         "New filename does not match UUID of instance")

    def test_insance_with_non_uuid_pk(self):
        """
        Verify handling when instance has a non-UUID primary key
        """
        self.instance.pk = "test"
        with self.assertRaises(TypeError):
            self.upload_to_path_and_rename(self.instance, "filename.jpg")

class StopTimeConversionTestCase(TestCase):
    """Tests for utils.StopTimeConversion."""
    def test_exception_time_difference_in_stops(self):
        """
        Verify exception for invalid values in
        StopTimeConversion.time_difference_in_stops.
        """
        with self.assertRaises(ValueError):
            utils.StopTimeConversion.time_difference_in_stops(0, 1)
        with self.assertRaises(ValueError):
            utils.StopTimeConversion.time_difference_in_stops(1, 0)
        with self.assertRaises(ValueError):
            utils.StopTimeConversion.time_difference_in_stops(0, 0)
        with self.assertRaises(ValueError):
            utils.StopTimeConversion.time_difference_in_stops(-1, -1)

    def test_exception_adjust_time_by_points(self):
        """
        Verify exception for invalid values in
        StopTimeConversion.adjust_time_by_points.
        """
        with self.assertRaises(ValueError):
            utils.StopTimeConversion.adjust_time_by_points(0, 1)
        with self.assertRaises(ValueError):
            utils.StopTimeConversion.adjust_time_by_points(-1, 1)

    def test_exception_adjust_time_by_stops(self):
        """
        Verify exception for invalid values in
        StopTimeConversion.adjust_time_by_stops.
        """
        with self.assertRaises(ValueError):
            utils.StopTimeConversion.adjust_time_by_stops(0, 1)
        with self.assertRaises(ValueError):
            utils.StopTimeConversion.adjust_time_by_stops(-1, 1)

    def test_time_difference_in_stops(self):
        """
        Verify values returned by
        StopTimeConversion.time_difference_in_stops.
        """
        self.assertEqual(
            utils.StopTimeConversion.time_difference_in_stops(6, 12), 1)
        self.assertEqual(
            utils.StopTimeConversion.time_difference_in_stops(12, 12), 0)
        self.assertEqual(
            utils.StopTimeConversion.time_difference_in_stops(12, 6), -1)

    def test_time_difference_in_points(self):
        """
        Verify values returned by
        StopTimeConversion.time_difference_in_points.
        """
        self.assertEqual(
            utils.StopTimeConversion.time_difference_in_points(6, 12), 12)
        self.assertEqual(
            utils.StopTimeConversion.time_difference_in_points(12, 12), 0)
        self.assertEqual(
            utils.StopTimeConversion.time_difference_in_points(12, 6), -12)

    def test_stop_difference_to_multiplier(self):
        """
        Verify values returned by
        StopTimeConversion.stop_difference_to_multiplier.
        """
        self.assertEqual(
            utils.StopTimeConversion.stop_difference_to_multiplier(1), 2)
        self.assertEqual(
            utils.StopTimeConversion.stop_difference_to_multiplier(0), 1)
        self.assertEqual(
            utils.StopTimeConversion.stop_difference_to_multiplier(-1), 0.5)

    def test_point_difference_to_multiplier(self):
        """
        Verify values returned by
        StopTimeConversion.point_difference_to_multiplier.
        """
        self.assertEqual(
            utils.StopTimeConversion.point_difference_to_multiplier(12), 2)
        self.assertEqual(
            utils.StopTimeConversion.point_difference_to_multiplier(0), 1)
        self.assertEqual(
            utils.StopTimeConversion.point_difference_to_multiplier(-12), 0.5)

    def test_adjust_time_by_stops(self):
        """
        Verify values returned by
        StopTimeConversion.adjust_time_by_stops.
        """
        self.assertEqual(
            utils.StopTimeConversion.adjust_time_by_stops(12, 1), 24)
        self.assertEqual(
            utils.StopTimeConversion.adjust_time_by_stops(12, 0), 12)
        self.assertEqual(
            utils.StopTimeConversion.adjust_time_by_stops(12, -1), 6)

    def test_adjust_time_by_points(self):
        """
        Verify values returned by
        StopTimeConversion.adjust_time_by_points.
        """
        self.assertEqual(
            utils.StopTimeConversion.adjust_time_by_points(12, 12), 24)
        self.assertEqual(
            utils.StopTimeConversion.adjust_time_by_points(12, 0), 12)
        self.assertEqual(
            utils.StopTimeConversion.adjust_time_by_points(12, -12), 6)

    def test_resize_print_enlarge(self):
        """
        Verify values returned by StopTimeConversion.resize_print,
        for a constant-aspect enlargement.
        """
        old_print = {'x':4, 'y':6}
        new_print = {'x':8, 'y':12}
        self.assertEqual(
            utils.StopTimeConversion.resize_print_in_stops(
                old_print, new_print),
            2)

    def test_resize_print_same(self):
        """
        Verify values returned by StopTimeConversion.resize_print,
        for a constant-aspect print of same size.
        """
        old_print = {'x':4, 'y':6}
        new_print = {'x':4, 'y':6}
        self.assertEqual(
            utils.StopTimeConversion.resize_print_in_stops(
                old_print, new_print),
            0)

    def test_resize_print_reduce(self):
        """
        Verify values returned by StopTimeConversion.resize_print,
        for a constant-aspect reduction.
        """
        old_print = {'x':8, 'y':12}
        new_print = {'x':4, 'y':6}
        self.assertEqual(
            utils.StopTimeConversion.resize_print_in_stops(
                old_print, new_print),
            - 2)

    def test_resize_print_enlarge_high_aspect(self):
        """
        Verify values returned by StopTimeConversion.resize_print,
        for a higher-aspect ratio enlargement.
        """
        old_print = {'x':4, 'y':6}
        new_print = {'x':8, 'y':10}
        self.assertEqual(
            utils.StopTimeConversion.resize_print_in_stops(
                old_print, new_print),
            2)

    def test_resize_print_same_high_aspect(self):
        """
        Verify values returned by StopTimeConversion.resize_print,
        for a higher-aspect ratio print of same size.
        """
        old_print = {'x':4, 'y':6}
        new_print = {'x':4, 'y':5}
        self.assertEqual(
            utils.StopTimeConversion.resize_print_in_stops(
                old_print, new_print),
            0)

    def test_resize_print_reduce_high_aspect(self):
        """
        Verify values returned by StopTimeConversion.resize_print,
        for a higher-aspect ratio reduction.
        """
        old_print = {'x':8, 'y':12}
        new_print = {'x':4, 'y':5}
        self.assertEqual(
            utils.StopTimeConversion.resize_print_in_stops(
                old_print, new_print),
            - 2)

    def test_resize_print_enlarge_low_aspect(self):
        """
        Verify values returned by StopTimeConversion.resize_print,
        for a lower-aspect ratio enlargement.
        """
        old_print = {'x':4, 'y':6}
        new_print = {'x':7, 'y':12}
        self.assertEqual(
            utils.StopTimeConversion.resize_print_in_stops(
                old_print, new_print),
            2)

    def test_resize_print_same_low_aspect(self):
        """
        Verify values returned by StopTimeConversion.resize_print,
        for a lower-aspect ratio print of same size.
        """
        old_print = {'x':4, 'y':6}
        new_print = {'x':3, 'y':6}
        self.assertEqual(
            utils.StopTimeConversion.resize_print_in_stops(
                old_print, new_print),
            0)

    def test_resize_print_reduce_low_aspect(self):
        """
        Verify values returned by StopTimeConversion.resize_print,
        for a higher-aspect ratio reduction.
        """
        old_print = {'x':8, 'y':12}
        new_print = {'x':3, 'y':6}
        self.assertEqual(
            utils.StopTimeConversion.resize_print_in_stops(
                old_print, new_print),
            - 2)
