from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from enderecos.models import Municipio
from enderecos.models import Logradouro
from usuarios.models import User
from fatosesub.models import Fato, Subfato

class Denuncia(models.Model):
    numero = models.AutoField(primary_key=True)
    denunciante = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Denunciante",
        related_name='denunciante_denuncias'
    )
    anonima = models.BooleanField(default=False, verbose_name="Denúncia anônima")
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    endereco = models.ForeignKey(
        Logradouro, on_delete=models.SET_NULL,
        null=True,
        verbose_name="Endereço relacionado",
        related_name='logradouro_denuncias'
    )
    nr_endereco = models.CharField(
        max_length=10, verbose_name="Numeral", blank=True, null=True)
    ponto_referencia = models.CharField(
        max_length=255, verbose_name="Ponto de Referência", blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('analise', 'Em análise'), ('fila', 'Aguardando atendimento'), (
        'concluida', 'Atendimento concluído'), ('negada', 'Denúncia rejeitada')], default='analise')
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Município relacionado",
        related_name='denuncias'
    )
    fato = models.ForeignKey(
        Fato,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Fato relacionado",
        related_name='fato_denuncias'
    )
    subfato = models.ForeignKey(
        Subfato,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Subfato relacionado",
        related_name='subfato_denuncias'
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Usuário responsável",
        related_name='responsavel_denuncias'
    )
    is_deleted = models.BooleanField(default=False, verbose_name="Deletado")
    infrator = models.CharField(
        max_length=255, verbose_name="Infrator", blank=True, null=True)
    
    prioridade = models.CharField(
    max_length=20,
    choices=[('baixa', 'Baixa'), ('media', 'Média'), ('alta', 'Alta'), ('urgente', 'Urgente')],
    default='baixa',
    verbose_name="Prioridade"
)
    localizacao = models.JSONField(
        verbose_name="Coordenada geográfica (GeoJSON)",
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Denuncia {self.numero} - {self.municipio}'
    
class StatusHistorico(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='historico_status')
    status = models.CharField(max_length=20)
    data_alteracao = models.DateTimeField(auto_now_add=True)

class Anexo(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='anexos/')
    descricao = models.CharField(max_length=255, blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)