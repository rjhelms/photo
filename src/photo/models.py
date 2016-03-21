from django.db import models

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
    
