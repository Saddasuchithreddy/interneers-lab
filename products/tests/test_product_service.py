import json
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from products import services

# to run this file , at the root use this in the terminal : python -m unittest products.tests.test_product_service

class TestProductService(unittest.TestCase):
    
    # note
    # patch the function which is going to be used in the repository layer, but
    # we have to patch it in the services.py not in repository.py because the funciton list_products is going to use the list function
    #   in the ProductRepository as a local refrence
    @patch("products.services.ProductRepository.list")
    def test_list_products(self,mock_list):
        
        # loading the mock data from the json file
        with open("products/tests/product_data.json","r") as file:
            mock_data = json.load(file)

        # Create mock objects from JSON data
        mock_products = []
        for product in mock_data:
            mock_product = MagicMock()
            mock_product.id = product["id"]
            mock_product.name = product["name"]
            mock_product.price = product["price"]
            mock_product.quantity = product["quantity"]
            mock_product.brand = product["brand"]
            mock_product.product_category = product["product_category"]
            mock_products.append(mock_product)
        
        # Set the return value of the mocked method
        mock_list.return_value = mock_products
        
        # Call the service method
        service = services.ProductService()
        result = service.list_products()
        
        # Assertions
        mock_list.assert_called_once()
        
        self.assertEqual(len(result),len(mock_data))
        for i,product in enumerate(mock_data):
            self.assertEqual(result[i].id,product["id"])
            self.assertEqual(result[i].name,product["name"])
    
    # These are the various test cases which will be tested with the below test_create_product funciton only
    # using parameterized.expand we can test multiple cases at once
    @parameterized.expand([
        ("valid", {"name": "name3", "brand": "brand3", "quantity": 30,"price":30}, False),
        ("missing_name", {"brand": "brand3", "quantity": 30,"price":30}, True),
        ("missing_brand", {"name": "name3", "quantity": 30,"price":30}, True),
        ("missing_quantity", {"name": "name3", "brand": "brand3","price":30}, True),
        ("negative_quantity", {"name": "name3", "brand": "brand3", "quantity": -30,"price":30}, True),
        ("negative_price", {"name": "name3", "brand": "brand3", "quantity": 30,"price":-30}, True),
    ])
    
    @patch("products.services.ProductRepository.create")
    def test_create_product(self,name,input_data,should_raise,mock_create):
        
        service = services.ProductService()
        
        if should_raise:
            with self.assertRaises(ValueError):
                service.create_product(input_data)
            mock_create.assert_not_called()
        
        else:
            # Set the return value of the mocked method
            mock_create.return_value = {"id":1,**input_data}
            
            # Call the service method
            result = service.create_product(input_data)
            
            # Assertions
            mock_create.assert_called_once()
            
            self.assertEqual(result["id"],1)
            self.assertEqual(result["name"],input_data["name"])
            

    @parameterized.expand([
        ("valid id", 1, {"name": "name3", "brand": "brand3", "quantity": 30,"price":30}, False),
        ("invalid id", 4, None, True)
    ])
    
    @patch("products.services.ProductRepository.get")
    def test_get_product(self, name, input_id, output_data, should_raise, mock_get_product):
        
        service = services.ProductService()
        
        if should_raise:
            
            mock_get_product.return_value = output_data
            with self.assertRaises(ValueError):
                service.get_product(input_id)
            mock_get_product.assert_called_once_with(input_id)
        
        else:
            mock_get_product.return_value = {"id":input_id,**output_data}
            
            # Call the service method
            result = service.get_product(input_id)
            
            # Assertions
            mock_get_product.assert_called_once_with(input_id)
            
            self.assertEqual(result["id"],input_id)
            self.assertEqual(result["name"],output_data["name"])
    
    @parameterized.expand([
        ("valid", 1, {"name": "name3", "brand": "brand3", "quantity": 30,"price":30}, False),
        ("missing_name", 1,{"brand": "brand3", "quantity": 30,"price":30}, True),
        ("missing_brand", 1,{"name": "name3", "quantity": 30,"price":30}, True),
        ("missing_quantity", 1, {"name": "name3", "brand": "brand3","price":30}, True),
        ("negative_quantity",1 , {"name": "name3", "brand": "brand3", "quantity": -30,"price":30}, True),
        ("negative_price", 1, {"name": "name3", "brand": "brand3", "quantity": 30,"price":-30}, True),
    ])
    
    @patch("products.services.ProductRepository.update")
    def test_update_product(self,name,id,input_data,should_raise,mock_update):
        
        service = services.ProductService()
        
        if should_raise:
            with self.assertRaises(ValueError):
                service.update_product(id,input_data)
            mock_update.assert_not_called()
        
        else:
            # Set the return value of the mocked method
            mock_update.return_value = {"id":id,**input_data}
            
            # Call the service method
            result = service.update_product(id,input_data)
            
            # Assertions
            mock_update.assert_called_once()
            
            self.assertEqual(result["id"],id)
            self.assertEqual(result["name"],input_data["name"])
        
    
    @parameterized.expand([
        ("valid id", 1,True, False),
        ("invalid id", 4,False,True)
    ])
    
    @patch("products.services.ProductRepository.delete")
    def test_delete_product(self, name, input_id, output, should_raise, mock_delete_product):
        
        # output is the "expected" delete function output at the repository layer and should_raise tells whether
        # it is a valid id or invalid id(False means valid id). For a correct test case both should be opposite.
        service = services.ProductService()
        
        if should_raise:
            if output is False:
                mock_delete_product.side_effect = ValueError("Product not found")
            with self.assertRaises(ValueError):
                service.delete_product(input_id)
            mock_delete_product.assert_called_once_with(input_id)
        
        else:
            # Set the return value of the mocked method
            mock_delete_product.return_value = output
            
            # Call the service method
            result = service.delete_product(input_id)
            
            # Assertions
            mock_delete_product.assert_called_once()
            
            self.assertEqual(result,True)
    
if __name__ == "__main__":
    unittest.main(verbosity=0)
