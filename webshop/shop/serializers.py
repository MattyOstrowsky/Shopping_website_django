from rest_framework.serializers import ModelSerializer
from .models import Product
from rest_framework import permissions

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'