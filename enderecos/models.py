from django.db import models

class Comarca(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Comarca")
    
    def __str__(self):
        return self.nome

class Municipio(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Município")
    comarca = models.ForeignKey(Comarca, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Comarca")

    def __str__(self):
        return f"{self.nome} (Comarca: {self.comarca.nome})"