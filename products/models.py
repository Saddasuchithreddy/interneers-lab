from mongoengine import Document, StringField, DecimalField, IntField

class Product(Document):
    name = StringField(max_length = 50)
    description = StringField(max_length = 400)
    category = StringField(max_length=50)
    price = DecimalField(max_digits = 10,decimal_places=2)
    brand = StringField(max_length=50)
    quantity = IntField(default = 0)

    def __str__(self):
        return self.name
