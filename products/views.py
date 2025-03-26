from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import ProductService

product_service = ProductService()

@api_view(['GET'])
def list_products(request):
    print("I am trying to request")
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 5)
    products = product_service.list_products(page, page_size)
    return Response(products)

@api_view(['POST'])
def create_product(request):
    try:
        product = product_service.create_product(request.data)
        return Response(product.to_json(), status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_product(request, product_id):
    try:
        product = product_service.get_product(product_id)
        return Response(product.to_json())
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_product(request, product_id):
    try:
        product = product_service.update_product(product_id, request.data)
        return Response(product.to_json())
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, product_id):
    if product_service.delete_product(product_id):
        return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


