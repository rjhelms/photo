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
    pk = None  # pylint: disable=invalid-name

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
        self.instance.pk = uuid.uuid4()  # pylint: disable=invalid-name
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
