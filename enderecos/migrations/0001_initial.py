# Generated by Django 5.1.3 on 2024-11-23 01:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comarca",
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
                        max_length=100, unique=True, verbose_name="Nome da Comarca"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Municipio",
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
                        max_length=100, unique=True, verbose_name="Nome do Município"
                    ),
                ),
                (
                    "comarca",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="enderecos.comarca",
                        verbose_name="Comarca",
                    ),
                ),
            ],
        ),
    ]
