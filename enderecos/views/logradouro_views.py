from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Logradouro, Municipio
from ..serializers.logradouro_serializers import LogradouroSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_logradouros(request, municipio_id):
    municipio = get_object_or_404(Municipio, id=municipio_id)

    query = request.query_params.get('q', '').strip()

    if query:
        if len(query) < 3:
            return Response({'error': 'A pesquisa deve conter pelo menos 3 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)
        logradouros = Logradouro.objects.filter(nome__icontains=query, cidade=municipio)
    else:
        logradouros = Logradouro.objects.filter(cidade=municipio)

    serializer = LogradouroSerializer(logradouros, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def criar_logradouro(request, municipio_id):
    try:
        municipio = Municipio.objects.get(id=municipio_id)
    except Municipio.DoesNotExist:
        return Response({'error': 'Município não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['cidade'] = municipio.id

    serializer = LogradouroSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def visualizar_logradouro(request, logradouro_id):
    try:
        logradouro = Logradouro.objects.get(id=logradouro_id)
    except Logradouro.DoesNotExist:
        return Response({'error': 'Logradouro não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LogradouroSerializer(logradouro)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def atualizar_logradouro(request, logradouro_id):
    try:
        logradouro = Logradouro.objects.get(id=logradouro_id)
    except Logradouro.DoesNotExist:
        return Response({'error': 'Logradouro não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LogradouroSerializer(logradouro, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deletar_logradouro(request, logradouro_id):
    try:
        logradouro = Logradouro.objects.get(id=logradouro_id)
    except Logradouro.DoesNotExist:
        return Response({'error': 'Logradouro não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    logradouro.delete()
    return Response({'message': 'Logradouro deletado com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
