from django.urls import path
from . import views
from .views import *    
urlpatterns = [
    path('profile/', user_profile, name='user_profile'),
    
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path('usuarios/create/', criar_usuario, name='criar_usuario'),
    path('usuarios/<str:cpf>/read/', visualizar_usuario, name='visualizar_usuario'),
    path('usuarios/<str:cpf>/update/', atualizar_usuario, name='atualizar_usuario'),
    path('usuarios/<str:cpf>/delete/', deletar_usuario, name='deletar_usuario'),
]