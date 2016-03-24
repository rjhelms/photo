"""
Admin classes for photo application
"""

from django.contrib import admin

from photo.models import FilmFormat, Manufacturer, Film, Developer, FilmRoll, \
    PhotoPaper, PhotoPaperFinish, Negative


class FilmAdmin(admin.ModelAdmin):
    """
    Admin class for :model:`photo.Film`
    """
    list_display = ('film_short_name', 'manufacturer_short_name', 'speed',)
    list_filter = ('manufacturer', 'speed', 'formats', 'process')

    def film_short_name(self, obj):
        """Short name of film, for display in admin lists."""
        return "%s %s" % (obj.manufacturer.short_name, obj.name)

    def manufacturer_short_name(self, obj):
        """Short name of film manufacturer, for display in admin lists."""
        return obj.manufacturer.short_name

    film_short_name.admin_order_field = 'name'
    film_short_name.short_description = "Film"

    manufacturer_short_name.admin_order_field = 'manufacturer__short_name'
    manufacturer_short_name.short_description = "Manufacturer"

    ordering = ('manufacturer__short_name', 'name')

class FilmRollAdmin(admin.ModelAdmin):
    """
    Admin class for :model:`photo.FilmRoll`
    """
    list_display = ('name', 'film', 'format', 'shot_date', 'developed_date')
    list_filter = ('film', 'format', 'shot_date', 'developed_date',)
    prepopulated_fields = {'developed_speed': ('shot_speed',)}

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['photographer'] = request.user
        return initial

class PhotoPaperAdmin(admin.ModelAdmin):
    """
    Admin class for :model:`photo.PhotoPaper`
    """
    list_display = ('name', 'manufacturer_short_name', 'multigrade', 'grade')
    list_filter = ('manufacturer', 'multigrade',)
    def paper_short_name(self, obj):
        """Short name of photo paper, for display in admin lists."""
        return "%s %s" % (obj.manufacturer.short_name, obj.name)

    def manufacturer_short_name(self, obj):
        """
        Short name of photo paper manufacturer, for display in admin lists.
        """
        return obj.manufacturer.short_name

    manufacturer_short_name.admin_order_field = 'manufacturer__short_name'
    manufacturer_short_name.short_description = "Manufacturer"

    ordering = ('manufacturer__short_name', 'name')

class NegativeAdmin(admin.ModelAdmin):
    """
    Admin class for :model:`photo.Negative`
    """
    list_display = ('film_roll', 'index', )
    list_filter = ('film_roll', 'film_roll__format', 'film_roll__film',
                   'film_roll__shot_date', 'film_roll__developed_date')
    ordering = ('film_roll', 'index')

# Register your models here.
admin.site.register(FilmFormat)
admin.site.register(Manufacturer)
admin.site.register(Film, FilmAdmin)
admin.site.register(Developer)
admin.site.register(FilmRoll, FilmRollAdmin)
admin.site.register(PhotoPaper, PhotoPaperAdmin)
admin.site.register(PhotoPaperFinish)
admin.site.register(Negative, NegativeAdmin)
