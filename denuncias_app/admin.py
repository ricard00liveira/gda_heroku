from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'email', 'nome', 'tipo_usuario', 'is_active', 'is_staff')
    
@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'descricao', 'data', 'status', 'municipio', 'usuario')
    search_fields = ('numero', 'descricao', 'municipio__nome', 'usuario__cpf')
    list_filter = ('status', 'municipio')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'comarca')
    search_fields = ('nome', 'comarca')