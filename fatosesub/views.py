from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Fato, Subfato
from .serializers import FatoSerializer, SubfatoSerializer

# CRUD Fato
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_fatos(request):
    fatos = Fato.objects.all()
    serializer = FatoSerializer(fatos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def criar_fato(request):
    serializer = FatoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def visualizar_fato(request, fato_id):
    try:
        fato = Fato.objects.get(id=fato_id)
    except Fato.DoesNotExist:
        return Response({'error': 'Fato não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = FatoSerializer(fato)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def atualizar_fato(request, fato_id):
    try:
        fato = Fato.objects.get(id=fato_id)
    except Fato.DoesNotExist:
        return Response({'error': 'Fato não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = FatoSerializer(fato, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deletar_fato(request, fato_id):
    try:
        fato = Fato.objects.get(id=fato_id)
    except Fato.DoesNotExist:
        return Response({'error': 'Fato não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    fato.delete()
    return Response({'message': 'Fato deletado com sucesso.'}, status=status.HTTP_204_NO_CONTENT)

# CRUD Subfato
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_subfatos(request, fato_id):
    try:
        fato = Fato.objects.get(id=fato_id)
    except Fato.DoesNotExist:
        return Response({'error': 'Fato não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    subfatos = Subfato.objects.filter(fato=fato)
    serializer = SubfatoSerializer(subfatos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def criar_subfato(request, fato_id):
    try:
        fato = Fato.objects.get(id=fato_id)
    except Fato.DoesNotExist:
        return Response({'error': 'Fato não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    data = request.data.copy()
    data['fato'] = fato.id
    serializer = SubfatoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def visualizar_subfato(request, subfato_id):
    try:
        subfato = Subfato.objects.get(id=subfato_id)
    except Subfato.DoesNotExist:
        return Response({'error': 'Subfato não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SubfatoSerializer(subfato)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def atualizar_subfato(request, subfato_id):
    try:
        subfato = Subfato.objects.get(id=subfato_id)
    except Subfato.DoesNotExist:
        return Response({'error': 'Subfato não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SubfatoSerializer(subfato, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deletar_subfato(request, subfato_id):
    try:
        subfato = Subfato.objects.get(id=subfato_id)
    except Subfato.DoesNotExist:
        return Response({'error': 'Subfato não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    subfato.delete()
    return Response({'message': 'Subfato deletado com sucesso.'}, status=status.HTTP_204_NO_CONTENT)