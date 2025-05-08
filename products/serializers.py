from rest_framework import serializers
from .models import ProductCategory
from bson import ObjectId
from bson.errors import InvalidId

class ProductSerializers(serializers.Serializer):
    
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=400, required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    brand = serializers.CharField(max_length=50)
    quantity = serializers.IntegerField()
    
    product_category = serializers.CharField(required=True)
    
    def validate_quantity (self, value):
        if value<0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value
    
    def validate_price (self, value):
        if value<0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_brand ( self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("Brand cannot be empty")
        return value
        
    def validate_product_category(self, value):
        try:
            # converting to string first to ensure consistent handling
            return ObjectId(str(value))
        except (InvalidId):
            raise serializers.ValidationError("Invalid category ID")
        
    # the purpose of the below funciton overiding is correct handling of the product_category serialization 
    # ( because by defaut ObjectId are not JSON-serializable )    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key,value in data.items():
            if isinstance(value,ObjectId):
                data[key] = str(value)
        return data
    
class ProductCategorySerializers( serializers.Serializer ):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length = 50)
    description = serializers.CharField(max_length = 400)
    
