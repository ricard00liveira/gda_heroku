from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.gis.geos import Point

from usuarios.models import User
from .models import Denuncia
from .serializers import DenunciaSerializer
from .views import lista_denuncias


class DenunciaSerializerTests(TestCase):
    def test_validate_descricao_min_length(self):
        data = {"descricao": "curto"}
        serializer = DenunciaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("descricao", serializer.errors)

    def test_create_with_coordinates(self):
        user = User.objects.create_user(cpf="00000000000", email="a@example.com", nome="A")
        data = {
            "descricao": "Descricao suficiente",
            "denunciante": user.pk,
            "latitude": -10.0,
            "longitude": 20.0,
        }
        serializer = DenunciaSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        denuncia = serializer.save()
        self.assertIsInstance(denuncia.localizacao, Point)
        self.assertEqual(denuncia.localizacao.x, 20.0)
        self.assertEqual(denuncia.localizacao.y, -10.0)


class DenunciaViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(cpf="11111111111", email="u1@example.com", nome="U1")
        self.user2 = User.objects.create_user(cpf="22222222222", email="u2@example.com", nome="U2")
        Denuncia.objects.create(descricao="Teste 1", denunciante=self.user1)
        Denuncia.objects.create(descricao="Teste 2", denunciante=self.user2)

    def test_lista_denuncias_filtra_por_usuario(self):
        request = self.factory.get("/denuncias/")
        force_authenticate(request, user=self.user1)
        response = lista_denuncias(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["denunciante"], self.user1.pk)

