from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('denuncias/', lista_denuncias, name='lista_denuncias'),
    path('denuncias/create', views.criar_denuncia, name='criar_denuncia'),
    path('denuncias/read/<int:denuncia_id>', views.read_denuncia, name='read_denuncia'),
    path('denuncias/update/<int:denuncia_id>', views.editar_denuncia, name='editar_denuncia'),
    path('denuncias/delete/<int:denuncia_id>', views.delete_denuncia, name='delete_denuncia'),


    path('municipios/', lista_municipios, name='lista_municipios'),
    path('municipios/create', criar_municipio, name='criar_municipio'),
    
    path('profile/', user_profile, name='user_profile'),
]