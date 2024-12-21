from rest_framework import serializers
from .models import Fato, Subfato

class FatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fato
        fields = ['id', 'nome']

class SubfatoSerializer(serializers.ModelSerializer):
    fato = serializers.PrimaryKeyRelatedField(queryset=Fato.objects.all())

    class Meta:
        model = Subfato
        fields = ['id', 'nome', 'fato']
