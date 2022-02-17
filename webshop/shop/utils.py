from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


def getProductList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


def getProductDetail(request, pk):
    products = Product.objects.get(id=pk)
    serializer = ProductSerializer(products, many=False)
    return Response(serializer.data)


def createProduct(request):
    data = request.data
    serializer = ProductSerializer(data, many=False)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, data=data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return Response('Product was deleted!')