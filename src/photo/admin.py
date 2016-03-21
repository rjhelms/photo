from django.contrib import admin

from photo.models import FilmFormat, Manufacturer, Film, Developer, FilmRoll, \
    PhotoPaper, PhotoPaperFinish


class FilmAdmin(admin.ModelAdmin):
    list_display = ('film_short_name', 'manufacturer_short_name', 'speed',)
    list_filter = ('manufacturer__name', 'speed', 'formats', 'process')

    def film_short_name(self, obj):
        return ("%s %s" % (obj.manufacturer.short_name, obj.name))

    def manufacturer_short_name(self, obj):
        return obj.manufacturer.short_name

    film_short_name.admin_order_field = 'name'
    film_short_name.short_description = "Film"

    manufacturer_short_name.admin_order_field = 'manufacturer__short_name'
    manufacturer_short_name.short_description = "Manufacturer"

    ordering = ('manufacturer__short_name', 'name')

class FilmRollAdmin(admin.ModelAdmin):
    list_display = ('name', 'film', 'format', 'shot_date', 'developed_date')
    list_filter = ('film', 'format', 'shot_date', 'developed_date',)
    prepopulated_fields = {'developed_speed': ('shot_speed',)}

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['photographer'] = request.user
        return initial

# Register your models here.
admin.site.register(FilmFormat)
admin.site.register(Manufacturer)
admin.site.register(Film, FilmAdmin)
admin.site.register(Developer)
admin.site.register(FilmRoll, FilmRollAdmin)
admin.site.register(PhotoPaper)
admin.site.register(PhotoPaperFinish)
