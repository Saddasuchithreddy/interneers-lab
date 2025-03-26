from .repositories import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def list_products(self, page=1, page_size=5):
        return self.repository.list(page, page_size)

    def create_product(self, product_data):
        
        if 'name' not in product_data or 'price' not in product_data or 'quantity' not in product_data:
            raise ValueError('Name, price, and quantity are required')
        if product_data['price'] < 0 or product_data['quantity'] < 0:
            raise ValueError('Price and quantity cannot be negative')
        
        return self.repository.create(product_data)

    def get_product(self, product_id):
        product = self.repository.get(product_id)
        if not product:
            raise ValueError('Product not found')
        return product

    def update_product(self, product_id, product_data):
        if 'name' not in product_data or 'price' not in product_data or 'quantity' not in product_data:
            raise ValueError('Name, price, and quantity are required')
        if product_data['price'] < 0 or product_data['quantity'] < 0:
            raise ValueError('Price and quantity cannot be negative')
        if product_data['id'] != product_id:
            raise ValueError('Product id sent in json data is different')
        return self.repository.update(product_id, product_data)

    def delete_product(self, product_id):
        return self.repository.delete(product_id)
