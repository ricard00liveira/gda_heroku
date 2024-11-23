from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'email', 'nome', 'tipo_usuario', 'is_active', 'is_staff')