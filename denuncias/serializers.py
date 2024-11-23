from rest_framework import serializers
from .models import Denuncia
from enderecos.models import Municipio, Comarca
from enderecos.serializers import MunicipioSerializer

class DenunciaSerializer(serializers.ModelSerializer):
    municipio = serializers.PrimaryKeyRelatedField(queryset=Municipio.objects.all())
    descricao = serializers.CharField(error_messages={'required': 'Descrição é obrigatória!', 'blank': 'A descrição não pode estar em branco.'})
    
    class Meta:
        model = Denuncia
        fields = '__all__'

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