"""
Tests for models in the photo application.
"""
from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from photo import models


# Model tests
class FilmFormatTestCase(TestCase):
    """
    Tests for :model:`photo.FilmFormat`
    """
    def test_str(self):
        """
        Test the __str__ method on :model:`photo.FilmFormat`
        """
        test_format = models.FilmFormat(name="test film_format",
                                        roll_film=True)
        self.assertEqual(str(test_format), "test film_format",
                         "FilmFormat.__str__ returned unexpected value.")

class ManufacturerTestCase(TestCase):
    """
    Tests for :model:`photo.Manufacturer`
    """
    def test_str(self):
        """
        Test the __str__ method on :model:`photo.Manufacturer`
        """
        test_manufacturer = models.Manufacturer(name="test manufacturer")
        self.assertEqual(str(test_manufacturer), "test manufacturer",
                         "Manufacturer.__str__ returned unexpected value.")

class FilmTestCase(TestCase):
    """
    Tests for :model:`photo.Film`
    """
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = models.Manufacturer.objects.create(
            name="test manufacturer", short_name="test")

    def test_str(self):
        """
        Test the __str__ method on :model:`photo.Film`
        """
        test_film = models.Film(name="test film",
                                manufacturer=self.manufacturer)
        self.assertEqual(str(test_film), "test test film",
                         "Film.__str__ returned unexpected value.")

class DeveloperTestCase(TestCase):
    """
    Tests for :model:`photo.Developer`
    """
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = models.Manufacturer.objects.create(
            name="test manufacturer", short_name="test")

    def test_str(self):
        """
        Test the __str__ method on :model:`photo.Developer`
        """
        test_developer = models.Developer(name="test developer",
                                          manufacturer=self.manufacturer)
        self.assertEqual(str(test_developer), "test test developer",
                         "Developer.__str__ returned unexpected value.")

class FilmRollTestCase(TestCase):
    """
    Tests for :model:`photo.FilmRoll`
    """
    @classmethod
    def setUpTestData(cls):
        manufacturer = models.Manufacturer.objects.create(
            name="test manufacturer", short_name="test")
        cls.film = models.Film.objects.create(name="test film",
                                              manufacturer=manufacturer,
                                              speed=200, process="B&W")

    def test_clean_neither(self):
        """
        Test the clean method on :model:`photo.FilmRoll`, in the case where
        neither shot_speed or developed_speed are provided.
        """
        test_film_roll = models.FilmRoll(name="test film_roll",
                                         film=self.film)
        test_film_roll.clean()

        self.assertEqual(test_film_roll.shot_speed, self.film.speed,
                         "shot_speed set incorrectly")
        self.assertEqual(test_film_roll.developed_speed, self.film.speed,
                         "developed_speed set incorrectly")

    def test_clean_only_shot_speed(self):
        """
        Test the clean method on :model:`photo.FilmRoll`, in the case where
        only shot_speed is provided.
        """
        test_film_roll = models.FilmRoll(name="test film_roll",
                                         film=self.film,
                                         shot_speed=400)
        test_film_roll.clean()
        self.assertEqual(test_film_roll.shot_speed, 400,
                         "shot_speed set incorrectly")
        self.assertEqual(test_film_roll.developed_speed, 400,
                         "developed_speed set incorrectly")

    def test_clean_only_developed(self):
        """
        Test the clean method on :model:`photo.FilmRoll`, in the case where
        only developed_speed is provided.
        """
        test_film_roll = models.FilmRoll(name="test film_roll",
                                         film=self.film,
                                         developed_speed=400)
        test_film_roll.clean()
        self.assertEqual(test_film_roll.shot_speed, self.film.speed,
                         "shot_speed set incorrectly")
        self.assertEqual(test_film_roll.developed_speed, 400,
                         "developed_speed set incorrectly")

    def test_clean_both(self):
        """
        Test the clean method on :model:`photo.FilmRoll`, in the case where
        both shot_speed and developed_speed are provided.
        """
        test_film_roll = models.FilmRoll(name="test film_roll",
                                         film=self.film,
                                         shot_speed=320,
                                         developed_speed=400)
        test_film_roll.clean()
        self.assertEqual(test_film_roll.shot_speed, 320,
                         "shot_speed set incorrectly")
        self.assertEqual(test_film_roll.developed_speed, 400,
                         "developed_speed set incorrectly")

    def test_str(self):
        """
        Test the __str__ method on :model:`photo.FilmRoll`
        """
        test_film_roll = models.FilmRoll(name="test film_roll")
        self.assertEqual(str(test_film_roll), "test film_roll",
                         "FilmRoll.__str__ returned unexpected value.")

class PhotoPaperFinishTestCase(TestCase):
    """
    Tests for :model:`photo.PhotoPaperFinish`
    """
    def test_str(self):
        """
        Test the __str__ method on :model:`photo.PhotoPaperFinish`
        """
        test_photo_paper_finish = (models.PhotoPaperFinish
                                   (name="test photo_paper_finish"))
        self.assertEqual(str(test_photo_paper_finish),
                         "test photo_paper_finish",
                         "PhotoPaperFinish.__str__ returned unexpected value.")

class PhotoPaperTestCase(TestCase):
    """
    Tests for :model:`photo.PhotoPaper`
    """
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = models.Manufacturer.objects.create(
            name="test manufacturer", short_name="test")

    def test_clean_multigrade_valid(self):
        """
        Test PhotoPaper.clean, for valid multigrade paper
        """
        test_photo_paper = models.PhotoPaper(name="test photo_paper",
                                             multigrade=True)
        try:
            test_photo_paper.clean()
        except ValidationError:
            self.fail("Valid PhotoPaper raised ValidationError")

    def test_clean_multigrade_invalid(self):
        """
        Test PhotoPaper.clean, for invalid multigrade paper
        """
        test_photo_paper = models.PhotoPaper(name="test photo_paper",
                                             multigrade=True,
                                             grade=2)
        self.assertRaises(ValidationError, test_photo_paper.clean)


    def test_clean_graded_valid(self):
        """
        Test PhotoPaper.clean, for valid graded paper
        """
        test_photo_paper = models.PhotoPaper(name="test photo_paper",
                                             multigrade=False,
                                             grade=2)
        try:
            test_photo_paper.clean()
        except ValidationError:
            self.fail("Valid PhotoPaper raised ValidationError")

    def test_clean_graded_invalid(self):
        """
        Test PhotoPaper.clean, for invalid graded paper
        """
        test_photo_paper = models.PhotoPaper(name="test photo_paper",
                                             multigrade=False)
        self.assertRaises(ValidationError, test_photo_paper.clean)

    def test_str(self):
        """
        Test the __str__ method on :model:`photo.PhotoPaper`
        """
        test_photo_paper = models.PhotoPaper(name="test photo_paper",
                                             manufacturer=self.manufacturer)
        self.assertEqual(str(test_photo_paper), "test test photo_paper",
                         "PhotoPaper.__str__ returned unexpected value.")

class FrameTestCase(TestCase):
    """
    Tests for :model:`photo.Frame`
    """
    @classmethod
    def setUpTestData(cls):
        manufacturer = models.Manufacturer.objects.create(
            name="test manufacturer", short_name="test")
        film = models.Film.objects.create(name="test film",
                                          manufacturer=manufacturer,
                                          speed=200, process="B&W")
        film_format = models.FilmFormat.objects.create(name="test format",
                                                       roll_film=True)
        cls.film_roll = models.FilmRoll.objects.create(name="test film_roll",
                                                       film=film,
                                                       format=film_format,
                                                       shot_speed=200,
                                                       developed_speed=200)

    def test_frame_number_positive(self):
        """
        Test Frame.frame_number handles positive indexes
        """
        test_frame = models.Frame(index=1)
        self.assertEqual(test_frame.frame_number(), "1",
                         "Incorrect frame number returned")

    def test_frame_number_double_zero(self):
        """
        Test Frame.frame_Number handles double-zero index
        """
        test_frame = models.Frame(index=-1)
        self.assertEqual(test_frame.frame_number(), "00",
                         "Incorrect frame number returned")

    def test_str(self):
        """
        Test the __str__ method on :model:`photo.Frame`
        """
        test_frame = models.Frame(index=0, film_roll=self.film_roll)
        self.assertEqual(str(test_frame), "test film_roll-0",
                         "Frame.__str__ returned unexpected value.")

class PrintTestCase(TestCase):
    """
    Tests for :model:`photo.Print`
    """
    @classmethod
    def setUpTestData(cls):
        manufacturer = models.Manufacturer.objects.create(name="manufacturer",
                                                          short_name="test")
        cls.finish_glossy = models.PhotoPaperFinish.objects.create(name=
                                                                   "glossy")
        cls.finish_matte = models.PhotoPaperFinish.objects.create(name=
                                                                  "matte")
        cls.photo_paper = models.PhotoPaper.objects.create(
            name="photo_paper", manufacturer=manufacturer, paper_type="RC",
            multigrade=True)

        cls.photo_paper.finishes.add(cls.finish_glossy)
        cls.photo_paper.save()

        cls.film_format_35mm = models.FilmFormat.objects.create(name="35mm",
                                                                roll_film=True)
        cls.film_format_120 = models.FilmFormat.objects.create(name="120",
                                                               roll_film=True)

        film = models.Film.objects.create(name="film",
                                          manufacturer=manufacturer,
                                          speed=200)
        film.formats.add(cls.film_format_35mm)
        film.formats.add(cls.film_format_120)
        film.save()

        cls.film_roll_120 = models.FilmRoll.objects.create(
            name="film_roll_120", film=film, format=cls.film_format_120,
            shot_speed=200, developed_speed=200)
        cls.frame_120 = models.Frame.objects.create(
            index=1, film_roll=cls.film_roll_120)

        cls.film_roll_35mm = models.FilmRoll.objects.create(
            name="film_roll_35mm", film=film, format=cls.film_format_35mm,
            shot_speed=200, developed_speed=200)
        cls.frame_35mm = models.Frame.objects.create(
            index=1, film_roll=cls.film_roll_35mm)

        cls.enlarger = models.Enlarger.objects.create(name="enlarger", type=0,
                                                      color_head=False)
        cls.enlarger.formats.add(cls.film_format_35mm)
        cls.enlarger.save()

    def test_clean_valid_finish(self):
        """
        Test Print.clean, for valid combination of paper and finish.
        """
        test_print = models.Print(paper=self.photo_paper,
                                  finish=self.finish_glossy)
        try:
            test_print.clean()
        except ValidationError:
            self.fail("Valid Print raised ValidationError")

    def test_clean_invalid_finish(self):
        """
        Test Print.clean, for invalid combination of paper and finish.
        """
        test_print = models.Print(paper=self.photo_paper,
                                  finish=self.finish_matte)
        self.assertRaises(ValidationError, test_print.clean)

    def test_clean_valid_enlarger(self):
        """
        Test Print.clean, for valid combination of format and enlarger.
        """
        test_print = models.Print(paper=self.photo_paper,
                                  finish=self.finish_glossy,
                                  frame=self.frame_35mm,
                                  enlarger=self.enlarger)
        try:
            test_print.clean()
        except ValidationError:
            self.fail("Valid Print raised ValidationError")

    def test_clean_invalid_enlarger(self):
        """
        Test Print.clean, for invalid combination of format and enlarger.
        """
        test_print = models.Print(paper=self.photo_paper,
                                  finish=self.finish_glossy,
                                  frame=self.frame_120,
                                  enlarger=self.enlarger)
        self.assertRaises(ValidationError, test_print.clean)

    def test_str(self):
        """
        Test the __str__ method on :model:`photo.Print`
        """
        test_print = models.Print(date=date(2012, 2, 2), sequence=1)
        self.assertEqual(str(test_print), "20120202-1",
                         "Print.__str__ returned unexpected value.")

class EnlargerTestCase(TestCase):
    """
    Tests for :model:`photo.Enlarger`
    """
    def test_str(self):
        """
        Test the __str__ method on :model:`photo.Enlarger`
        """
        test_enlarger = models.Enlarger(name="test enlarger")
        self.assertEqual(str(test_enlarger), "test enlarger",
                         "Enlarger.__str__ return unexpected value.")
