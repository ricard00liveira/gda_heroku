from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from enderecos.models import Municipio
   
class Denuncia(models.Model):
    numero = models.AutoField(primary_key=True)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Resolvido', 'Resolvido')], default='Pendente')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Município relacionado")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário")

    def __str__(self):
        return f'Denuncia {self.numero} - {self.municipio}'