# Generated by Django 5.1.3 on 2024-12-15 23:51

from django.db import models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("denuncias", "0003_denuncia_fato_denuncia_subfato"),
    ]

    operations = [
        migrations.AddField(
            model_name="denuncia",
            name="anonima",
            field=models.BooleanField(default=False, verbose_name="Denúncia anônima"),
        ),
        migrations.AddField(
            model_name="denuncia",
            name="localizacao",
            field=models.JSONField(
                blank=True, null=True, verbose_name="Coordenada geográfica"
            ),
        ),
        migrations.AddField(
            model_name="denuncia",
            name="prioridade",
            field=models.CharField(
                choices=[
                    ("baixa", "Baixa"),
                    ("media", "Média"),
                    ("alta", "Alta"),
                    ("urgente", "Urgente"),
                ],
                default="baixa",
                max_length=20,
                verbose_name="Prioridade",
            ),
        ),
        migrations.CreateModel(
            name="Anexo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("arquivo", models.FileField(upload_to="anexos/")),
                ("descricao", models.CharField(blank=True, max_length=255, null=True)),
                ("data_upload", models.DateTimeField(auto_now_add=True)),
                (
                    "denuncia",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="anexos",
                        to="denuncias.denuncia",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StatusHistorico",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.CharField(max_length=20)),
                ("data_alteracao", models.DateTimeField(auto_now_add=True)),
                (
                    "denuncia",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="historico_status",
                        to="denuncias.denuncia",
                    ),
                ),
            ],
        ),
    ]
