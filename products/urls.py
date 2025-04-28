from django.urls import path
from .views import create_product, get_product, list_products, update_product, delete_product
from .views import create_category, get_category, list_categories, update_category, delete_category , list_category_products

urlpatterns = [
    path('products/create/', create_product, name='create_product'),
    path('products/<str:product_id>/', get_product, name='get_product'),
    path('products/', list_products, name='list_products'),
    path('products/<str:product_id>/update/', update_product, name='update_product'),
    path('products/<str:product_id>/delete/', delete_product, name='delete_product'),

    path('categories/create/', create_category, name='create_category'),
    path('categories/<str:category_id>/', get_category, name='get_category'),
    path('categories/', list_categories, name='list_categories'),
    path('categories/<str:category_id>/update/', update_category, name='update_category'),
    path('categories/<str:category_id>/delete/', delete_category, name='delete_category'),
    path('categories/<str:category_id>/products/', list_category_products, name='list_category_products'),

]
