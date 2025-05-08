import os
import logging
from bson import ObjectId
from products import models
from django.urls import reverse
from mongoengine import connection
from rest_framework import status
from rest_framework.test import APITestCase

logging.basicConfig(filename = "category_integration_test.log",level = logging.INFO)
logger = logging.getLogger(__name__)

logger.info("started")

# to run this program , at the root use : 1. $env:USE_LOCAL_MONGO = "true" , this line ensures the useage of the local mongodb server
#                                         2. python manage.py test products.tests.integration.category_test  
#                                         3. $env:USE_LOCAL_MONGO = "false"

class ProductIntegrationTest(APITestCase):
    
    def setUp(self):
        # first creating category for consistency of the product_category for product
        self.category = models.ProductCategory(
            name = "category1",
            description = "description1"
        )
        self.category.save()
        
        self.product = models.Product(
            name = "name1",
            price = 10,
            quantity = 10,
            brand = "brand1",
            product_category = self.category.pk
        )
        self.product.save()
        
        return super().setUp()
    
    def tearDown(self):
        models.Product.objects.delete()
        models.ProductCategory.objects.delete()
        return super().tearDown()
    
    @classmethod
    def tearDownClass(cls):
        os.environ["USE_LOCAL_MONGO"] = "false"
        logger.info("finished")
        return super().tearDownClass()
    
    def test_database_connection(self):
    
        # Geting connection information from mongoengine
        db = connection.get_db()
        conn = connection.get_connection()
        
        # Log connection info
        logger.info(f"Database name: {db.name}")
        logger.info(f"Database host: {conn.address[0]}:{conn.address[1]}")
        
        self.assertEqual(db.name, 'mydb')
        self.assertEqual(conn.address[0], 'localhost')
    
    def test_list_categories(self):
        
        url = reverse('list_categories')
        
        response = self.client.get(url)
        
        self.assertIn('results',response.data)
        self.assertIn('count',response.data)
        
        logger.info(response.data["results"])
        
        self.assertEqual(len(response.data["results"]),1)
        
        # Check the first item in the results
        self.assertEqual(response.data["results"][0]["name"], "category1")
        self.assertEqual(response.data["results"][0]["description"], "description1")
        
    def test_create_category(self):
        url = reverse('create_category')
        
        data = {
            "name" : "name2",
            "description" : "description2",
        }
        
        response = self.client.post(url,data)
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"],"name2")
        
        # checking the existance of the product in the database
        self.assertEqual(models.ProductCategory.objects.filter(id=response.data['id']).count(),1)
    
    def test_incorrect_create_category(self):
        url = reverse('create_category')
        
        data = {
            "description" : "description3",
        }
        
        response = self.client.post(url,data)
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_get_category(self):
        
        url = reverse('get_category', kwargs = {'category_id' : str(self.category.pk)})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["name"],"category1")
    
    def test_non_existent_get_category(self):
        
        url = reverse('get_category', kwargs = {'category_id' : "000000000000000000000000"})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def test_update_category(self):
        
        url = reverse('update_category', kwargs = {'category_id' : str(self.category.pk)})
        
        data = {
            "name" : "name22",
            "description" : "description22",
        }
        response = self.client.put(url,data,format = "json")
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["name"],"name22")
        self.assertEqual(response.data["description"],"description22")
        
    def test_delete_category(self):
        
        url = reverse('delete_category', kwargs = {'category_id' : str(self.category.pk)})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.ProductCategory.objects.filter(id=self.category.pk).count(),0)
    
    def test_list_category_products(self):
        url = reverse('list_category_products', kwargs={"category_id":str(self.category.pk)})
        
        response = self.client.get(url)
        
        # Check the first item in the results
        self.assertEqual(response.data["results"][0]["name"], "name1")
        self.assertEqual(response.data["results"][0]["brand"], "brand1")
        
    
