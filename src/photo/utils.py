'''
Utility classes and functions for the photo application
'''

import math
import os
import uuid

from django.utils.deconstruct import deconstructible


@deconstructible
# pylint: disable=too-few-public-methods
class UploadToPathAndRename(object):
    """
    Helper class for renaming files to a uuid on upload.

    For user-supplied files, file names should be obfuscated by using this
    class for the upload_to parameter. This will match the primary key of the
    parent object if it exists, or generate a new uuid if it does not.
    """

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            if isinstance(instance.pk, uuid.UUID):
                filename = '{}.{}'.format(instance.pk, ext)
            else:
                raise TypeError("UploadToPathAndRename should only be called "
                                "for objects with UUID primary keys.")
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)

class StopTimeConversion(object):
    """Class for time and stop conversion methods."""

    @staticmethod
    def time_difference_in_stops(time_1, time_2):
        """
        Convert a difference in expose times to stops.

        Args:
            time_1: the base time
            time_2: the new time
        """

        if time_1 <= 0 or time_2 <= 0:
            raise ValueError("Times must be greater than 0.")

        ratio = time_2 / time_1
        return math.log2(ratio)

    @staticmethod
    def time_difference_in_points(time_1, time_2):
        """
        Convert a difference in exposure times to printer points.
        A printer's point is 1/12 of a stop.

        Args:
            time_1: the base time
            time_2: the new time
        """

        return StopTimeConversion.time_difference_in_stops(
            time_1, time_2) * 12

    @staticmethod
    def stop_difference_to_multiplier(stops):
        """
        Convert a stop difference to a time multiplier.

        Args:
            stops: the difference in stops.
        """

        return 2 ** stops

    @staticmethod
    def point_difference_to_multiplier(points):
        """
        Convert a points difference to a time multiplier.

        Args:
            points: the difference in printer's points.
        """
        return StopTimeConversion.stop_difference_to_multiplier(points / 12)

    @staticmethod
    def adjust_time_by_stops(base_time, stops):
        """
        Adjust a given exposure time by a difference in stops.

        Args:
            base_time: the base exposure time to modify.
            stops: the change in exposure, in stops.
        """
        if base_time <= 0:
            raise ValueError("Base time must be greater than 0.")

        multiplier = StopTimeConversion.stop_difference_to_multiplier(stops)
        return base_time * multiplier

    @staticmethod
    def adjust_time_by_points(base_time, points):
        """
        Adjust a given exposure time by a difference in points.

        Args:
            base_time: the base exposure time to modify.
            points: the change in exposure, in points.
        """
        if base_time <= 0:
            raise ValueError("Base time must be greater than 0.")

        multiplier = StopTimeConversion.point_difference_to_multiplier(
            points)
        return base_time * multiplier

    @staticmethod
    def resize_print_in_stops(old_size, new_size):
        """
        Calculates exposure adjustment, in stops, needed to resize a print.

        Args:
            old_size: a dictionary, containing x and y for old print size.
            new_size: a dictionary, containing x and y for new print size.
        """
        old_aspect = old_size['x'] / old_size['y']
        new_aspect = new_size['x'] / new_size['y']

        aspect_difference = old_aspect - new_aspect
        if aspect_difference == 0:
            constant_aspect_new_size = {
                'x':new_size['x'],
                'y':new_size['y']}
            # print("Prints same aspect ratio")
        elif aspect_difference < 0:
            # print("new print higher aspect ratio")
            constant_aspect_new_size = {
                'x':new_size['x'],
                'y':old_size['y'] * new_size['x'] / old_size['x']}
            # print("treating new print as {0}x{1}".format(
            #    constant_aspect_new_size['x'],
            #    constant_aspect_new_size['y']))
        else:
            # print("new print lower aspect ratio")
            constant_aspect_new_size = {
                'x':old_size['x'] * new_size['y'] / old_size['y'],
                'y':new_size['y']}
            # print("treating new print as {0}x{1}".format(
            #    constant_aspect_new_size['x'],
            #    constant_aspect_new_size['y']))
        old_area = old_size['x'] * old_size['y']
        new_area = constant_aspect_new_size['x'] * constant_aspect_new_size['y']
        size_ratio = new_area / old_area
        return math.log2(size_ratio)

# old_print = {"x":3,"y":6}
# new_print = {"x":6,"y":12}
# stop_adjust = StopTimeConversion.resize_print_in_stops(old_print, new_print)
# print(stop_adjust)
