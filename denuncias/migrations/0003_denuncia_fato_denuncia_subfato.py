# Generated by Django 5.1.3 on 2024-12-15 01:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("denuncias", "0002_remove_denuncia_usuario_denuncia_denunciante_and_more"),
        ("fatosesub", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="denuncia",
            name="fato",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="fato_denuncias",
                to="fatosesub.fato",
                verbose_name="Fato relacionado",
            ),
        ),
        migrations.AddField(
            model_name="denuncia",
            name="subfato",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="subfato_denuncias",
                to="fatosesub.subfato",
                verbose_name="Subfato relacionado",
            ),
        ),
    ]
