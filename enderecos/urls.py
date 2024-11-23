from django.urls import path
from .views.municipio_views import *
from .views.logradouro_views import *

urlpatterns = [
    path('municipios/', lista_municipios, name='lista_municipios'),
    path('municipios/create', criar_municipio, name='criar_municipio'),
    
    path('municipios/logradouro', lista_logradouros, name='lista_logradouros'),
]