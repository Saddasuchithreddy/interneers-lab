from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import ProductService
from .services import ProductCategoryService

product_service = ProductService()

@api_view(['GET'])
def list_products(request):
    print("I am trying to request")
    page = int(request.GET.get('page', 1))
    page_size = int ( request.GET.get('page_size', 5) )
    products = product_service.list_products(page, page_size)
    print(products)
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


category_service = ProductCategoryService()

@api_view(['GET'])
def list_categories(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 5))
    categories = category_service.list_category(page, page_size)
    return Response(categories)

@api_view(['GET'])
def list_category_products(request,category_id):
    
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 5))
    products = category_service.list_category_products(category_id,page,page_size)
    return Response(products)


@api_view(['POST'])
def create_category(request):
    try:
        category = category_service.create_category(request.data)
        return Response(category.to_json(), status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_category(request, category_id):
    try:
        category = category_service.get_category(category_id)
        return Response(category.to_json())
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_category(request, category_id):
    try:
        category = category_service.update_category(category_id, request.data)
        return Response(category.to_json())
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_category(request, category_id):
    if category_service.delete_category(category_id):
        return Response({'message': 'Category deleted'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
