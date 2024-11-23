from django.db import models

class Comarca(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Comarca")
    
    def __str__(self):
        return f"ID: {self.id} - Nome da Comarca: {self.nome}"

class Municipio(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Município")
    comarca = models.ForeignKey(Comarca, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Comarca")

    def __str__(self):
        return f"Id: {self.id} - {self.nome} (Comarca: {self.comarca.nome})"
    
class Logradouro(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Logradouro")
    cidade = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Cidade relacionada")

    def __str__(self):
        return self.nome

class LogCor(models.Model):
    logradouro = models.ForeignKey(Logradouro, on_delete=models.CASCADE, verbose_name="Logradouro relacionado")
    dados = models.JSONField(verbose_name="Dados em formato JSON")

    def __str__(self):
        return f"LogCor ID: {self.id} - Logradouro: {self.logradouro.nome}"