from django.urls import path
from . import views
from .views import *    
urlpatterns = [
    path('profile/', user_profile, name='user_profile'),
]