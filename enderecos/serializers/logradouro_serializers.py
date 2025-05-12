from rest_framework import serializers
from ..models import Logradouro


class LogradouroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logradouro
        fields = "__all__"

    def validate_nome(self, value):
        return value.upper().strip()

    def validate(self, attrs):
        nome = attrs.get("nome")
        cidade = attrs.get("cidade")

        if nome and cidade:
            queryset = Logradouro.objects.filter(nome=nome.upper(), cidade=cidade)

            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)

            if queryset.exists():
                raise serializers.ValidationError(
                    {"nome": "Já existe um logradouro com este nome neste município."}
                )

        return attrs
