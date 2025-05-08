from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .services import ProductService,ProductCategoryService

from .serializers import ProductSerializers,ProductCategorySerializers

product_service = ProductService()

class ProductPagination(PageNumberPagination):  
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# @api_view(['GET'])
# def list_products(request):
#     print("I am trying to request")
#     page = int(request.GET.get('page', 1))
#     page_size = int ( request.GET.get('page_size', 5) )
#     paginated_response = product_service.list_products(page, page_size)
    
#     # Extraction and Serialization of the data before sending
#     product_data = paginated_response.get('data',[])
#     serialized_products = ProductSerializers(product_data, many = True)
    
#     paginated_response['data'] = serialized_products.data
    
#     # print(products)
#     return Response(paginated_response)

@api_view(['GET'])
def list_products(request):
    
    products = product_service.list_products()
    
    # Create a paginator instance
    paginator = ProductPagination()
    
    # Paginate the queryset
    paginated_products = paginator.paginate_queryset(products, request)
    
    # Serialize the paginated data
    serializer = ProductSerializers(paginated_products, many=True)
    
    # Return the paginated response
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def create_product(request):
    
    # serialize the data , verify and send to the below layers
    serialized_obj = ProductSerializers(data=request.data)
    if serialized_obj.is_valid():
        try:
            product = product_service.create_product(serialized_obj.validated_data)
            
            serialized_response = ProductSerializers(product)
            
            # here we can use to_json() for correct json serialization also ( but not recommended )
            return Response(serialized_response.data, status=status.HTTP_201_CREATED)
        
        # service layer error handling
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serialized_obj.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_product(request, product_id):
    try:
        product = product_service.get_product(product_id)
        serialized_product = ProductSerializers(product)
        
        return Response(serialized_product.data, status = status.HTTP_200_OK)
    
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_product(request, product_id):
    try:
        # First get the existing product
        product = product_service.get_product(product_id)
        
        # Validate the incoming data with the serializer
        serialized_obj = ProductSerializers(product, data=request.data, partial=True)
        if serialized_obj.is_valid():
            # Update the product with validated data
            updated_product = product_service.update_product(product_id, serialized_obj.validated_data)
            
            # Serialize the response
            serialized_response = ProductSerializers(updated_product)
            return Response(serialized_response.data, status=status.HTTP_200_OK)
        else:
            # Return validation errors if any
            return Response(serialized_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, product_id):
    if product_service.delete_product(product_id):
        return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

category_service = ProductCategoryService()

class ProductCategoryPagination(PageNumberPagination):
    page_size = 5 # this is default
    page_size_query_param = 'page_size'
    max_page_size = 100
    

@api_view(['GET'])
def list_categories(request):

    # Get all the categories
    categories = category_service.list_category()
    
    # Create a paginator instance
    paginator = ProductCategoryPagination()
    
    # Paginate the queryset
    paginated_categories = paginator.paginate_queryset(categories,request)
    
    # Serialize the paginated data
    serialized_categories = ProductCategorySerializers( paginated_categories, many = True )
    
    # Return the paginated response
    return paginator.get_paginated_response(serialized_categories.data)

@api_view(['GET'])
def list_category_products(request,category_id):

    # Get all the products which belong to the requested category
    products = category_service.list_category_products(category_id)
    
    # Create a paginator instance
    paginator = ProductPagination()
    
    # Paginate the queryset
    paginated_products = paginator.paginate_queryset(products, request)
    
    # Serialize the paginated data
    serialized_products = ProductSerializers(paginated_products, many = True)
    
    # Return the paginated response
    return paginator.get_paginated_response(serialized_products.data)


@api_view(['POST'])
def create_category(request):
    
    # serialize the data , verify and send to the below layers
    serialized_obj = ProductCategorySerializers(data = request.data)
    
    if serialized_obj.is_valid():
        try:
            
            category = category_service.create_category(serialized_obj.validated_data)
            
            serialized_response = ProductCategorySerializers(category)
            
            return Response(serialized_response.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serialized_obj.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_category(request, category_id):
    try:
        
        category = category_service.get_category(category_id)
        serialized_category = ProductCategorySerializers(category)
        return Response(serialized_category.data,status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_category(request, category_id):
    try:
        # First get the existing product
        category = category_service.get_category(category_id)
        
        # Validate the incoming data with the serializer
        serialized_obj = ProductCategorySerializers(data = request.data)

        if serialized_obj.is_valid():
            try:
                # Update the product with validated data
                category = category_service.update_category(category_id,serialized_obj.validated_data)
                
                # Serialize the response
                serialized_response = ProductCategorySerializers(category)
                
                return Response(serialized_response.data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serialized_obj.errors, status = status.HTTP_400_BAD_REQUEST)
        
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_category(request, category_id):
    if category_service.delete_category(category_id):
        return Response({'message': 'Category deleted'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
