from django.contrib import admin

from photo.models import FilmFormat, Manufacturer, Film, Developer, FilmRoll, \
    PhotoPaper, PhotoPaperFinish


class FilmRollAdmin(admin.ModelAdmin):
    list_display = ('name', 'film', 'format', 'shot_date',)
    list_filter = ('film', 'format', 'shot_date', 'developed_date',)
    prepopulated_fields = {'developed_speed': ('shot_speed',)}
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['photographer'] = request.user
        return initial

# Register your models here.
admin.site.register(FilmFormat)
admin.site.register(Manufacturer)
admin.site.register(Film)
admin.site.register(Developer)
admin.site.register(FilmRoll, FilmRollAdmin)
admin.site.register(PhotoPaper)
admin.site.register(PhotoPaperFinish)