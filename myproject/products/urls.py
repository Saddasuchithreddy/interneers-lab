from django.urls import path
from .views import create_product, get_product, list_products, update_product, delete_product

urlpatterns = [
    path('create/', create_product, name='create_product'),
    path('<str:product_id>/', get_product, name='get_product'),
    path('', list_products, name='list_products'),
    path('<str:product_id>/update/', update_product, name='update_product'),
    path('<str:product_id>/delete/', delete_product, name='delete_product'),
]
