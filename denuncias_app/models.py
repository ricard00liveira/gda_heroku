from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError("O CPF é obrigatório")
        if not email:
            raise ValueError("O email é obrigatório")
        
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
        return f"{self.nome} ({self.tipo_usuario})"
    

class Municipio(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Município")
    comarca = models.CharField(max_length=100, verbose_name="Comarca")

    def __str__(self):
        return f"{self.nome} - Comarca: {self.comarca}"
    
class Denuncia(models.Model):
    numero = models.AutoField(primary_key=True)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Resolvido', 'Resolvido')], default='Pendente')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Município relacionado")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário")

    def __str__(self):
        return f'Denuncia {self.numero} - {self.municipio}'