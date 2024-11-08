from django.urls import path
from .views import *

urlpatterns = [
    path('denuncias/', lista_denuncias, name='lista_denuncias'),
    path('profile/', user_profile, name='user_profile'),
]