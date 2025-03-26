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






# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework.pagination import PageNumberPagination

# from uuid import uuid4

# # In-memory storage
# PRODUCTS = []

# # Fetch all products
# @api_view(['GET'])
# def list_products(request):
#     paginator = PageNumberPagination()
#     paginator.page_size = 5
#     result_page = paginator.paginate_queryset(PRODUCTS,request)

#     return paginator.get_paginated_response(result_page)


# # Create a new product
# @api_view(['POST'])
# def create_product(request):
#     data = request.data
#     if 'name' not in data or 'price' not in data or 'quantity' not in data:
#         return Response({'error': 'name, price, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["price"]<0:
#         return Response({'error':"Price can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["quantity"]<0:
#         return Response({'error':"Quantity can't be negative"}, status=status.HTTP_400_BAD_REQUEST)

#     product = {
#         "id": str(uuid4()),  # Generate a unique ID
#         "name": data["name"],
#         "description": data.get("description", ""),
#         "category": data.get("category", ""),
#         "price": data["price"],
#         "brand": data.get("brand", ""),
#         "quantity": data["quantity"]
#     }
#     PRODUCTS.append(product)
#     return Response(product, status=status.HTTP_201_CREATED)

# # Fetch a single product by ID
# @api_view(['GET'])
# def get_product(request, product_id):
#     product = next((p for p in PRODUCTS if p["id"] == product_id), None)
#     if not product:
#         return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
#     return Response(product)


# # Update a product
# @api_view(['PUT'])
# def update_product(request, product_id):
#     product = next((p for p in PRODUCTS if p["id"] == product_id), None)
#     if not product:
#         return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

#     data = request.data
#     if 'name' not in data or 'price' not in data or 'quantity' not in data:
#         return Response({'error': 'Name, price, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["price"]<0:
#         return Response({'error':"Price can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["quantity"]<0:
#         return Response({'error':"Quantity can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["id"]!=product_id:
#         return Response({'error':"Product id sent in json data is different"}, status=status.HTTP_400_BAD_REQUEST)

#     for key, value in request.data.items():
#         if key in product and key!="id": 
#             product[key] = value
    
#     return Response(product)

# # Delete a product
# @api_view(['DELETE'])
# def delete_product(request, product_id):
#     global PRODUCTS
#     PRODUCTS = [p for p in PRODUCTS if p["id"] != product_id]
#     return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)


# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.pagination import PageNumberPagination
# from .serializer import ProductSerializer
# from .models import Product

# from uuid import uuid4

# # In-memory storage
# PRODUCTS = []


# class ProductManager(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     @action(detail=True, methods=['GET'])
#     def list_products(request):
#         paginator = PageNumberPagination()
#         paginator.page_size = 5
#         result_page = paginator.paginate_queryset(PRODUCTS,request)

#         return paginator.get_paginated_response(result_page)
    
#     @action(detail=True,methods=['POST'])
#     def create_product(request):
#         data = request.data
#         if 'name' not in data or 'price' not in data or 'quantity' not in data:
#             return Response({'error': 'Name, price, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         if data["price"]<0:
#             return Response({'error':"Price can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
        
#         if data["quantity"]<0:
#             return Response({'error':"Quantity can't be negative"}, status=status.HTTP_400_BAD_REQUEST)

#         product = {
#             "id": str(uuid4()),  # Generate a unique ID
#             "name": data["name"],
#             "description": data.get("description", ""),
#             "category": data.get("category", ""),
#             "price": data["price"],
#             "brand": data.get("brand", ""),
#             "quantity": data["quantity"]
#         }
#         PRODUCTS.append(product)
#         return Response(product, status=status.HTTP_201_CREATED)
    
#     @action(detail=True,methods=['GET'])
#     def get_product(request, product_id):
#         product = next((p for p in PRODUCTS if p["id"] == product_id), None)
#         if not product:
#             return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
#         return Response(product)
    
#     @action(detail=True,methods=['PUT'])
#     def update_product(request, product_id):
#         product = next((p for p in PRODUCTS if p["id"] == product_id), None)
#         if not product:
#             return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

#         data = request.data
#         if 'name' not in data or 'price' not in data or 'quantity' not in data:
#             return Response({'error': 'Name, price, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         if data["price"]<0:
#             return Response({'error':"Price can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
        
#         if data["quantity"]<0:
#             return Response({'error':"Quantity can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
        
#         if data["id"]!=product_id:
#             return Response({'error':"Product id sent in json data is different"}, status=status.HTTP_400_BAD_REQUEST)

#         for key, value in request.data.items():
#             if key in product and key!="id": 
#                 product[key] = value
        
#         return Response(product)

#     @action(detail=True,methods=['DELETE'])
#     def delete_product(request, product_id):
#         global PRODUCTS
#         PRODUCTS = [p for p in PRODUCTS if p["id"] != product_id]
#         return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)

# # Fetch all products
# @api_view(['GET'])
# def list_products(request):
#     paginator = PageNumberPagination()
#     paginator.page_size = 5
#     result_page = paginator.paginate_queryset(PRODUCTS,request)

#     return paginator.get_paginated_response(result_page)


# # Create a new product
# @api_view(['POST'])
# def create_product(request):
#     data = request.data
#     if 'name' not in data or 'price' not in data or 'quantity' not in data:
#         return Response({'error': 'Name, price, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["price"]<0:
#         return Response({'error':"Price can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["quantity"]<0:
#         return Response({'error':"Quantity can't be negative"}, status=status.HTTP_400_BAD_REQUEST)

#     product = {
#         "id": str(uuid4()),  # Generate a unique ID
#         "name": data["name"],
#         "description": data.get("description", ""),
#         "category": data.get("category", ""),
#         "price": data["price"],
#         "brand": data.get("brand", ""),
#         "quantity": data["quantity"]
#     }
#     PRODUCTS.append(product)
#     return Response(product, status=status.HTTP_201_CREATED)

# # Fetch a single product by ID
# @api_view(['GET'])
# def get_product(request, product_id):
#     product = next((p for p in PRODUCTS if p["id"] == product_id), None)
#     if not product:
#         return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
#     return Response(product)


# # Update a product
# @api_view(['PUT'])
# def update_product(request, product_id):
#     product = next((p for p in PRODUCTS if p["id"] == product_id), None)
#     if not product:
#         return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

#     data = request.data
#     if 'name' not in data or 'price' not in data or 'quantity' not in data:
#         return Response({'error': 'Name, price, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["price"]<0:
#         return Response({'error':"Price can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["quantity"]<0:
#         return Response({'error':"Quantity can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if data["id"]!=product_id:
#         return Response({'error':"Product id sent in json data is different"}, status=status.HTTP_400_BAD_REQUEST)

#     for key, value in request.data.items():
#         if key in product and key!="id": 
#             product[key] = value
    
#     return Response(product)

# # Delete a product
# @api_view(['DELETE'])
# def delete_product(request, product_id):
#     global PRODUCTS
#     PRODUCTS = [p for p in PRODUCTS if p["id"] != product_id]
#     return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
