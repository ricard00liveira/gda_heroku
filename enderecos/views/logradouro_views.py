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
def lista_logradouros(request):
    logradouros = Logradouro.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(logradouros, request)
    serializer = LogradouroSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)