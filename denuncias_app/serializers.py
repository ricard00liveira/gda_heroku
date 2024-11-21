from rest_framework import serializers
from .models import Denuncia, Municipio

class DenunciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denuncia
        fields = '__all__'

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

    def validate_nome(self, value):
        if Municipio.objects.filter(nome=value).exists():
            raise serializers.ValidationError(f"Já existe um município com o nome '{value}'.")
        return value

    def validate_comarca(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("O campo 'comarca' não pode estar vazio.")
        return value

    def validate(self, data):
        if 'Cidade' in data.get('nome', '') or 'Estado' in data.get('comarca', ''):
            raise serializers.ValidationError("A combinação 'Cidade' ou 'Estado' não é permitida.")
        return data