from rest_framework import viewsets, status
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import User
from .serializers import UserSerializer
from django.utils import timezone
from django.utils.timezone import now
import uuid
import os


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def listar_usuarios(request):
    query = request.query_params.get("q", "").strip()

    if query:
        if len(query) < 3:
            return Response(
                {"error": "A pesquisa deve conter pelo menos 3 caracteres."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Filtra por CPF, nome ou email
        usuarios = User.objects.filter(
            models.Q(nome__icontains=query)
            | models.Q(email__icontains=query)
            | models.Q(cpf__icontains=query)
        )
    else:
        usuarios = User.objects.all()

    serializer = UserSerializer(usuarios, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def criar_usuario(request):
    data = request.data.copy()

    if not request.user.is_authenticated:
        data["tipo_usuario"] = "comum"

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        password = data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return Response(
            {
                "message": "Conta criada com sucesso.",
                "usuario": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def visualizar_usuario(request, cpf):
    try:
        usuario = User.objects.get(cpf=cpf)
    except User.DoesNotExist:
        return Response(
            {"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    # Apenas o próprio usuário ou administradores podem visualizar
    if not (request.user.tipo_usuario == "adm" or request.user == usuario):
        return Response(
            {"error": "Permissão negada."}, status=status.HTTP_403_FORBIDDEN
        )

    from denuncias.models import Denuncia
    from denuncias.serializers import DenunciaSerializer

    denuncias = Denuncia.objects.filter(denunciante=usuario).order_by("-data")
    denuncias_serializadas = DenunciaSerializer(denuncias, many=True).data

    usuario_serializado = UserSerializer(usuario).data

    return Response(
        {"usuario": usuario_serializado, "denuncias": denuncias_serializadas}
    )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def atualizar_usuario(request, cpf):
    try:
        usuario = User.objects.get(cpf=cpf)
    except User.DoesNotExist:
        return Response(
            {"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    imagem_nova = request.FILES.get("imagem_perfil", None)

    if imagem_nova:
        # Apagar imagem antiga (se existir)
        if usuario.imagem_perfil:
            usuario.imagem_perfil.delete(save=False)

        # Gerar nome único com UUID
        ext = os.path.splitext(imagem_nova.name)[1]  # ex: .jpg
        nome_unico = f"{uuid.uuid4().hex}{ext}"

        # Atribuir o novo nome ao arquivo
        imagem_nova.name = nome_unico
        request._mutable = True  # garantir edição do request.data
        request.data["imagem_perfil"] = imagem_nova

    email = request.data.get("email")
    if email and email != usuario.email:
        if User.objects.filter(email=email).exclude(cpf=usuario.cpf).exists():
            return Response(
                {"error": "Erro no e-mail, escolha outro."},
                status=status.HTTP_409_CONFLICT,
            )

    serializer = UserSerializer(usuario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deletar_usuario(request, cpf):
    try:
        usuario = User.objects.get(cpf=cpf)
    except User.DoesNotExist:
        return Response(
            {"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    usuario.delete()
    return Response(
        {"message": "Usuário deletado com sucesso."}, status=status.HTTP_204_NO_CONTENT
    )


# PROFILE
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response(
        {
            "cpf": user.cpf,
            "email": user.email,
            "nome": user.nome,
            "tipo_usuario": user.tipo_usuario,
            "imagem_perfil_url": user.imagem_perfil.url if user.imagem_perfil else None,
            "conf_tema": user.conf_tema,
            "conf_notEmail": user.conf_not_email,
            "conf_notPush": user.conf_not_push,
            "conf_notNewDenuncia": user.conf_not_newdenun,
            "user_created": user.date_created,
        }
    )


# RECUPERAR SENHA
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


@api_view(["POST"])
@permission_classes([AllowAny])
def recuperar_senha(request):
    identificador = request.data.get("identificador")

    if not identificador:
        return Response({"error": "Informe o CPF ou e-mail."}, status=400)

    try:
        user = (
            User.objects.get(email=identificador)
            if "@" in identificador
            else User.objects.get(cpf=identificador)
        )
    except User.DoesNotExist:
        return Response({"error": "Usuário não encontrado."}, status=404)

    # Gerar token
    user.reset_token = uuid.uuid4().hex
    user.reset_token_created = timezone.now()
    user.save()

    # Carregar credenciais do token.json
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    # Preparar conteúdo do e-mail
    BASE_URL = "https://gda-app.xyz/"
    reset_link = f"{BASE_URL}renew-password"
    corpo_email = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; color: #333;">
    <div style="max-width: 600px; margin: auto; background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.05);">

      <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://gda-app.s3.us-east-2.amazonaws.com/app/icon_gda.png" alt="Logo GDA" style="max-width: 120px; height: auto;" />
      </div>

      <h2 style="color: #2c3e50;">Olá, {user.nome},</h2>

      <p>Recebemos uma solicitação para redefinir sua senha no sistema <strong>GDA</strong>.</p>

      <p>
        Clique no link abaixo para definir uma nova senha:<br>
        <a href="{reset_link}" style="color: #1a73e8; word-break: break-all;">{reset_link}</a>
      </p>

      <p>
        <strong>Use o código de verificação abaixo:</strong><br>
        <span style="display: inline-block; font-size: 1.5em; font-weight: bold; color: #d32f2f; margin: 10px 0;">{user.reset_token}</span>
      </p>

      <p style="color: #777;">
        ⚠️ O código acima expira em <strong>1 hora</strong>. Solicite outro código se necessário.
      </p>

      <p>Se você não solicitou essa alteração, ignore este e-mail.</p>

      <p style="margin-top: 30px;">Atenciosamente,<br/>Equipe do <strong>Sistema GDA</strong>.</p>
    </div>
  </body>
</html>

"""
    message = MIMEText(corpo_email, "html")
    message["to"] = user.email
    message["subject"] = "Redefinição de Senha - GDA"
    raw = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        enviado = service.users().messages().send(userId="me", body=raw).execute()
        print(f"E-mail enviado. ID: {enviado['id']}")
    except Exception as e:
        return Response({"error": f"Erro ao enviar e-mail: {str(e)}"}, status=500)

    return Response(
        {
            "message": "Se o usuário existir, um link foi enviado para o e-mail cadastrado."
        },
        status=200,
    )


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def recuperar_senha(request):
#     identificador = request.data.get("identificador")

#     if not identificador:
#         return Response({"error": "Informe o CPF ou e-mail."}, status=400)

#     try:
#         if "@" in identificador:
#             user = User.objects.get(email=identificador)
#         else:
#             user = User.objects.get(cpf=identificador)
#     except User.DoesNotExist:
#         return Response({"error": "Usuário não encontrado."}, status=404)

#     # Gerar token único
#     user.reset_token = uuid.uuid4().hex
#     user.reset_token_created = timezone.now()
#     user.save()

#     # Simular envio de e-mail (substituir pelo send_mail real em produção)
#     print(f"[DEBUG] Link de redefinição: https://seusite.com/redefinir-senha/{user.reset_token}")

#     return Response({
#         "message": "Se o usuário existir, um link de redefinição foi enviado para o e-mail cadastrado." + str({user.reset_token})
#     }, status=200)


# REDEFINIR SENHA
@api_view(["POST"])
@permission_classes([AllowAny])
def redefinir_senha(request):
    token = request.data.get("token")
    nova_senha = request.data.get("nova_senha")

    if not token or not nova_senha:
        return Response({"error": "Token e nova senha são obrigatórios."}, status=400)

    try:
        user = User.objects.get(reset_token=token)
    except User.DoesNotExist:
        return Response({"error": "Token inválido ou expirado."}, status=404)

    from datetime import timedelta
    from django.utils import timezone

    if (
        user.reset_token_created
        and timezone.now() - user.reset_token_created > timedelta(hours=1)
    ):
        return Response({"error": "Token expirado."}, status=400)

    # Redefinir senha
    user.set_password(nova_senha)
    user.reset_token = None
    user.reset_token_created = None
    user.save()

    return Response({"message": "Senha redefinida com sucesso."}, status=200)


# ALTERAR SENHA
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def alterar_senha(request):
    user = request.user
    senha_atual = request.data.get("senha_atual")
    nova_senha = request.data.get("nova_senha")

    if not senha_atual or not nova_senha:
        return Response({"error": "Todos os campos são obrigatórios."}, status=400)

    if not user.check_password(senha_atual):
        return Response({"error": "Senha atual incorreta."}, status=403)

    if len(nova_senha) < 6:
        return Response(
            {"error": "A nova senha deve ter pelo menos 6 caracteres."}, status=400
        )

    user.set_password(nova_senha)
    user.save()

    return Response({"message": "Senha alterada com sucesso."}, status=200)


# CONSULTAR TOKEN
@api_view(["GET"])
@permission_classes([AllowAny])
def verificar_token_recuperacao(request, token):
    try:
        user = User.objects.get(reset_token=token)
    except User.DoesNotExist:
        return Response({"error": "Token inválido ou expirado."}, status=404)

    from datetime import timedelta
    from django.utils import timezone

    if (
        user.reset_token_created
        and timezone.now() - user.reset_token_created > timedelta(hours=1)
    ):
        return Response({"error": "Token expirado."}, status=400)

    return Response({"cpf": user.cpf})


# LAST LOGIN
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def atualizar_last_login(request):
    user = request.user
    user.last_login = now()
    user.save(update_fields=["last_login"])

    return Response(
        {
            "message": "Último login atualizado com sucesso.",
            "last_login": user.last_login,
        },
        status=status.HTTP_200_OK,
    )
