"""
Django models for the photo application.

Models:
    :model:`photo.Developer`: a film developer
    :model:`photo.Film`: a type of film
    :model:`photo.FilmFormat`: a film format
    :model:`photo.FilmRoll`: an individual roll of film
    :model:`photo.Manufacturer`: a manufacturer of photo products
    :model:`photo.PhotoPaper`: a type of photo paper
    :model:`photo.PhotoPaperFinish`: a finish for photo paper, ie glossy, matte
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
                             upload_to=UploadToPathAndRename('negatives'))

    def clean(self):
        """
        Validates that a frame's index is unique for its FilmRoll.
        """
        if self.film_roll is None:
            raise ValidationError("Film roll is mandatory.")

        existing_frames = Frame.objects.filter(film_roll=self.film_roll)
        for item in existing_frames:
            if (item.id != self.id) & (item.index == self.index):
                raise ValidationError("Index must be unique for each frame "
                                      "on a roll.")

    class Meta:
        """
        Meta class for :model:`photo.Frame`
        """
        ordering = ('film_roll__name', 'index')

    def frame_number(self):
        if self.index >= 0:
            return str(self.index)
        elif self.index == -1:
            return "00"

    def __str__(self):
        return "{}-{}".format(self.film_roll.name, self.index)
