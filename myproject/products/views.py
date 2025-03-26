from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from uuid import uuid4

# In-memory storage
PRODUCTS = []

# Fetch all products
@api_view(['GET'])
def list_products(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    result_page = paginator.paginate_queryset(PRODUCTS,request)

    return paginator.get_paginated_response(result_page)


# Create a new product
@api_view(['POST'])
def create_product(request):
    data = request.data
    if 'name' not in data or 'price' not in data or 'quantity' not in data:
        return Response({'error': 'Name, price, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if data["price"]<0:
        return Response({'error':"Price can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
    
    if data["quantity"]<0:
        return Response({'error':"Quantity can't be negative"}, status=status.HTTP_400_BAD_REQUEST)

    product = {
        "id": str(uuid4()),  # Generate a unique ID
        "name": data["name"],
        "description": data.get("description", ""),
        "category": data.get("category", ""),
        "price": data["price"],
        "brand": data.get("brand", ""),
        "quantity": data["quantity"]
    }
    PRODUCTS.append(product)
    return Response(product, status=status.HTTP_201_CREATED)

# Fetch a single product by ID
@api_view(['GET'])
def get_product(request, product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(product)


# Update a product
@api_view(['PUT'])
def update_product(request, product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    if 'name' not in data or 'price' not in data or 'quantity' not in data:
        return Response({'error': 'Name, price, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if data["price"]<0:
        return Response({'error':"Price can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
    
    if data["quantity"]<0:
        return Response({'error':"Quantity can't be negative"}, status=status.HTTP_400_BAD_REQUEST)
    
    if data["id"]!=product_id:
        return Response({'error':"Product id sent in json data is different"}, status=status.HTTP_400_BAD_REQUEST)

    for key, value in request.data.items():
        if key in product and key!="id": 
            product[key] = value
    
    return Response(product)

# Delete a product
@api_view(['DELETE'])
def delete_product(request, product_id):
    global PRODUCTS
    PRODUCTS = [p for p in PRODUCTS if p["id"] != product_id]
    return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
