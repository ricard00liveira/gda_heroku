from rest_framework import serializers
from .models import Municipio, Comarca

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Verifica o tipo do usuário no request
        request = self.context.get('request')
        if request and request.user.tipo_usuario not in ['adm']:
            representation.pop('comarca', None)
        return representation

    def validate_nome(self, value):
        if Municipio.objects.filter(nome=value).exists():
            raise serializers.ValidationError(f"Já existe um município com o nome '{value}'.")
        return value

    def validate_comarca(self, value):
        if not value:
            raise serializers.ValidationError("O campo 'comarca' não pode estar vazio.")
        if not Comarca.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(f"A comarca '{value.nome}' não existe.")
        return value
    
class ComarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comarca
        fields = '__all__'