from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('denuncias/', lista_denuncias, name='lista_denuncias'),
    path('denuncias/create', views.criar_denuncia, name='criar_denuncia'),
    path('denuncias/<int:denuncia_id>/read/', views.read_denuncia, name='read_denuncia'),
    path('denuncias/<int:denuncia_id>/update/', views.editar_denuncia, name='editar_denuncia'),
    path('denuncias/<int:denuncia_id>/delete/', views.delete_denuncia, name='delete_denuncia'),

]