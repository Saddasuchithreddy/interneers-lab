import json
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from products import services

# to run this file , at the root use this in the terminal : python -m unittest products.tests.test_category_services

class TestProductCategoryService(unittest.TestCase):
    
    # note
    # patch the function which is going to be used in the repository layer, but
    # we have to patch it in the services.py not in repository.py because the funciton list_category is going to use the list function
    #   in the ProductCategoryRepository as a local refrence
    @patch("products.services.ProductCategoryRepository.list")
    def test_list_category(self,mock_list):
        
        # loading the mock data from the json file
        with open("products/tests/category_data.json","r") as file:
            mock_data = json.load(file)

        # Create mock objects from JSON data
        mock_categories = []
        for category in mock_data:
            mock_category = MagicMock()
            mock_category.id = category["id"]
            mock_category.name = category["name"]
            mock_categories.append(mock_category)
        
        # Set the return value of the mocked method
        mock_list.return_value = mock_categories
        
        # Call the service method
        service = services.ProductCategoryService()
        result = service.list_category()
        
        # Assertions
        mock_list.assert_called_once()
        
        self.assertEqual(len(result),len(mock_data))
        for i,category in enumerate(mock_data):
            self.assertEqual(result[i].id,category["id"])
            self.assertEqual(result[i].name,category["name"])
    
    # These are the various test cases which will be tested with the below test_create_category funciton only
    # using parameterized.expand we can test multiple cases at once
    @parameterized.expand([
        ("valid", {"name": "name", "description": "abc"}, False),
        ("missing_name", {"description": "abc"}, True),
    ])
    
    @patch("products.services.ProductCategoryRepository.create")
    def test_create_category(self,name,input_data,should_raise,mock_create):
        
        service = services.ProductCategoryService()
        
        if should_raise:
            with self.assertRaises(ValueError):
                service.create_category(input_data)
            mock_create.assert_not_called()
        
        else:
            # Set the return value of the mocked method
            mock_create.return_value = {"id":1,**input_data}
            
            # Call the service method
            result = service.create_category(input_data)
            
            # Assertions
            mock_create.assert_called_once()
            
            self.assertEqual(result["id"],1)
            self.assertEqual(result["name"],input_data["name"])
            

    @parameterized.expand([
        ("valid id", 1, {"name": "name3", "description": "abc"}, False),
        ("invalid id", 4, None, True)
    ])
    
    @patch("products.services.ProductCategoryRepository.get")
    def test_get_category(self, name, input_id, output_data, should_raise, mock_get_category):
        
        service = services.ProductCategoryService()
        
        if should_raise:
            
            mock_get_category.return_value = output_data
            with self.assertRaises(ValueError):
                service.get_category(input_id)
            mock_get_category.assert_called_once_with(input_id)
        
        else:
            mock_get_category.return_value = {"id":input_id,**output_data}
            
            # Call the service method
            result = service.get_category(input_id)
            
            # Assertions
            mock_get_category.assert_called_once_with(input_id)
            
            self.assertEqual(result["id"],input_id)
            self.assertEqual(result["name"],output_data["name"])
    
    @parameterized.expand([
        ("valid",1, {"name": "name", "description": "abc"}, False),
        ("missing_name",4, {"description": "abc"}, True),
    ])
    
    @patch("products.services.ProductCategoryRepository.update")
    def test_update_category(self,name,input_id,input_data,should_raise,mock_update):
        
        service = services.ProductCategoryService()
        
        if should_raise:
            with self.assertRaises(ValueError):
                service.update_category(input_id,input_data)
            mock_update.assert_not_called()
        
        else:
            # Set the return value of the mocked method
            mock_update.return_value = {"id":input_id,**input_data}
            
            # Call the service method
            result = service.update_category(input_id,input_data)
            
            # Assertions
            mock_update.assert_called_once()
            
            self.assertEqual(result["id"],1)
            self.assertEqual(result["name"],input_data["name"])
        
    
    @parameterized.expand([
        ("valid id", 1, True, False),
        ("invalid id", 4, False, True)
    ])
    
    @patch("products.services.ProductCategoryRepository.delete")
    def test_delete_category(self, name, input_id, output, should_raise, mock_delete_category):
        
        # output is the "expected" delete function output at the repository layer and should_raise tells whether
        # it is a valid id or invalid id(False means valid id). For a correct test case both should be opposite.
        service = services.ProductCategoryService()
        
        if should_raise:
            if output is False:
                mock_delete_category.side_effect = ValueError("Category not found")
            with self.assertRaises(ValueError):
                service.delete_category(input_id)
            mock_delete_category.assert_called_once_with(input_id)
        
        else:
            # Set the return value of the mocked method
            mock_delete_category.return_value = output
            
            # Call the service method
            result = service.delete_category(input_id)
            
            # Assertions
            mock_delete_category.assert_called_once()
            
            self.assertEqual(result,True)
    
    @parameterized.expand([
        (1),(2),(3)
    ])
    @patch("products.services.ProductCategoryRepository.list_products")
    def test_list_category(self,input_category_id,mock_list_products):
        # loading the mock data from the json file
        with open("products/tests/product_data.json","r") as file:
            mock_data = json.load(file)

        filtered_data = []
        for product in mock_data:
            if product["product_category"] == input_category_id:
                filtered_data.append(product)
        
        # Create mock objects from JSON data
        mocked_products = []
        for product in filtered_data:
            mock_product = MagicMock()
            mock_product.id = product["id"]
            mock_product.name = product["name"]
            mock_product.price = product["price"]
            mock_product.quantity = product["quantity"]
            mock_product.brand = product["brand"]
            mock_product.product_category = product["product_category"]
            mocked_products.append(mock_product)
        
        # Set the return value of the mocked method
        mock_list_products.return_value = mocked_products
        
        # Call the service method
        service = services.ProductCategoryService()
        result = service.list_category_products(input_category_id)
        
        # Assertions
        mock_list_products.assert_called_once()
        
        
        for i,product in enumerate(filtered_data):
            if product["product_category"] == input_category_id:
                self.assertEqual(result[i].id,product["id"])
                self.assertEqual(result[i].name,product["name"])
        self.assertEqual(len(result),len(filtered_data))
        
    
if __name__ == "__main__":
    unittest.main(verbosity=2)
