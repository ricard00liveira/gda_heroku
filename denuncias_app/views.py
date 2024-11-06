from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Denuncia
from .serializers import DenunciaSerializer

class DenunciaViewSet(viewsets.ModelViewSet):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer

@api_view(['GET'])
def lista_denuncias(request):
    denuncias = Denuncia.objects.all()
    serializer = DenunciaSerializer(denuncias, many=True)
    return Response(serializer.data)

def view_lista_denuncias(request):
    return render(request, 'denuncias_list.html')