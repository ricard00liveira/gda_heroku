from django.contrib import admin
from .models import *
    
@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'descricao', 'data', 'status', 'municipio', 'usuario')
    search_fields = ('numero', 'descricao', 'municipio__nome', 'usuario__cpf')
    list_filter = ('status', 'municipio')