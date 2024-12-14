from django.db import models


class Fato(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Subfato(models.Model):
    nome = models.CharField(max_length=255)
    fato = models.ForeignKey(
        Fato, on_delete=models.CASCADE, related_name='subfatos_fatos')

    def __str__(self):
        return self.nome
