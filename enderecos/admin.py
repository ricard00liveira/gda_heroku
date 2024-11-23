from django.contrib import admin
from .models import *

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'comarca')
    search_fields = ('nome', 'comarca')

@admin.register(Comarca)
class ComarcaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
