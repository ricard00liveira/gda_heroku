from rest_framework import serializers
from ..models import Comarca

class ComarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comarca
        fields = '__all__'