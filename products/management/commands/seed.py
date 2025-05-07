# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
import random
from products.models import Product, ProductCategory
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

# to run this there are 2 modes refresh and clear
# refresh clears the existing data and seeds the new data
# clear just only clears the data
# to run the code go the the root and use : python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Seed mode: 'refresh' clears existing data and creates new sample data, 'clear' only removes existing data.")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the Product and category data"""
    logger.info("Deleting products and categories instances")
    Product.objects.all().delete()
    ProductCategory.objects.all().delete()
    logger.info("Deleted products and categories instances")


def create_categories():
    """Creates category objects with random data"""
    logger.info("Creating category")
    
    categories = [
        {"name": "Laptops", "description": "Portable computers for work and entertainment"},
        {"name": "Smartphones", "description": "Mobile devices with advanced features"},
        {"name": "Tablets", "description": "Touchscreen mobile computers"},
        {"name": "Accessories", "description": "Add-ons for electronic devices"},
        {"name": "Audio", "description": "Sound equipment and accessories"}
    ]
    
    category_data = random.choice(categories)
    created_category = ProductCategory(
        name=category_data["name"],
        description=category_data["description"]
    )
    created_category.save()
    logger.info(f"Category created: {created_category.name}")
    return created_category

def create_products(categories=None):
    """Creates product instances with random data linked to categories"""
    
    logger.info("Creating product")
    if not categories:
        # Get all categories or create one if none exist
        categories = list(ProductCategory.objects.all())
        if not categories:
            categories = [create_categories()]
    
    products = [
        {"name": "Dell XPS", "description": "Premium ultrabook with InfinityEdge display", "brand": "Dell"},
        {"name": "Lenovo ThinkPad", "description": "Business laptop with excellent keyboard", "brand": "Lenovo"},
        {"name": "MacBook Pro", "description": "Apple's professional laptop", "brand": "Apple"},
        {"name": "iPhone 14", "description": "Apple's flagship smartphone", "brand": "Apple"},
        {"name": "Galaxy S23", "description": "Samsung's premium smartphone", "brand": "Samsung"},
        {"name": "iPad Pro", "description": "Professional tablet with M2 chip", "brand": "Apple"},
        {"name": "Surface Pro", "description": "Microsoft's versatile 2-in-1 device", "brand": "Microsoft"}
    ]
    
    product_data = random.choice(products)
    product = Product(
        name=product_data["name"],
        description=product_data["description"],
        price=Decimal(str(random.uniform(499.99, 1999.99))).quantize(Decimal('0.01')),
        brand=product_data["brand"],
        quantity=random.randint(0, 100),
        product_category= (random.choice(categories)).pk
    )
    product.save()
    logger.info(f"Product created: {product.name} ({product.brand})")
    return product

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Create 5 categories
    categories = []
    for i in range(5):
        categories.append(create_categories())
    
    # Create 15 products
    for i in range(15):
        create_products(categories)
    
    self.stdout.write(self.style.SUCCESS(f'Created 5 categories and 15 products'))