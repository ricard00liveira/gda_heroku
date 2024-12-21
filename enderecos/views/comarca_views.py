from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Comarca
from ..serializers import ComarcaSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def listar_comarcas(request):
    comarcas = Comarca.objects.all()
    serializer = ComarcaSerializer(comarcas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def criar_comarca(request):
    serializer = ComarcaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def visualizar_comarca(request, comarca_id):
    try:
        comarca = Comarca.objects.get(id=comarca_id)
        serializer = ComarcaSerializer(comarca)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Comarca.DoesNotExist:
        return Response({'error': 'Comarca não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def atualizar_comarca(request, comarca_id):
    try:
        comarca = Comarca.objects.get(id=comarca_id)
        serializer = ComarcaSerializer(comarca, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Comarca.DoesNotExist:
        return Response({'error': 'Comarca não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deletar_comarca(request, comarca_id):
    try:
        comarca = Comarca.objects.get(id=comarca_id)
        comarca.delete()
        return Response({'message': 'Comarca deletada com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
    except Comarca.DoesNotExist:
        return Response({'error': 'Comarca não encontrada.'}, status=status.HTTP_404_NOT_FOUND)