from django.db import models
from django.contrib import auth

# Create your models here.
class FilmFormat(models.Model):
    name = models.CharField(max_length=50)
    roll_film = models.BooleanField()

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Film(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer)
    speed = models.IntegerField()
    formats = models.ManyToManyField(FilmFormat)

    def __str__(self):
        return "{} {}".format(self.manufacturer.short_name, self.name)

class Developer(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer)
    powder = models.BooleanField()

    def __str__(self):
        return "{} {}".format(self.manufacturer.short_name, self.name)

class FilmRoll(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    film = models.ForeignKey(Film)
    format = models.ForeignKey(FilmFormat)
    developer = models.ForeignKey(Developer, blank=True, null=True)
    shot_speed = models.PositiveIntegerField()
    developed_speed = models.PositiveIntegerField()
    shot_date = models.DateField(blank=True, null=True)
    developed_date = models.DateField(blank=True, null=True)
    photographer = models.ForeignKey(auth.models.User, blank=True, null=True)
    
    def __str__(self):
        return self.name

    def _base_speed(self):
        return self.film.speed
    