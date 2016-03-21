from django.contrib import admin

from photo.models import FilmFormat, Manufacturer, Film


# Register your models here.
admin.site.register(FilmFormat)
admin.site.register(Manufacturer)
admin.site.register(Film)
