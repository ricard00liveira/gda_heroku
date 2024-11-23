from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError("O CPF é obrigatório")
        if not email:
            raise ValueError("O e-mail é obrigatório")
        
        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(cpf, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    TIPOS_USUARIO = [
        ('comum', 'Comum'),
        ('operador', 'Operador'),
        ('adm', 'Administrador'),
    ]

    cpf = models.CharField(max_length=11, primary_key=True, unique=True, verbose_name="CPF")
    email = models.EmailField(unique=True, verbose_name="Email")
    nome = models.CharField(max_length=150, verbose_name="Nome")
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='comum', verbose_name="Tipo de Usuário")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['email', 'nome', 'tipo_usuario']

    def __str__(self):
        return f"{self.nome} - ({self.tipo_usuario})"
