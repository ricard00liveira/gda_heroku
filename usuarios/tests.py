from django.test import TestCase
from .models import User
from .serializers import UserSerializer


class UserSerializerTests(TestCase):
    def test_validate_cpf_invalid(self):
        serializer = UserSerializer(data={"cpf": "123", "email": "a@a.com", "nome": "A", "password": "pass"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("cpf", serializer.errors)

    def test_create_user(self):
        data = {"cpf": "99999999999", "email": "a@a.com", "nome": "A", "password": "secret"}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertTrue(user.check_password("secret"))


class UserModelTests(TestCase):
    def test_generate_reset_token(self):
        user = User.objects.create_user(cpf="77777777777", email="u@u.com", nome="U")
        self.assertIsNone(user.reset_token)
        user.generate_reset_token()
        self.assertIsNotNone(user.reset_token)

