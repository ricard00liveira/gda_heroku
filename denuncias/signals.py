from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from enderecos.models import Logradouro, Municipio
from usuarios.models import User
from .models import Denuncia
from fatosesub.models import Fato, Subfato


@receiver(pre_delete, sender=User)
def set_denunciante_name_on_delete(sender, instance, **kwargs):
    denuncias = Denuncia.objects.filter(denunciante=instance)

    for denuncia in denuncias:
        denuncia.denunciante = instance.nome
        denuncia.save()


@receiver(pre_delete, sender=Logradouro)
def set_endereco_name_on_delete(sender, instance, **kwargs):
    denuncias = Denuncia.objects.filter(endereco=instance)

    for denuncia in denuncias:
        denuncia.endereco = instance.nome
        denuncia.save()


@receiver(pre_delete, sender=Municipio)
def set_municipio_name_on_delete(sender, instance, **kwargs):
    denuncias = Denuncia.objects.filter(municipio=instance)

    for denuncia in denuncias:
        denuncia.municipio = instance.nome
        denuncia.save()


@receiver(pre_delete, sender=get_user_model())
def set_responsavel_name_on_delete(sender, instance, **kwargs):
    denuncias = Denuncia.objects.filter(responsavel=instance)

    for denuncia in denuncias:
        denuncia.responsavel = instance.nome
        denuncia.save()


@receiver(pre_delete, sender=Fato)
def set_fato_name_on_delete(sender, instance, **kwargs):
    denuncias = Denuncia.objects.filter(fato=instance)

    for denuncia in denuncias:
        denuncia.fato = instance.nome
        denuncia.save()


@receiver(pre_delete, sender=Subfato)
def set_subfato_name_on_delete(sender, instance, **kwargs):
    denuncias = Denuncia.objects.filter(subfato=instance)

    for denuncia in denuncias:
        denuncia.subfato = instance.nome
        denuncia.save()
