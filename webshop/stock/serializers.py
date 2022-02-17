from rest_framework.serializers import ModelSerializer
from webshop.shop.models import Product


class BucketSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class BucketItemSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'