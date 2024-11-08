from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('denuncias/', lista_denuncias, name='lista_denuncias'),
    path('denuncias/create', views.criar_denuncia, name='criar_denuncia'),
    path('denuncias/delete/<int:denuncia_id>/', views.delete_denuncia, name='delete_denuncia'),
    path('municipios/', lista_municipios, name='lista_municipios'),
    path('profile/', user_profile, name='user_profile'),
]