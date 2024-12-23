from django.urls import path
from .views.municipio_views import *
from .views.logradouro_views import *
from .views.comarca_views import *

urlpatterns = [
    path('municipios/', lista_municipios, name='lista_municipios'),
    path('municipios/create/', criar_municipio, name='criar_municipio'),
    path('municipios/<int:municipio_id>/read/', visualizar_municipio, name='visualizar_municipio'),
    path('municipios/<int:municipio_id>/update/', atualizar_municipio, name='atualizar_municipio'),
    path('municipios/<int:municipio_id>/delete/', deletar_municipio, name='deletar_municipio'),
    
    path('comarcas/', listar_comarcas, name='listar_comarcas'),
    path('comarcas/create/', criar_comarca, name='criar_comarca'),
    path('comarcas/<int:comarca_id>/read/', visualizar_comarca, name='visualizar_comarca'),
    path('comarcas/<int:comarca_id>/update/', atualizar_comarca, name='atualizar_comarca'),
    path('comarcas/<int:comarca_id>/delete/', deletar_comarca, name='deletar_comarca'),

    path('logradouros/<int:municipio_id>/', listar_logradouros, name='listar_logradouros'),
    path('logradouros/<int:municipio_id>/create/', criar_logradouro, name='criar_logradouro'),
    path('logradouros/<int:logradouro_id>/read/', visualizar_logradouro, name='visualizar_logradouro'),
    path('logradouros/<int:logradouro_id>/update/', atualizar_logradouro, name='atualizar_logradouro'),
    path('logradouros/<int:logradouro_id>/delete/', deletar_logradouro, name='deletar_logradouro'),

]