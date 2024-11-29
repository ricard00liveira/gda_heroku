from django.contrib import admin
from .models import *

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'comarca')
    search_fields = ('nome', 'comarca')

@admin.register(Comarca)
class ComarcaAdmin(admin.ModelAdmin):
    list_display = ('id','nome',)
    search_fields = ('nome',)

@admin.register(Logradouro)
class LogradouroAdmin(admin.ModelAdmin):
    list_display = ('id','nome','cidade')
    search_fields = ('nome', )
    
@admin.register(LogCor)
class LogCorAdmin(admin.ModelAdmin):
    list_display = ('id','logradouro')
    search_fields = ('logradouro__nome',)