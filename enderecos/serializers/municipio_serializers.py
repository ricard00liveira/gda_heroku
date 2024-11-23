from rest_framework import serializers
from ..models import Municipio, Comarca, Logradouro, LogCor

class MunicipioSerializer(serializers.ModelSerializer):
    arquivo = serializers.FileField(required=False, write_only=True)

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

    def validate(self, data):
        # Validar o arquivo JSON se for enviado
        arquivo = data.get('arquivo')
        if arquivo and not arquivo.name.endswith('.json'):
            raise serializers.ValidationError({'arquivo': 'O arquivo deve estar no formato JSON.'})
        return data

    def create(self, validated_data):
        # Extrair o arquivo JSON, se fornecido
        arquivo = validated_data.pop('arquivo', None)
        municipio = Municipio.objects.create(**validated_data)

        if arquivo:
            try:
                import json
                json_data = json.load(arquivo)
                self.processar_base_faces(json_data, municipio)
            except Exception as e:
                raise serializers.ValidationError({'arquivo': f'Erro ao processar o arquivo JSON: {str(e)}'})

        return municipio

    def processar_base_faces(self, json_data, municipio):
        logradouros_dict = {}

        for feature in json_data['features']:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {})

            tip_log = properties.get('NM_TIP_LOG')
            tit_log = properties.get('NM_TIT_LOG')
            log_name = properties.get('NM_LOG')
            name_parts = filter(None, [tip_log, tit_log, log_name])
            full_name = " ".join(name_parts)

            # Extrair coordenadas de início e fim
            coordinates = geometry.get('coordinates', [])
            if coordinates:
                coordenada_inicio = coordinates[0] if len(coordinates) > 0 else None
                coordenada_fim = coordinates[-1] if len(coordinates) > 1 else None

                if full_name and coordenada_inicio and coordenada_fim:
                    if full_name in logradouros_dict:
                        logradouros_dict[full_name]['coordenadas'].append({
                            "inicio": coordenada_inicio,
                            "fim": coordenada_fim
                        })
                    else:
                        logradouros_dict[full_name] = {
                            "logradouro": full_name,
                            "coordenadas": [
                                {
                                    "inicio": coordenada_inicio,
                                    "fim": coordenada_fim
                                }
                            ]
                        }

        for logradouro_name, log_data in logradouros_dict.items():
            # Verificar duplicatas antes de criar
            if Logradouro.objects.filter(nome=logradouro_name, cidade=municipio).exists():
                continue
            logradouro = Logradouro.objects.create(nome=logradouro_name, cidade=municipio)
            for coord in log_data['coordenadas']:
                LogCor.objects.create(
                    logradouro=logradouro,
                    dados={
                        "inicio": coord["inicio"],
                        "fim": coord["fim"]
                    }
                )
