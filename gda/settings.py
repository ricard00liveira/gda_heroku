# gda/settings.py
from pathlib import Path
import os
from decouple import config, Csv
import django_heroku
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STORAGES = {
    "default": {
        "BACKEND": config(
            "DEFAULT_FILE_STORAGE", default="storages.backends.s3boto3.S3Boto3Storage"
        ),
    },
    "staticfiles": {
        "BACKEND": config(
            "STATICFILES_STORAGE_BACKEND",
            default="storages.backends.s3boto3.S3Boto3Storage",
        ),
    },
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# --- DEBUG agora controlado por variável de ambiente ---
# Defina DEBUG=False em produção (Heroku) e DEBUG=True localmente no seu .env
DEBUG = config("DEBUG", default=False, cast=bool)

# --- ALLOWED_HOSTS (Preservado o seu método, configure DJANGO_ALLOWED_HOSTS no Heroku) ---
# Ex: DJANGO_ALLOWED_HOSTS="back.gda-app.xyz,gda-app-644eb108e04c.herokuapp.com"
# Para desenvolvimento local, "localhost,127.0.0.1" são adicionados se DJANGO_ALLOWED_HOSTS não estiver definido ou DEBUG=True.
_default_allowed_hosts = "back.gda-app.xyz,gda-app-644eb108e04c.herokuapp.com"
if DEBUG:
    _default_allowed_hosts = "localhost,127.0.0.1,[::1]," + _default_allowed_hosts

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default=_default_allowed_hosts).split(
    ","
)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    # Novos (do seu arquivo original)
    "django_extensions",
    "rest_framework",
    "rest_framework_gis",
    "corsheaders",
    "usuarios",
    "denuncias",
    "enderecos",
    "fatosesub",
    "storages",  # Para o S3 AWS
    "drf_yasg",  # Para Swagger/OpenAPI (se não estava, adicione se for usar as URLs do seu gda/urls.py)
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise ainda é útil para servir arquivos que não vão para S3 ou em dev.
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- Configurações de CORS ---
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://gda-app.xyz",
]

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=Csv(),
    default=[
        "http://localhost:8080,http://127.0.0.1:8080,https://gda-app.xyz,https://back.gda-app.xyz,https://gda-app-644eb108e04c.herokuapp.com",
    ],
)


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

ROOT_URLCONF = "gda.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gda.wsgi.application"


DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=config(
            "DB_SSL_REQUIRE", default=not DEBUG, cast=bool
        ),  # SSL obrigatório em prod, opcional em dev
    )
}

APPEND_SLASH = False

# Password validation (Preservado)
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")  #
TIME_ZONE = config("TIME_ZONE", default="UTC")  #
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# S3 para staticfiles (via STORAGES), STATICFILES_STORAGE aponta para S3.
# WhiteNoise ainda pode servir arquivos localmente em DEBUG ou arquivos não gerenciados pelo S3.
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# A configuração de STORAGES["staticfiles"] geralmente sobrepõe esta,
# mas defina explicitamente se S3 for o primário para estáticos.
STATICFILES_STORAGE = config(
    "STATICFILES_STORAGE",
    default=(
        "storages.backends.s3boto3.S3Boto3Storage"
        if not DEBUG
        else "whitenoise.storage.CompressedManifestStaticFilesStorage"
    ),
)

# Media files (S3 é o default storage, então MEDIA_URL e MEDIA_ROOT podem não ser usados se tudo for S3)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "usuarios.User"

# JWT
from rest_framework_simplejwt.settings import api_settings

api_settings.USER_ID_FIELD = "cpf"
api_settings.USER_ID_CLAIM = "cpf"

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", default=30, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("JWT_REFRESH_TOKEN_LIFETIME_DAYS", default=2, cast=int)
    ),
    "ROTATE_REFRESH_TOKENS": config(
        "JWT_ROTATE_REFRESH_TOKENS", default=False, cast=bool
    ),
    "BLACKLIST_AFTER_ROTATION": config(
        "JWT_BLACKLIST_AFTER_ROTATION", default=True, cast=bool
    ),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# AWS S3 (Preservado do seu arquivo original)
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default=None)
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default=None)
AWS_S3_ENDPOINT_URL = config(
    "AWS_S3_ENDPOINT_URL", default=None
)  # Adicionado para flexibilidade (ex: MinIO)
AWS_S3_CUSTOM_DOMAIN = config(
    "AWS_S3_CUSTOM_DOMAIN", default=None
)  # Se usar CloudFront/custom domain para S3
AWS_LOCATION = config("AWS_LOCATION", default="")

AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "public, max-age=31536000",
}
# Se for usar S3 para media files e static files:
if AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Email Configuration (Exemplo, ajuste conforme necessário)
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=not DEBUG, cast=bool)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # Essencial para Heroku
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=not DEBUG, cast=bool)
SESSION_COOKIE_HTTPONLY = config(
    "SESSION_COOKIE_HTTPONLY", default=True, cast=bool
)  # Default já é True
CSRF_COOKIE_HTTPONLY = config(
    "CSRF_COOKIE_HTTPONLY", default=False, cast=bool
)  # Default é False, mantenha se precisar ler via JS, senão True
SECURE_HSTS_SECONDS = config(
    "SECURE_HSTS_SECONDS", default=0 if DEBUG else 2592000, cast=int
)  # 30 dias para começar, aumente depois
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=not DEBUG, cast=bool
)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=not DEBUG, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = config(
    "SECURE_CONTENT_TYPE_NOSNIFF", default=not DEBUG, cast=bool
)
# SECURE_BROWSER_XSS_FILTER é obsoleto, mas não prejudica.
# X_FRAME_OPTIONS = 'DENY' # Já é o default do middleware

# Swagger
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Formato do Token: Bearer [seu_token_aqui]",
        }
    },
    "USE_SESSION_AUTH": False,
}

# --- Configuração django-heroku e GeoDjango (Preservada do seu arquivo original) ---
if "DATABASE_URL" in os.environ or config(
    "DJANGO_HEROKU_APPLY", default=not DEBUG, cast=bool
):  # Aplicar em prod
    # Configurações GeoDjango (bibliotecas devem estar instaladas no Heroku via buildpacks)
    GDAL_LIBRARY_PATH = config(
        "GDAL_LIBRARY_PATH", default=os.getenv("GDAL_LIBRARY_PATH")
    )
    GEOS_LIBRARY_PATH = config(
        "GEOS_LIBRARY_PATH", default=os.getenv("GEOS_LIBRARY_PATH")
    )

    django_heroku.settings(locals(), staticfiles=False)

    # Sobrescreve o engine do banco de dados para PostGIS se estiver usando GeoDjango
    if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
        DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"
