from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['cpf', 'email', 'nome', 'telefone', 'tipo_usuario', 'password']

    def create(self, validated_data):
        # Remove o password dos dados validados e usa o método `create_user` do modelo
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
