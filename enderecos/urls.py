from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('municipios/', lista_municipios, name='lista_municipios'),
    path('municipios/create', criar_municipio, name='criar_municipio'),
]