from rest_framework import serializers
from .models import Denuncia
from .models import Anexo
from enderecos.models import Municipio
from enderecos.serializers import MunicipioSerializer
from django.contrib.gis.geos import Point


class AnexoSerializer(serializers.ModelSerializer):
    arquivo_url = serializers.SerializerMethodField()

    class Meta:
        model = Anexo
        fields = [
            "id",
            "denuncia",
            "arquivo",
            "arquivo_url",
            "descricao",
            "data_upload",
        ]

    def get_arquivo_url(self, obj):
        return obj.arquivo.url if obj.arquivo else None


class DenunciaSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    municipio = serializers.PrimaryKeyRelatedField(queryset=Municipio.objects.all())
    anexos = AnexoSerializer(many=True, read_only=True)
    descricao = serializers.CharField(
        error_messages={
            "required": "Descrição é obrigatória!",
            "blank": "A descrição não pode estar em branco.",
        }
    )
    localizacao = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Denuncia
        fields = "__all__"
        read_only_fields = ["localizacao"]

    def get_localizacao(self, obj):
        if obj.localizacao:
            return {"latitude": obj.localizacao.y, "longitude": obj.localizacao.x}
        return None

    def create(self, validated_data):
        lat = validated_data.pop("latitude", None)
        lng = validated_data.pop("longitude", None)
        if lat is not None and lng is not None:
            validated_data["localizacao"] = Point(lng, lat)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        lat = validated_data.pop("latitude", None)
        lng = validated_data.pop("longitude", None)
        if lat is not None and lng is not None:
            validated_data["localizacao"] = Point(lng, lat)
        return super().update(instance, validated_data)

    def validate_descricao(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "A descrição deve ter pelo menos 10 caracteres."
            )
        return value
