from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="Description",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),  # ADMIN
    path("api/", include("denuncias.urls")),  # Rota Denuncias
    path("api/", include("enderecos.urls")),  # Rota Enderecos
    path("api/", include("usuarios.urls")),  # Rota Usuarios
    path("api/", include("fatosesub.urls")),  # Rota Fatos e Subfatos
    # TOKEN
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # SWAGGER
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]
