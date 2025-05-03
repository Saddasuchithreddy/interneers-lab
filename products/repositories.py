from mongoengine import DoesNotExist
from .models import Product, ProductCategory
from bson import ObjectId

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
                if key != 'product_category':
                    setattr(product, key, value)
                elif key == 'product_category':
                    product.product_category = ObjectId(value)
            product.save()
        return product

    def delete(self, product_id):
        product = self.get(product_id)
        if product:
            product.delete()
            return True
        return False

    def list(self):
        return Product.objects.all()

class ProductCategoryRepository:

    def create(self, product_data):
        product = ProductCategory(**product_data)
        product.save()
        return product

    def get(self, category_id):
        try:
            return ProductCategory.objects.get(id=category_id)
        except DoesNotExist:
            return None

    def update(self, category_id, category_data):
        category = self.get(category_id)
        if category:
            for key, value in category_data.items():
                if key != 'id':
                    setattr(category, key, value)
            category.save()
        return category

    def delete(self, category_id):
        category = self.get(category_id)
        if category:
            category.delete()
            return True
        return False

    def list(self):
        return ProductCategory.objects.all()
    
    def list_products(self,category_id):
        return Product.objects(product_category=category_id)


    # old pagenation codes :

        
    
    # def list(self, page=1, page_size=5):
    #     # Calculate the number of documents to skip
    #     skip_count = (page - 1) * page_size

    #     # Fetch paginated products using skip and limit
    #     products = Product.objects.skip(skip_count).limit(page_size)

    #     # Get the total count of documents in the collection
    #     total_count = Product.objects.count()

    #     # Calculate total pages
    #     total_pages = (total_count + page_size - 1) // page_size

    #     # Determine if there's a next page
    #     has_next_page = page < total_pages

    #     # Return paginated response
    #     return {
    #         "data": list(products),
    #         "has_next_page": has_next_page,
    #         "page": page,
    #         "total_pages": total_pages,
    #         "total_items": total_count,
    #     }

    # def list(self, page=1, page_size=5):
    #     # Calculate the number of documents to skip
    #     skip_count = (page - 1) * page_size

    #     # Fetch paginated categories using skip and limit
    #     categories = ProductCategory.objects.skip(skip_count).limit(page_size)

    #     # Get the total count of documents in the collection
    #     total_count = ProductCategory.objects.count()

    #     # Calculate total pages
    #     total_pages = (total_count + page_size - 1) // page_size

    #     # Check if the paginated result is empty
    #     if not categories:
    #         return {"data": [], "has_next_page": False, "page": page, "total_pages": total_pages}

    #     # Determine if there's a next page
    #     has_next_page = page < total_pages

    #     # Return paginated response
    #     return {
    #         "data": [category.to_json() for category in categories],
    #         "has_next_page": has_next_page,
    #         "page": page,
    #         "total_pages": total_pages,
    #         "total_items": total_count,
    #     }
    
    # def list_products(self,category_id, page=1, page_size=5):

    #     # Filter products by category
    #     all_products = Product.objects(product_category=category_id)

    #     # Calculate the number of documents to skip
    #     skip_count = (page - 1) * page_size

    #     # Fetch paginated products using skip and limit
    #     products = all_products.skip(skip_count).limit(page_size)

    #     # Get the total count of documents in this category
    #     total_count = all_products.count()

    #     # Calculate total pages
    #     total_pages = (total_count + page_size - 1) // page_size

    #     # Check if the paginated result is empty
    #     if not products:
    #         return {"data": [], "has_next_page": False, "page": page, "total_pages": total_pages}


    #     # Serialize products into JSON-like format
    #     serialized_products = [
    #         {
    #             "id": str(product.id),
    #             "name": product.name,
    #             "description": product.description if product.description else None,
    #             "category": str(product.product_category.id) if product.product_category else None,
    #             "price": str(product.price),
    #             "brand": product.brand  if product.brand else None,
    #             "quantity": product.quantity,
    #         }
    #         for product in products
    #     ]

    #     # Determine if there's a next page
    #     has_next_page = page < total_pages

    #     # Return paginated response
    #     return {
    #         "data": serialized_products,
    #         "has_next_page": has_next_page,
    #         "page": page,
    #         "total_pages": total_pages,
    #         "total_items": total_count,
    #     }
