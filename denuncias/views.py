from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Denuncia
from .serializers import DenunciaSerializer
from enderecos.models import Municipio
from usuarios.models import User

class DenunciaViewSet(viewsets.ModelViewSet):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer
#READ_ALL
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_denuncias(request):
    if request.user.tipo_usuario == 'comum':
        denuncias = Denuncia.objects.filter(denunciante=request.user)
    else:
        denuncias = Denuncia.objects.all()
    serializer = DenunciaSerializer(denuncias, many=True, context={'request': request})
    return Response(serializer.data)

#READ_ONE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_denuncia(request, denuncia_id):
    try:
        denuncia = Denuncia.objects.get(numero=denuncia_id)
        if not (request.user.tipo_usuario != 'adm' or request.user.tipo_usuario != 'operador' or request.user != denuncia.denunciante):
            return Response({'error': 'Você não tem permissão para visualizar esta denúncia.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DenunciaSerializer(denuncia, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Denuncia.DoesNotExist:
        return Response({'error': 'Denúncia não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

#CREATE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_denuncia(request):
    data = request.data.copy()
    
    if request.user.tipo_usuario == 'comum':
        data['denunciante'] = request.user.pk
    elif request.user.tipo_usuario in ['adm', 'operador']:
        if 'denunciante' not in data or not data['denunciante']:
            data['denunciante'] = None

    serializer = DenunciaSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#UPDATE
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def editar_denuncia(request, denuncia_id):
    try:
        denuncia = Denuncia.objects.get(numero=denuncia_id)
    except Denuncia.DoesNotExist:
        return Response({'error': 'Denúncia não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.tipo_usuario not in ['adm', 'operador']:
        return Response({'error': 'Você não tem permissão para editar esta denúncia'}, status=status.HTTP_403_FORBIDDEN)

    serializer = DenunciaSerializer(denuncia, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#DELETE
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_denuncia(request, denuncia_id):
    try:
        denuncia = Denuncia.objects.get(numero=denuncia_id)
        if request.user.tipo_usuario not in ['adm', 'operador']:
            return Response({'error': 'Você não tem permissão para excluir esta denúncia'}, status=status.HTTP_403_FORBIDDEN)
        denuncia.delete()
        return Response({'message': 'Denúncia deletada com sucesso'}, status=status.HTTP_204_NO_CONTENT)
    except Denuncia.DoesNotExist:
        return Response({'error': 'Denúncia não encontrada'}, status=status.HTTP_404_NOT_FOUND)
