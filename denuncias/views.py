from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import DenunciaSerializer
from enderecos.models import Municipio
from usuarios.models import User
from .serializers import AnexoSerializer
from .models import Denuncia, Anexo
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import openai
import os


class DenunciaViewSet(viewsets.ModelViewSet):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer


# READ_ALL
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def lista_denuncias(request):
    if request.user.tipo_usuario == "comum":
        denuncias = Denuncia.objects.filter(denunciante=request.user)
    else:
        denuncias = Denuncia.objects.all()
    serializer = DenunciaSerializer(denuncias, many=True, context={"request": request})
    return Response(serializer.data)


# READ_ONE
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def read_denuncia(request, denuncia_id):
    try:
        denuncia = Denuncia.objects.get(numero=denuncia_id)
        if (
            request.user.tipo_usuario not in ["adm", "operador"]
            and request.user != denuncia.denunciante
        ):
            return Response(
                {"error": "Você não tem permissão para visualizar esta denúncia."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = DenunciaSerializer(denuncia, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Denuncia.DoesNotExist:
        return Response(
            {"error": "Denúncia não encontrada."}, status=status.HTTP_404_NOT_FOUND
        )


# CREATE
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def criar_denuncia(request):
    data = request.data.copy()

    if request.user.tipo_usuario == "comum":
        data["denunciante"] = request.user.pk
    elif request.user.tipo_usuario in ["adm", "operador"]:
        if "denunciante" not in data or not data["denunciante"]:
            data["denunciante"] = None

    if request.user.tipo_usuario in ["adm", "operador"]:
        data["aprovada"] = True

    serializer = DenunciaSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def editar_denuncia(request, denuncia_id):
    try:
        denuncia = Denuncia.objects.get(numero=denuncia_id)
    except Denuncia.DoesNotExist:
        return Response(
            {"error": "Denúncia não encontrada"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.user.tipo_usuario not in ["adm", "operador"]:
        return Response(
            {"error": "Você não tem permissão para editar esta denúncia"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = DenunciaSerializer(
        denuncia, data=request.data, partial=True, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_denuncia(request, denuncia_id):
    try:
        denuncia = Denuncia.objects.get(numero=denuncia_id)
        if request.user.tipo_usuario not in ["adm", "operador"]:
            return Response(
                {"error": "Você não tem permissão para excluir esta denúncia"},
                status=status.HTTP_403_FORBIDDEN,
            )
        denuncia.delete()
        return Response(
            {"message": "Denúncia deletada com sucesso"},
            status=status.HTTP_204_NO_CONTENT,
        )
    except Denuncia.DoesNotExist:
        return Response(
            {"error": "Denúncia não encontrada"}, status=status.HTTP_404_NOT_FOUND
        )


# UPLOAD ANEXOS
@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_anexo(request):
    denuncia_id = request.data.get("denuncia")
    descricao = request.data.get("descricao", "")

    if not denuncia_id:
        return Response({"error": "ID da denúncia é obrigatório."}, status=400)

    try:
        denuncia = Denuncia.objects.get(pk=denuncia_id)
    except Denuncia.DoesNotExist:
        return Response({"error": "Denúncia não encontrada."}, status=404)

    arquivos = request.FILES.getlist("arquivos")
    if not arquivos:
        return Response({"error": "Nenhum arquivo enviado."}, status=400)

    total_existente = Anexo.objects.filter(denuncia=denuncia).count()
    if total_existente + len(arquivos) > 4:
        return Response(
            {
                "error": f"Essa denúncia já possui {total_existente} anexo(s). O limite é 4."
            },
            status=400,
        )

    anexos_criados = []
    for arquivo in arquivos:
        serializer = AnexoSerializer(
            data={"denuncia": denuncia.pk, "arquivo": arquivo, "descricao": descricao}
        )
        if serializer.is_valid():
            serializer.save()
            anexos_criados.append(serializer.data)
        else:
            return Response(
                {
                    "error": "Erro ao salvar um dos arquivos.",
                    "detalhes": serializer.errors,
                },
                status=400,
            )

    return Response(
        {
            "message": f"{len(anexos_criados)} anexo(s) enviado(s) com sucesso.",
            "anexos": anexos_criados,
        },
        status=201,
    )


# CRIAR DENUNCIA ANONIMA
@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def criar_denuncia_anonima(request):
    data = request.data.copy()
    data["anonima"] = True
    data["aprovada"] = False
    data["denunciante"] = None

    serializer = DenunciaSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        denuncia = serializer.save()

        return Response(
            {
                "mensagem": "Denúncia anônima registrada com sucesso.",
                "denuncia": DenunciaSerializer(
                    denuncia, context={"request": request}
                ).data,
            },
            status=201,
        )
    return Response(serializer.errors, status=400)


# TRANSCRICÃO DE AUDIO
openai.api_key = "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"


@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def transcrever_audio(request):
    audio_file = request.FILES.get("audio")
    if not audio_file:
        return Response({"error": "Nenhum arquivo de áudio foi enviado."}, status=400)

    try:
        audio_tuple = (audio_file.name, audio_file.read(), audio_file.content_type)
        transcription = openai.audio.transcriptions.create(
            model="whisper-1", file=audio_tuple
        )
        texto_transcrito = transcription.text
        chat = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente que melhora e organiza relatos ambientais. Não invente, apenas corrija gramática, clareza e fluidez do texto transcrito. Só responda com o texto corrigido. Até 2000 caracteres, caso contrário, resuma. Seja imparcial. Não adicione informações ou opiniões pessoais. Não use emojis ou formatação especial. Apenas o texto corrigido. Caso o trecho transcrito não faça sentido como uma denuncia ambiental ou não descreva fatos semelhantes a uma, retorne apenas a palavra 'irrelevante'.",
                },
                {"role": "user", "content": texto_transcrito},
            ],
        )
        texto_final = chat.choices[0].message.content.strip()

        return Response({"transcricao": texto_transcrito, "texto_final": texto_final})

    except Exception as e:
        return Response({"error": f"Erro ao processar o áudio: {str(e)}"}, status=500)


# VALIDAÇÃO DE HISTÓRICO
@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def validar_historico(request):
    texto = request.data.get("historico", "").strip()

    if not texto:
        return Response({"error": "Texto do histórico não fornecido."}, status=400)

    try:
        chat = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um classificador que identifica se um texto descreve ou não uma denúncia ambiental. "
                        "Analise apenas o conteúdo fornecido. Se for uma descrição plausível de um fato ambiental como desmatamento, poluição, maus-tratos à fauna, descarte irregular de resíduos, entre outros, retorne 'valido'. "
                        "Caso o texto esteja incompleto, irrelevante ou não tenha relação com crimes ou irregularidades ambientais, retorne 'irrelevante'. "
                        "Apenas retorne 'valido' ou 'irrelevante', sem explicações adicionais."
                    ),
                },
                {"role": "user", "content": texto},
            ],
        )

        classificacao = chat.choices[0].message.content.strip().lower()

        if classificacao not in ["valido", "irrelevante"]:
            return Response({"error": "Resposta inesperada do modelo."}, status=500)

        return Response({"classificacao": classificacao})

    except Exception as e:
        return Response({"error": f"Erro ao processar o texto: {str(e)}"}, status=500)
