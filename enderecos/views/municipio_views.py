from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Municipio
from ..serializers.municipio_serializers import MunicipioSerializer


# CRUD MUNICIPIOS

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_municipios(request):
    municipios = Municipio.objects.all()
    serializer = MunicipioSerializer(municipios, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def criar_municipio(request):
    serializer = MunicipioSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        municipio = serializer.save()
        return Response({
            'message': 'Município criado com sucesso.',
            'id': municipio.id,
            'nome': municipio.nome
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def visualizar_municipio(request, municipio_id):
    try:
        municipio = Municipio.objects.get(id=municipio_id)
    except Municipio.DoesNotExist:
        return Response({'error': 'Município não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MunicipioSerializer(municipio, context={'request': request})
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def atualizar_municipio(request, municipio_id):
    try:
        municipio = Municipio.objects.get(id=municipio_id)
    except Municipio.DoesNotExist:
        return Response({'error': 'Município não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MunicipioSerializer(municipio, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Município atualizado com sucesso.',
            'id': municipio.id,
            'nome': municipio.nome
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deletar_municipio(request, municipio_id):
    try:
        municipio = Municipio.objects.get(id=municipio_id)
    except Municipio.DoesNotExist:
        return Response({'error': 'Município não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    municipio.delete()
    return Response({'message': 'Município deletado com sucesso.'}, status=status.HTTP_204_NO_CONTENT)