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
