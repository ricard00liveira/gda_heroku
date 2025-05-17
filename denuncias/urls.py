from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("denuncias/", views.lista_denuncias, name="lista_denuncias"),
    path("denuncias/create/", views.criar_denuncia, name="criar_denuncia"),
    path(
        "denuncias/<int:denuncia_id>/read/", views.read_denuncia, name="read_denuncia"
    ),
    path(
        "denuncias/<int:denuncia_id>/update/",
        views.editar_denuncia,
        name="editar_denuncia",
    ),
    path(
        "denuncias/<int:denuncia_id>/delete/",
        views.delete_denuncia,
        name="delete_denuncia",
    ),
    # EndPoint Denúncia Anônima
    path(
        "denuncias/anonima/",
        views.criar_denuncia_anonima,
        name="criar_denuncia_anonima",
    ),
    # Upload anexos
    path("denuncias/anexos/upload/", views.upload_anexo, name="upload_anexo"),
    # Transcrição de áudio
    path("denuncias/transcrever-audio/", transcrever_audio, name="transcrever-audio"),
]
