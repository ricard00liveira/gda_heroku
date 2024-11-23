from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Municipio
from .serializers import MunicipioSerializer

class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

# CRUD MUNICIPIOS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_municipios(request):
    municipios = Municipio.objects.all()
    serializer = MunicipioSerializer(municipios, many=True, context={'request': request})
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