from django.urls import path
from .views import *

urlpatterns = [
    path('denuncias/', lista_denuncias, name='lista_denuncias'),
    path('ver_denuncias/', view_lista_denuncias, name='view_lista_denuncias'),
    path('profile/', user_profile, name='user_profile'),
]