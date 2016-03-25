"""
Django models for the photo application.

Models:
    :model:`photo.Developer`: a film developer
    :model:`photo.Enlarger`: a photographic enlarger
    :model:`photo.Film`: a type of film
    :model:`photo.FilmFormat`: a film format
    :model:`photo.FilmRoll`: an individual roll of film
    :model:`photo.Frame`: a frame on a film roll
    :model:`photo.Manufacturer`: a manufacturer of photo products
    :model:`photo.PhotoPaper`: a type of photo paper
    :model:`photo.PhotoPaperFinish`: a finish for photo paper, ie 
        glossy, matte
    :model:`photo.Print`: an individual print
"""
import uuid

from django.contrib import auth
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import CharField

from .utils import UploadToPathAndRename


# Create your models here.
class FilmFormat(models.Model):
    """
    Stores a film format.
    """
    name = models.CharField(max_length=50)
    roll_film = models.BooleanField()

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """
    Stores a manufacturer of photo products.
    """
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Film(models.Model):
    """
    Stores a type of film, related to :model:`photo.FilmFormat` and
    :model:`photo.Manufacturer`.
    """
    PROCESSES = (
        ("B&W", "black and white"),
        ("C41", "C-41"),
        ("E6", "E-6")
    )
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer)
    speed = models.IntegerField()
    formats = models.ManyToManyField(FilmFormat)
    process = CharField(max_length=3, choices=PROCESSES)

    class Meta:
        """Meta class for :model:`photo.Film`."""
        ordering = ('manufacturer__short_name', 'name')

    def __str__(self):
        return "{} {}".format(self.manufacturer.short_name, self.name)

class Developer(models.Model):
    """
    Stores a film developer, related to :model:`photo.Manufacturer`.
    """
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer)
    powder = models.BooleanField()

    def __str__(self):
        return "{} {}".format(self.manufacturer.short_name, self.name)

class FilmRoll(models.Model):
    """
    Stores an individual roll of film, related to :model:`photo.Film`,
    :model:`photo.FilmFormat`, :model:`photo.Developer` and :model:`auth.User`.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, db_index=True)
    film = models.ForeignKey(Film)
    format = models.ForeignKey(FilmFormat)
    developer = models.ForeignKey(Developer, blank=True, null=True)
    shot_speed = models.PositiveIntegerField(blank=True)
    developed_speed = models.PositiveIntegerField(blank=True)
    shot_date = models.DateField(blank=True, null=True)
    developed_date = models.DateField(blank=True, null=True)
    photographer = models.ForeignKey(auth.models.User, blank=True, null=True)
    contact_sheet = models.ImageField(blank=True,
                                      upload_to=UploadToPathAndRename
                                      ('contacts'))

    def clean(self):
        """
        Sets shot_speed and developed_speed if they are not already specified.
        """
        if self.shot_speed is None:
            self.shot_speed = self._base_speed()
        if self.developed_speed is None:
            self.developed_speed = self.shot_speed

    def __str__(self):
        return self.name

    def _base_speed(self):
        return self.film.speed

class PhotoPaperFinish(models.Model):
    """
    Stores a type of finish for photo paper.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class PhotoPaper(models.Model):
    """
    Stores a type of photo paper, related to :model:'photo.Manufacturer' and
    :model:`photo.PhotoPaperFinish`.
    """
    PAPER_TYPE_CHOICES = (
        ('RC', "resin-coated"),
        ('FB', "fibre-based",)
    )

    GRADE_CHOICES = (
        (-1, "00"),
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"))

    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer)
    paper_type = models.CharField(max_length=2, choices=PAPER_TYPE_CHOICES)
    multigrade = models.BooleanField()
    grade = models.IntegerField(choices=GRADE_CHOICES, blank=True, null=True)
    finishes = models.ManyToManyField(PhotoPaperFinish)

    def clean(self):
        """
        Validates a photo paper by ensuring that multigrade papers do not have
        a grade set, and graded papers do.
        """
        if self.multigrade is True:
            if self.grade is not None:
                raise ValidationError("Multigrade papers can not have a "
                                      " grade specified")
        else:
            if self.grade is None:
                raise ValidationError("Graded papers must have a grade "
                                      "specified")

    def __str__(self):
        return "{} {}".format(self.manufacturer.short_name, self.name)

class Frame(models.Model):
    """
    Stores an individual negative, related to :model:`photo.FilmRoll`.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.SmallIntegerField()
    film_roll = models.ForeignKey(FilmRoll)
    description = models.TextField(blank=True)
    scan = models.ImageField(blank=True,
                             upload_to=UploadToPathAndRename('frames'))

    class Meta:
        """
        Meta class for :model:`photo.Frame`
        """
        ordering = ('film_roll__name', 'index')
        unique_together = ('index', 'film_roll')

    def frame_number(self):
        """
        Converts the index into a string representing what would be printed on
        the film. This is needed to handle frame 00.
        """
        if self.index == -1:
            return "00"
        else:
            return str(self.index)

    def __str__(self):
        return "{}-{}".format(self.film_roll.name, self.frame_number())

class Enlarger(models.Model):
    """
    Stores a model of enlarger, related to :model:`photo.FilmFormat`.
    """
    TYPE_CHOICES = (
        (0, "Condenser"),
        (1, "Diffuser"),
    )
    name = models.CharField(max_length=100)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    color_head = models.BooleanField()
    formats = models.ManyToManyField(FilmFormat)

    def __str__(self):
        return self.name

class Print(models.Model):
    """
    Stores an individual print, related to :model:`photo.Enlarger`,
    :model:`photo.Frame`, :model:`photo.PhotoPaper` and 
    :model:`photo.PhotoPaperFinish.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    sequence = models.SmallIntegerField()
    frame = models.ForeignKey(Frame)
    paper = models.ForeignKey(PhotoPaper)
    finish = models.ForeignKey(PhotoPaperFinish)
    scan = models.ImageField(blank=True,
                             upload_to=UploadToPathAndRename('prints'))
    enlarger = models.ForeignKey(Enlarger, blank=True, null=True)

    def clean(self):
        """
        Validates that the selected paper finish is valid for the selected
        paper.
        """
        if self.finish not in self.paper.finishes.all():
            raise ValidationError("Invalid combination of paper and finish.")
        if self.enlarger is not None:
            if self.frame.film_roll.format not in self.enlarger.formats.all():
                raise ValidationError("Invalid combination of negative and "
                                      "enlarger")
    class Meta:
        """Metadata for :model:`photo.Print`"""
        ordering = ('date', 'sequence')
        unique_together = ('date', 'sequence')

    def __str__(self):
        return "{:%Y%m%d}-{}".format(self.date, self.sequence)

