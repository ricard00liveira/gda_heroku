from rest_framework import serializers
from .models import Denuncia, Municipio

class DenunciaSerializer(serializers.ModelSerializer):
    municipio = serializers.PrimaryKeyRelatedField(queryset=Municipio.objects.all())
    descricao = serializers.CharField(error_messages={'required': 'Descrição é obrigatória!', 'blank': 'A descrição não pode estar em branco.'})
    class Meta:
        model = Denuncia
        fields = ['numero', 'descricao', 'data', 'status', 'municipio', 'usuario']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Verifica o tipo do usuário no request
        request = self.context.get('request')
        if request and request.user.tipo_usuario not in ['adm', 'operador']:
            representation.pop('data', None)
            representation.pop('usuario', None)
        return representation
    
    def validate_descricao(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("A descrição deve ter pelo menos 10 caracteres.")
        return value

    def create(self, validated_data):
        return Denuncia.objects.create(**validated_data)

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