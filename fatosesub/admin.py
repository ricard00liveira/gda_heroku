from django.contrib import admin
from .models import Fato, Subfato


@admin.register(Fato)
class FatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')  # Exibe o ID e o nome do Fato na listagem
    search_fields = ('nome',)  # Permite busca pelo nome do Fato
    ordering = ('nome',)  # Ordena os Fatos alfabeticamente


@admin.register(Subfato)
class SubfatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'fato')  # Exibe o ID, nome e Fato relacionado na listagem
    search_fields = ('nome', 'fato__nome')  # Permite busca pelo nome do Subfato e do Fato relacionado
    list_filter = ('fato',)  # Adiciona um filtro por Fato
    ordering = ('nome',)  # Ordena os Subfatos alfabeticamente
