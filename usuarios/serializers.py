from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    date_created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate_cpf(self, value):
        if len(value) != 11 or not value.isdigit():
            raise serializers.ValidationError("Enter a valid CPF.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
