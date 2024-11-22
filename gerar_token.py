import os
import django
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken

# Configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gda.settings')  # Caminho para o settings.py
settings.configure()
django.setup()

# Gera um token de acesso
token = AccessToken()
token.set_exp(from_time=None, lifetime=timedelta(days=1))

print("Token:", str(token))
print("Expiração:", token.payload['exp'])
