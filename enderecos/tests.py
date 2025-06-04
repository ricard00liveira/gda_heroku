from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Municipio, Logradouro
from .serializers.logradouro_serializers import LogradouroSerializer
from .views.municipio_views import lista_municipios
from usuarios.models import User


class LogradouroSerializerTests(TestCase):
    def test_validate_nome_upper_strip(self):
        municipio = Municipio.objects.create(nome="Cidade")
        data = {"nome": " rua a ", "cidade": municipio.pk}
        serializer = LogradouroSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        logradouro = serializer.save()
        self.assertEqual(logradouro.nome, "RUA A")


class MunicipioViewTests(TestCase):
    def test_lista_municipios(self):
        Municipio.objects.create(nome="Cidade1")
        Municipio.objects.create(nome="Cidade2")
        factory = APIRequestFactory()
        user = User.objects.create_user(cpf="33333333333", email="x@example.com", nome="X", tipo_usuario="adm")
        request = factory.get("/municipios/")
        force_authenticate(request, user=user)
        response = lista_municipios(request)
        self.assertEqual(len(response.data), 2)

