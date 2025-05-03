from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.utils import timezone
import uuid

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def listar_usuarios(request):
    query = request.query_params.get('q', '').strip()

    if query:
        if len(query) < 3:
            return Response({'error': 'A pesquisa deve conter pelo menos 3 caracteres.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Filtra por CPF, nome ou email
        usuarios = User.objects.filter(
            models.Q(nome__icontains=query) | 
            models.Q(email__icontains=query) | 
            models.Q(cpf__icontains=query)
        )
    else:
        usuarios = User.objects.all()

    serializer = UserSerializer(usuarios, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def criar_usuario(request):
    data = request.data.copy()

    if not request.user.is_authenticated:
        data['tipo_usuario'] = 'comum'

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        password = data.get('password')
        if password:
            user.set_password(password)
            user.save()
        return Response({
            'message': 'Conta criada com sucesso.',
            'usuario': serializer.data,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def visualizar_usuario(request, cpf):
    try:
        usuario = User.objects.get(cpf=cpf)
    except User.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if not (request.user.tipo_usuario == 'adm' or request.user == usuario):
        return Response({'error': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(usuario)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def atualizar_usuario(request, cpf):
    try:
        usuario = User.objects.get(cpf=cpf)
    except User.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if not (request.user.tipo_usuario == 'adm' or request.user == usuario):
        return Response({'error': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(usuario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deletar_usuario(request, cpf):
    try:
        usuario = User.objects.get(cpf=cpf)
    except User.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    usuario.delete()
    return Response({'message': 'Usuário deletado com sucesso.'}, status=status.HTTP_204_NO_CONTENT)

# PROFILE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        "cpf": user.cpf,
        "email": user.email,
        "nome": user.nome,
        "tipo": user.tipo_usuario,
    })

# RECUPERAR SENHA
@api_view(['POST'])
@permission_classes([AllowAny])
def recuperar_senha(request):
    identificador = request.data.get("identificador")

    if not identificador:
        return Response({"error": "Informe o CPF ou e-mail."}, status=400)

    try:
        if "@" in identificador:
            user = User.objects.get(email=identificador)
        else:
            user = User.objects.get(cpf=identificador)
    except User.DoesNotExist:
        return Response({"error": "Usuário não encontrado."}, status=404)

    # Gerar token único
    user.reset_token = uuid.uuid4().hex
    user.reset_token_created = timezone.now()
    user.save()

    # Simular envio de e-mail (substituir pelo send_mail real em produção)
    print(f"[DEBUG] Link de redefinição: https://seusite.com/redefinir-senha/{user.reset_token}")

    return Response({
        "message": "Se o usuário existir, um link de redefinição foi enviado para o e-mail cadastrado." + str({user.reset_token})
    }, status=200)
    
 # REDEFINIR SENHA   
@api_view(['POST'])
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

    if user.reset_token_created and timezone.now() - user.reset_token_created > timedelta(hours=1):
        return Response({"error": "Token expirado."}, status=400)

    # Redefinir senha
    user.set_password(nova_senha)
    user.reset_token = None
    user.reset_token_created = None
    user.save()

    return Response({"message": "Senha redefinida com sucesso."}, status=200)

# CONSULTAR TOKEN
@api_view(['GET'])
@permission_classes([AllowAny])
def verificar_token_recuperacao(request, token):
    try:
        user = User.objects.get(reset_token=token)
    except User.DoesNotExist:
        return Response({"error": "Token inválido ou expirado."}, status=404)

    from datetime import timedelta
    from django.utils import timezone

    if user.reset_token_created and timezone.now() - user.reset_token_created > timedelta(hours=1):
        return Response({"error": "Token expirado."}, status=400)

    return Response({"cpf": user.cpf})