from rest_framework.decorators import api_view, permission_classes
from .utils import updateProduct, getProductDetail, deleteProduct, getProductList, createProduct
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def getProducts(request):
    if request.method == 'GET':
        return getProductList(request)

    if request.method == 'POST':
        return createProduct(request)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def getProduct(request, pk):
    if request.method == 'GET':
        return getProductDetail(request, pk)

    if request.method == 'PUT':
        return updateProduct(request, pk)

    if request.method == 'DELETE':
        return deleteProduct(request, pk)