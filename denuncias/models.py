from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from enderecos.models import Municipio
from enderecos.models import Logradouro
from usuarios.models import User
from fatosesub.models import Fato, Subfato
from django.contrib.gis.db import models as gis_models
import uuid
import os
from django.core.validators import FileExtensionValidator


class Denuncia(models.Model):
    numero = models.AutoField(primary_key=True)
    denunciante = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Denunciante",
        related_name="denunciante_denuncias",
    )
    anonima = models.BooleanField(default=False, verbose_name="Denúncia anônima")
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    endereco = models.ForeignKey(
        Logradouro,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Endereço relacionado",
        related_name="logradouro_denuncias",
    )
    bairro = models.CharField(
        max_length=255, verbose_name="Bairro", blank=True, null=True
    )
    nr_endereco = models.CharField(
        max_length=10, verbose_name="Numeral", blank=True, null=True
    )
    ponto_referencia = models.CharField(
        max_length=255, verbose_name="Ponto de Referência", blank=True, null=True
    )
    STATUS_CHOICES = [
        ("analise", "Em análise"),
        ("fila", "Aguardando atendimento"),
        ("atendimento", "Em atendimento"),
        ("concluida", "Atendimento concluído"),
        ("negada", "Denúncia rejeitada"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="analise",
        db_index=True,
        verbose_name="Status da denúncia",
    )
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Município relacionado",
        related_name="denuncias",
    )
    fato = models.ForeignKey(
        Fato,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Fato relacionado",
        related_name="fato_denuncias",
    )
    subfato = models.ForeignKey(
        Subfato,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Subfato relacionado",
        related_name="subfato_denuncias",
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuário responsável",
        related_name="responsavel_denuncias",
    )
    is_deleted = models.BooleanField(default=False, verbose_name="Deletado")
    infrator = models.CharField(
        max_length=255, verbose_name="Infrator", blank=True, null=True
    )

    prioridade = models.CharField(
        max_length=20,
        choices=[
            ("baixa", "Baixa"),
            ("media", "Média"),
            ("alta", "Alta"),
            ("urgente", "Urgente"),
        ],
        default="baixa",
        verbose_name="Prioridade",
    )
    localizacao = gis_models.PointField(
        geography=True,
        verbose_name="Localização geográfica (latitude/longitude)",
        null=True,
        blank=True,
    )
    aprovada = models.BooleanField(
        default=False, db_index=True, verbose_name="Aprovada por autoridade"
    )
    denuncia_ref = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referencias",
        verbose_name="Denúncia relacionada",
    )

    def __str__(self):
        return f"Denuncia {self.numero} - {self.municipio}"


class StatusHistorico(models.Model):
    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name="historico_status",
        verbose_name="Denúncia",
    )
    status = models.CharField(
        max_length=20, choices=Denuncia.STATUS_CHOICES, verbose_name="Status"
    )
    data_alteracao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data da alteração"
    )

    class Meta:
        ordering = ["-data_alteracao"]

    def __str__(self):
        return (
            f"Status {self.status} em {self.data_alteracao.strftime('%d/%m/%Y %H:%M')}"
        )


def anexo_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    nome = f"{uuid.uuid4().hex}{ext}"
    return f"anexos/denuncia_{instance.denuncia.numero}/{nome}"


class Anexo(models.Model):
    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name="anexos",
        verbose_name="Denúncia",
    )
    arquivo = models.FileField(
        upload_to=anexo_upload_path,
        verbose_name="Arquivo",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "mp4"])
        ],
    )
    descricao = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Descrição"
    )
    data_upload = models.DateTimeField(auto_now_add=True, verbose_name="Data do envio")

    class Meta:
        ordering = ["-data_upload"]

    def __str__(self):
        return f"Anexo {self.id} da denúncia {self.denuncia.numero}"
