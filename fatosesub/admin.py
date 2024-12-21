from django.contrib import admin
from .models import Fato, Subfato


@admin.register(Fato)
class FatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(Subfato)
class SubfatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'fato')
    search_fields = ('nome', 'fato__nome')
    list_filter = ('fato',)
    ordering = ('nome',)
