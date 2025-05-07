from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import DenunciaSerializer
from enderecos.models import Municipio
from usuarios.models import User
from .serializers import AnexoSerializer
from .models import Denuncia, Anexo
from rest_framework.parsers import MultiPartParser, FormParser

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
        if request.user.tipo_usuario not in ['adm', 'operador'] and request.user != denuncia.denunciante:
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

    if request.user.tipo_usuario in ['adm', 'operador']:
        data['aprovada'] = True
        
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

# UPLOAD ANEXOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_anexo(request):
    denuncia_id = request.data.get('denuncia')
    descricao = request.data.get('descricao', '')

    if not denuncia_id:
        return Response({'error': 'ID da denúncia é obrigatório.'}, status=400)

    try:
        denuncia = Denuncia.objects.get(pk=denuncia_id)
    except Denuncia.DoesNotExist:
        return Response({'error': 'Denúncia não encontrada.'}, status=404)

    # Validação de permissão
    if request.user.tipo_usuario not in ['adm', 'operador'] and request.user != denuncia.denunciante:
        return Response({'error': 'Você não tem permissão para anexar arquivos a esta denúncia.'}, status=403)

    arquivos = request.FILES.getlist('arquivos')
    if not arquivos:
        return Response({'error': 'Nenhum arquivo enviado.'}, status=400)

    total_existente = Anexo.objects.filter(denuncia=denuncia).count()
    if total_existente + len(arquivos) > 4:
        return Response({'error': f'Essa denúncia já possui {total_existente} anexo(s). O limite é 4.'}, status=400)

    anexos_criados = []
    for arquivo in arquivos:
        serializer = AnexoSerializer(data={
            'denuncia': denuncia.pk,
            'arquivo': arquivo,
            'descricao': descricao
        })
        if serializer.is_valid():
            serializer.save()
            anexos_criados.append(serializer.data)
        else:
            return Response({'error': 'Erro ao salvar um dos arquivos.', 'detalhes': serializer.errors}, status=400)

    return Response({'message': f'{len(anexos_criados)} anexo(s) enviado(s) com sucesso.', 'anexos': anexos_criados}, status=201)
