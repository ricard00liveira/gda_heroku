from rest_framework import serializers
from .models import Fato, Subfato


class FatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fato
        fields = ["id", "nome"]

    def validate_nome(self, value):
        if self.instance:
            if Fato.objects.filter(nome=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    f"Já existe um fato com o nome '{value}'."
                )
        else:
            if Fato.objects.filter(nome=value).exists():
                raise serializers.ValidationError(
                    f"Já existe um fato com o nome '{value}'."
                )
        return value


class SubfatoSerializer(serializers.ModelSerializer):
    fato = serializers.PrimaryKeyRelatedField(queryset=Fato.objects.all())

    class Meta:
        model = Subfato
        fields = ["id", "nome", "fato"]

    def validate(self, data):
        nome = data.get("nome")
        fato = data.get("fato")
        if self.instance:
            if (
                Subfato.objects.filter(nome=nome, fato=fato)
                .exclude(id=self.instance.id)
                .exists()
            ):
                raise serializers.ValidationError(
                    {
                        "nome": f"Já existe um subfato com o nome '{nome}' para esse fato."
                    }
                )
        else:
            if Subfato.objects.filter(nome=nome, fato=fato).exists():
                raise serializers.ValidationError(
                    {
                        "nome": f"Já existe um subfato com o nome '{nome}' para esse fato."
                    }
                )
        return data
