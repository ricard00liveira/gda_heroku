import os
from decouple import config

from django.test import TestCase
from django.urls import reverse

class SettingsTestCase(TestCase):
    def test_secret_key(self):
        secret_key = config('SECRET_KEY')
        self.assertIsNotNone(secret_key)
        self.assertIsInstance(secret_key, str)

    def test_debug_mode(self):
        debug_mode = config('DEBUG', default=True, cast=bool)
        self.assertIsNotNone(debug_mode)
        self.assertIsInstance(debug_mode, bool)

    def test_allowed_hosts(self):
        allowed_hosts = config("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")
        self.assertIsNotNone(allowed_hosts)
        self.assertIsInstance(allowed_hosts, list)
        self.assertGreater(len(allowed_hosts), 0)

    def test_installed_apps(self):
        installed_apps = [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            'rest_framework',
            'corsheaders',
            'usuarios',
            'denuncias',
            'enderecos',
            'fatosesub',
        ]
        self.assertIsNotNone(installed_apps)
        self.assertIsInstance(installed_apps, list)
        self.assertGreater(len(installed_apps), 0)

    def test_cors_allowed_origins(self):
        cors_allowed_origins = config(
            "CORS_ALLOWED_ORIGINS",
            default="http://localhost:3000,https://gda-front.netlify.app,https://gda-app.xyz,https://back.gda-app.xyz"
        ).split(",")
        self.assertIsNotNone(cors_allowed_origins)
        self.assertIsInstance(cors_allowed_origins, list)
        self.assertGreater(len(cors_allowed_origins), 0)

    def test_database_settings(self):
        database_settings = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='gda_app'),
            'USER': config('DB_USER', default='usuario'),
            'PASSWORD': config('DB_PASSWORD', default='1234'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
        self.assertIsNotNone(database_settings)
        self.assertIsInstance(database_settings, dict)
        self.assertGreater(len(database_settings), 0)

    def test_static_url(self):
        static_url = 'static/'
        self.assertIsNotNone(static_url)
        self.assertIsInstance(static_url, str)

    def test_static_root(self):
        static_root = BASE_DIR / 'staticfiles'
        self.assertIsNotNone(static_root)
        self.assertIsInstance(static_root, str)

    def test_simple_jwt_settings(self):
        simple_jwt_settings = {
            'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
            'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
            'ROTATE_REFRESH_TOKENS': False,
            'BLACKLIST_AFTER_ROTATION': True,
            'ALGORITHM': 'HS256',
            'SIGNING_KEY': SECRET_KEY,
            'AUTH_HEADER_TYPES': ('Bearer',),
        }
        self.assertIsNotNone(simple_jwt_settings)
        self.assertIsInstance(simple_jwt_settings, dict)
        self.assertGreater(len(simple_jwt_settings), 0)