from django.shortcuts import render
from .models import User

# PROFILE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        "cpf": user.cpf,
        "email": user.email,
        "nome": user.nome,
        "tipo": user.tipo_usuario
    })
