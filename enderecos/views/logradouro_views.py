from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from ..models import Logradouro, Municipio, LogCor as TrechoLogradouro
from ..serializers.logradouro_serializers import LogradouroSerializer
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import LineString, MultiLineString
from django.db import transaction
import json
import unicodedata
import tempfile
import os


# BUSCAR TODOS LOGRADOUROS POR UM MUNICIPIO (PAGINADO)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_logradouros(request, municipio_id):
    municipio = get_object_or_404(Municipio, id=municipio_id)

    query = request.query_params.get("q", "").strip()

    if query:
        if len(query) < 3:
            return Response(
                {"error": "A pesquisa deve conter pelo menos 3 caracteres."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logradouros = Logradouro.objects.filter(nome__icontains=query, cidade=municipio)
    else:
        logradouros = Logradouro.objects.filter(cidade=municipio)

    logradouros = logradouros.order_by("nome")

    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(logradouros, request)

    serializer = LogradouroSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def criar_logradouro(request, municipio_id):
    try:
        municipio = Municipio.objects.get(id=municipio_id)
    except Municipio.DoesNotExist:
        return Response(
            {"error": "Município não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    data = request.data.copy()
    data["cidade"] = municipio.id

    serializer = LogradouroSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def visualizar_logradouro(request, logradouro_id):
    try:
        logradouro = Logradouro.objects.get(id=logradouro_id)
    except Logradouro.DoesNotExist:
        return Response(
            {"error": "Logradouro não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = LogradouroSerializer(logradouro)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsAdminUser])
def atualizar_logradouro(request, logradouro_id):
    try:
        logradouro = Logradouro.objects.get(id=logradouro_id)
    except Logradouro.DoesNotExist:
        return Response(
            {"error": "Logradouro não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = LogradouroSerializer(logradouro, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def deletar_logradouro(request, logradouro_id):
    try:
        logradouro = Logradouro.objects.get(id=logradouro_id)
    except Logradouro.DoesNotExist:
        return Response(
            {"error": "Logradouro não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    logradouro.delete()
    return Response(
        {"message": "Logradouro deletado com sucesso."},
        status=status.HTTP_204_NO_CONTENT,
    )


# IMPORTAR LOGRADOUROS DE UM ARQUIVO JSON
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def importar_logradouros_json(request, municipio_id):
    municipio = get_object_or_404(Municipio, id=municipio_id)

    caminho = request.data.get("arquivo_path")
    if not caminho or not os.path.exists(caminho):
        return Response(
            {"error": "Arquivo não encontrado no caminho informado."}, status=400
        )

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError:
        return Response({"error": "Erro ao ler o arquivo JSON."}, status=400)

    logradouros_criados = 0
    geometrias_atualizadas = 0

    for item in dados:
        nome = item.get("logradouro", "").strip().upper()
        if not nome:
            continue

        logradouro, criado = Logradouro.objects.get_or_create(
            nome=nome, cidade=municipio
        )
        if criado:
            logradouros_criados += 1

        linhas = []
        for trecho in item.get("coordenadas", []):
            try:
                inicio = tuple(trecho["inicio"])
                fim = tuple(trecho["fim"])
                linha = LineString(inicio, fim, srid=4326)
                linhas.append(linha)
            except Exception:
                continue

        if linhas:
            multi = MultiLineString(linhas, srid=4326)

            with transaction.atomic():
                trecho_existente = getattr(logradouro, "trecho_unico", None)
                if trecho_existente:
                    # Atualiza a geometria existente
                    trecho_existente.trecho = multi
                    trecho_existente.save()
                else:
                    TrechoLogradouro.objects.create(logradouro=logradouro, trecho=multi)
                geometrias_atualizadas += 1

    return Response(
        {
            "mensagem": "Importação concluída.",
            "logradouros_criados": logradouros_criados,
            "geometrias_salvas": geometrias_atualizadas,
            "arquivo_usado": caminho,
        },
        status=201,
    )


# CRIAR ARQUIVO JSON BASEADO NO IBGE
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
@parser_classes([MultiPartParser])
def normalizar_logradouros_ibge(request):
    arquivo_ibge = request.FILES.get("arquivo")
    if not arquivo_ibge:
        return Response({"error": "Arquivo JSON do IBGE não enviado."}, status=400)

    try:
        data = json.load(arquivo_ibge)
    except json.JSONDecodeError:
        return Response({"error": "Arquivo JSON inválido."}, status=400)

    logradouros_dict = {}

    for feature in data.get("features", []):
        props = feature.get("properties", {})
        coords = feature.get("geometry", {}).get("coordinates", [])

        if feature.get("geometry", {}).get("type") != "LineString" or len(coords) < 2:
            continue

        nome = " ".join(
            filter(
                None,
                [props.get("NM_TIP_LOG"), props.get("NM_TIT_LOG"), props.get("NM_LOG")],
            )
        )
        nome = (
            unicodedata.normalize("NFKD", nome.strip().upper())
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )

        if not nome:
            continue

        trecho = {"inicio": coords[0], "fim": coords[-1]}
        if nome in logradouros_dict:
            logradouros_dict[nome]["coordenadas"].append(trecho)
        else:
            logradouros_dict[nome] = {"logradouro": nome, "coordenadas": [trecho]}

    dados_formatados = list(logradouros_dict.values())

    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, suffix=".json", encoding="utf-8"
    ) as tmp_file:
        json.dump(dados_formatados, tmp_file, ensure_ascii=False, indent=2)
        tmp_path = tmp_file.name

    return Response(
        {
            "mensagem": "Logradouros normalizados com sucesso.",
            "arquivo_temporario": tmp_path,
        },
        status=200,
    )
