from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['cpf', 'email', 'nome', 'telefone', 'tipo_usuario', 'is_active', 'is_staff', 'self_registration']
        read_only_fields = ['is_active', 'is_staff']
