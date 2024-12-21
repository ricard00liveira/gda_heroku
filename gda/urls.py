from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls), # ADMIN
    path('api/', include('denuncias.urls')),  # rota Denuncias
    path('api/', include('enderecos.urls')), # Rota Enderecos
    path('api/', include('usuarios.urls')), # Rota Usuarios
    path('api/', include('fatosesub.urls')), # Rota Fatos e Subfatos
    # TOKEN
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]