from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Denuncia, Municipio, User
from .serializers import DenunciaSerializer, MunicipioSerializer

class DenunciaViewSet(viewsets.ModelViewSet):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer

class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    
# CRUD MUNICIPIOS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_municipios(request):
    municipios = Municipio.objects.all()
    serializer = MunicipioSerializer(municipios, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def criar_municipio(request):
    if request.method == 'POST':
        serializer = MunicipioSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CRUD DENUNCIAS
@api_view(['GET'])
def lista_denuncias(request):
    if request.user.tipo_usuario == 'comum':
        denuncias = Denuncia.objects.filter(usuario=request.user)
    else:
        denuncias = Denuncia.objects.all()
    serializer = DenunciaSerializer(denuncias, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_denuncia(request, denuncia_id):
    try:
        denuncia = Denuncia.objects.get(numero=denuncia_id)
    except Denuncia.DoesNotExist:
        return Response({'error': 'Denúncia não encontrada.'},
                        status=status.HTTP_404_NOT_FOUND)
    
    if request.user.tipo_usuario == 'comum' and denuncia.usuario != request.user:
        return Response({'error': 'Você não tem permissão para acessar esta denúncia.'},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = DenunciaSerializer(denuncia, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_denuncia(request):
    data = request.data.copy()
    data['usuario'] = request.user.cpf
    
    serializer = DenunciaSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_denuncia(request, denuncia_id):
    try:
        denuncia = Denuncia.objects.get(numero=denuncia_id)
    except Denuncia.DoesNotExist:
        return Response({'error': 'Denúncia não encontrada ou você não tem permissão para deletá-la.'},
                        status=status.HTTP_404_NOT_FOUND)
    denuncia.delete()
    return Response({'message': 'Denúncia deletada com sucesso.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def editar_denuncia(request, denuncia_id):
    try:
        denuncia = Denuncia.objects.get(numero=denuncia_id)
    except Denuncia.DoesNotExist:
        return Response({'error': 'Denúncia não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    usuario = User.objects.get(cpf=request.user.cpf)
    if usuario.tipo_usuario != 'adm' and usuario.tipo_usuario != 'operador':
        return Response({'error': 'Você não tem permissão para essa ação.'}, status=status.HTTP_404_NOT_FOUND)

    descricao = request.data.get('descricao', None)
    municipio_id = request.data.get('municipio', None)
    status_denuncia = request.data.get('status', None)

    if status_denuncia is not None:
        if status_denuncia == 'Pendente' or status_denuncia == 'Resolvido':
            denuncia.status = status_denuncia
        else:
            return Response({'error': 'Status não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if descricao is not None:
        denuncia.descricao = descricao

    if municipio_id is not None:
        try:
            municipio = Municipio.objects.get(id=municipio_id)
            denuncia.municipio = municipio
        except Municipio.DoesNotExist:
            return Response({'error': 'Município inválido'}, status=status.HTTP_400_BAD_REQUEST)
    
    denuncia.save()

    serializer = DenunciaSerializer(denuncia)
    return Response(serializer.data, status=status.HTTP_200_OK)

# PROFILE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        "cpf": user.cpf,
        "email": user.email,
        "nome": user.nome,
        "tipo": user.tipo_usuario
    })