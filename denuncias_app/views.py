from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Denuncia, Municipio
from .serializers import DenunciaSerializer, MunicipioSerializer

class DenunciaViewSet(viewsets.ModelViewSet):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer

class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_municipios(request):
    municipios = Municipio.objects.all()
    serializer = MunicipioSerializer(municipios, many=True)
    return Response(serializer.data)


# CRUD DENUNCIAS
@api_view(['GET'])
def lista_denuncias(request):
    denuncias = Denuncia.objects.all()
    serializer = DenunciaSerializer(denuncias, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_denuncia(request):
    descricao = request.data.get('descricao')
    municipio_id = request.data.get('municipio')
    
    try:
        municipio = Municipio.objects.get(id=municipio_id)
    except Municipio.DoesNotExist:
        return Response({'error': 'Município inválido'}, status=status.HTTP_400_BAD_REQUEST)

    denuncia = Denuncia.objects.create(
        descricao=descricao,
        municipio=municipio,
        usuario=request.user
    )
    
    serializer = DenunciaSerializer(denuncia)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

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

# PROFILE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        "cpf": user.cpf,
        "email": user.email,
        "nome": user.nome,
        "tipo_usuario": user.tipo_usuario
    })