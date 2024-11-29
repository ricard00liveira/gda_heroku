from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from ..models import Municipio, Logradouro, LogCor
from ..serializers.municipio_serializers import MunicipioSerializer
from ..serializers.logradouro_serializers import LogradouroSerializer

# CRUD LOGRADOURO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_logradouros(request, municipio_id):
    # Obter o parâmetro de pesquisa
    query = request.query_params.get('q', '').strip()

    if not query or len(query) < 3:
        return Response({'error': 'A pesquisa deve conter pelo menos 3 caracteres.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        municipio = Municipio.objects.get(id=municipio_id)
    except Municipio.DoesNotExist:
        return Response({'error': 'Município não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    logradouros = Logradouro.objects.filter(nome__icontains=query, cidade=municipio)[:5]
    
    serializer = LogradouroSerializer(logradouros, many=True)
    return Response(serializer.data)