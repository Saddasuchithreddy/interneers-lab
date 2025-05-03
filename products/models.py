from mongoengine import Document, StringField, DecimalField, IntField , ReferenceField
from mongoengine import *

class ProductCategory(Document):
    name = StringField(max_length = 50)
    description = StringField(max_length = 400)

    def __str__(self):
        return self.name

class Product(Document):
    name = StringField(max_length = 50)
    description = StringField(max_length = 400)
    # category = StringField(max_length=50)
    price = DecimalField(max_digits = 10,decimal_places=2)
    brand = StringField(max_length=50)
    quantity = IntField(default = 0)
    product_category = ReferenceField("ProductCategory",reverse_delete_rule=NULLIFY)

    def __str__(self):
        return self.name
    

