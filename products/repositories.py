from mongoengine import DoesNotExist
from .models import Product

class ProductRepository:
    def get(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except DoesNotExist:
            return None

    def create(self, product_data):
        product = Product(**product_data)
        product.save()
        return product

    def update(self, product_id, product_data):
        product = self.get(product_id)
        if product:
            for key, value in product_data.items():
                if key != 'id':
                    setattr(product, key, value)
            product.save()
        return product

    def delete(self, product_id):
        product = self.get(product_id)
        if product:
            product.delete()
            return True
        return False
    
    def list(self, page=1, page_size=5):
        # Calculate the number of documents to skip
        skip_count = (page - 1) * page_size

        # Fetch paginated products using skip and limit
        products = Product.objects.skip(skip_count).limit(page_size)

        # Get the total count of documents in the collection
        total_count = Product.objects.count()

        # Calculate total pages
        total_pages = (total_count + page_size - 1) // page_size

        # Check if the paginated result is empty
        if not products:
            return {"data": [], "has_next_page": False, "page": page, "total_pages": total_pages}

        # Determine if there's a next page
        has_next_page = page < total_pages

        # Return paginated response
        return {
            "data": [product.to_json() for product in products],
            "has_next_page": has_next_page,
            "page": page,
            "total_pages": total_pages,
            "total_items": total_count,
        }