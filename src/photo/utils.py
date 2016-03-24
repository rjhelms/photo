'''
Utility classes and functions for the photo application
'''

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
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)
