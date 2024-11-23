# Generated by Django 5.1.3 on 2024-11-23 02:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enderecos", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Logradouro",
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
                (
                    "nome",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Nome do Logradouro"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LogCor",
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
                ("dados", models.JSONField(verbose_name="Dados em formato JSON")),
                (
                    "logradouro",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="enderecos.logradouro",
                        verbose_name="Logradouro relacionado",
                    ),
                ),
            ],
        ),
    ]
