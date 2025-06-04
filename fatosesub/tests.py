from django.test import TestCase
from .models import Fato
from .serializers import FatoSerializer


class FatoSerializerTests(TestCase):
    def test_unique_nome_validation(self):
        Fato.objects.create(nome="A")
        serializer = FatoSerializer(data={"nome": "A"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("nome", serializer.errors)


class FatoModelTests(TestCase):
    def test_str_representation(self):
        fato = Fato.objects.create(nome="Teste")
        self.assertEqual(str(fato), "Teste")

