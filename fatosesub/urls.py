from django.urls import path
from .views import *

urlpatterns = [
    # Fatos
    path('fatos/', listar_fatos, name='listar_fatos'),
    path('fatos/create/', criar_fato, name='criar_fato'),
    path('fatos/<int:fato_id>/', visualizar_fato, name='visualizar_fato'),
    path('fatos/<int:fato_id>/update/', atualizar_fato, name='atualizar_fato'),
    path('fatos/<int:fato_id>/delete/', deletar_fato, name='deletar_fato'),

    # Subfatos
    path('fatos/<int:fato_id>/subfatos/', listar_subfatos, name='listar_subfatos'),
    path('fatos/<int:fato_id>/subfatos/create/', criar_subfato, name='criar_subfato'),
    path('subfatos/<int:subfato_id>/', visualizar_subfato, name='visualizar_subfato'),
    path('subfatos/<int:subfato_id>/update/', atualizar_subfato, name='atualizar_subfato'),
    path('subfatos/<int:subfato_id>/delete/', deletar_subfato, name='deletar_subfato'),
]
