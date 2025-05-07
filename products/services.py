from .repositories import *

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def list_products(self):
        return self.repository.list()
    
    def create_product(self, product_data):
        if 'name' not in product_data or 'price' not in product_data or 'quantity' not in product_data or 'brand' not in product_data:
            raise ValueError('Name, price, quantity and brand are required')
        
        if product_data['price'] < 0 or product_data['quantity'] < 0:
            raise ValueError('Price and quantity cannot be negative')
        
        return self.repository.create(product_data)
    
    def get_product(self, product_id):
        product = self.repository.get(product_id)
        if not product:
            raise ValueError('Product not found')
        return product

    def update_product(self, product_id, product_data):
        
        if 'name' not in product_data or 'price' not in product_data or 'quantity' not in product_data or 'brand' not in product_data:
            raise ValueError('Name, price, quantity and brand are required')
        
        if product_data['price'] < 0 or product_data['quantity'] < 0:
            raise ValueError('Price and quantity cannot be negative')
        
        return self.repository.update(product_id, product_data)

    def delete_product(self, product_id):
        return self.repository.delete(product_id)

class ProductCategoryService:
    def __init__(self):
        self.repository = ProductCategoryRepository()

    def list_category(self):
        return self.repository.list()
    
    def list_category_products(self,category_id):
        return self.repository.list_products(category_id)

    def create_category(self, category_data):
        
        if 'name' not in category_data :
            raise ValueError('Name is required')
        
        return self.repository.create(category_data)

    def get_category(self, category_id):
        category = self.repository.get(category_id)
        if not category:
            raise ValueError('Category not found')
        return category

    def update_category(self, category_id, category_data):
        if 'name' not in category_data :
            raise ValueError('Name is required')
        return self.repository.update(category_id, category_data)

    def delete_category(self, category_id):
        return self.repository.delete(category_id)
