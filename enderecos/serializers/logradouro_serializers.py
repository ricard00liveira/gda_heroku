from rest_framework import serializers
from ..models import Logradouro, LogCor
from rest_framework_gis.serializers import GeoFeatureModelSerializer


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


class LogCorGeoJSONSerializer(GeoFeatureModelSerializer):
    logradouro_nome = serializers.CharField(source="logradouro.nome", read_only=True)
    bairro = serializers.CharField(source="logradouro.bairro", read_only=True)
    cidade_id = serializers.IntegerField(source="logradouro.cidade.id", read_only=True)

    class Meta:
        model = LogCor
        geo_field = "trecho"
        fields = ("id", "logradouro_nome", "bairro", "cidade_id")
