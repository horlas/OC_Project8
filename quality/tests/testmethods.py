from django.test import TestCase
from unittest.mock import patch , MagicMock
from quality.methods import *
import requests
import json
from quality.tests.fake import *


# test tests!
class MyTest(TestCase):
    def test_is_even(self):
        self.assertTrue(is_even(2))
        self.assertFalse(is_even(1))
        self.assertEqual(is_even(0) , True)


class MyTestCase(TestCase):
    '''Here is a parent class with custom global setup'''

    def setUp(self):
        '''we call the global setup from fake.py'''
        self.results = FAKE_RESULTS['products']
        self.data = FAKE_RESULTS_BETA
        self.products = FAKE_PRODUCTS  # return of data_process
        self.url = FAKE_URL
        self.cat = FAKE_CAT
        self.substituts = FAKE_RETURN_BESTSUBSTITUT


class QueryOffTest(MyTestCase):
    def test_data_process_results(self):
        ''' we tested that data_process returns a list of the first 6 products with good value among 20 products,
         each product containing 7 items, with the following data '''

        # self data is a sample of datas:
        products = self.data

        # the first item have a name with "," : we test that data_process remove comas from the name
        self.assertEqual(products[0]['product_name'] , 'Tortellini Pesto, Basilic & Pignons')
        self.assertEqual(data_process(products)[0]['product_name'] , 'Tortellini Pesto')

        # the second item is a product without name
        self.assertRaises(KeyError, lambda: products[1]['product_name'])
        # and we must remove it
        # the product code before data_process
        self.assertEqual(products[1]['url'], 'https://fr.openfoodfacts.org/produit/2020203799998/speculos-hema')
        # after data_process it doesn't exist any more
        self.assertNotEqual(data_process(products)[1]['url'] ,
                            'https://fr.openfoodfacts.org/produit/2020203799998/speculos-hema')

        # the fifth item has no field 'category"
        self.assertRaises(KeyError , lambda: products[5]['categories'])
        # and we must remove it
        # the product code before data_process
        self.assertEqual(products[5]['product_name'] , 'Merveilleux speculos X4')
        # after data_process it doesn't exist any more
        self.assertNotEqual(data_process(products)[1]['product_name'] , 'Merveilleux speculos X4')


        # the third has no field image_front_url :
        self.assertRaises(KeyError , lambda: products[2]['image_front_url'])
        # and we must remove it
        # the product code before data_process
        self.assertEqual(products[2]['product_name'] , 'Gü-yorkais au speculos')
        # after data_process it doesn't exist any more
        self.assertNotEqual(data_process(products)[2]['product_name'] , 'Gü-yorkais au speculos')

        # data_process must return 6 items
        self.assertEqual(data_process(products).__len__() , 6)

        # each item must have 7 fields
        self.assertEqual(data_process(products)[0].__len__() , 7)

        # test some stuff among the list
        self.assertEqual(data_process(products)[0]['product_name'], 'Tortellini Pesto')
        self.assertEqual(data_process(products)[1]['img'], 'https://static.openfoodfacts.org/images/products/322/847/003/8249/front_fr.10.400.jpg')
        self.assertEqual(data_process(products)[2]['url'], 'https://fr.openfoodfacts.org/produit/2020203799998/speculos-hema')
        self.assertEqual(data_process(products)[3]['category'], 'Glaces au spéculoos')
        self.assertEqual(data_process(products)[4]['nutriscore'], 'C')
        self.assertEqual(data_process(products)[5]['img_nutrition'], 'https://static.openfoodfacts.org/images/products/356/488/402/0532/nutrition_fr.20.400.jpg')
        self.assertEqual(data_process(products)[0]['magasins'], 'Carrefour Market,Franprix')

    def test_query_off(self):
        '''the function query_off must return a status_200 and processed datas'''
        response = requests.get(self.url)
        products = data_process(self.results)  # the return of query_off function
        self.assertEqual(response.status_code , 200)
        self.assertEqual(products , self.products)

    def test_best_substitut(self):
        '''the function should returns with parameters cat = FAKE_CAT a list.
        This list should have a lenght=18.
        And the data_process of this list should have 6 products, the first one with a nutriscore "A"
        and the last one with a nutriscore B'''

        # this test should fail if the OpenfoodFacts database changes. The test set (FAKE_RETURN_BESTSUBSTITUT will no longer be valid

        cat = self.cat
        data = best_substitut(cat)
        self.assertEqual(len(data) , 6)
        self.assertEqual(data[0]['nutriscore'] , 'A')
        self.assertEqual(data[5]['nutriscore'] , 'C')
        self.assertEqual(data , self.substituts)

    # an other way to do that
    @patch('requests.get')  # la fonction que l'on souhaite partcher
    def test_request_off(self , mock_requests_get):
        mock_requests_get.return_value = MagicMock(status_code=200 , response=FAKE_RESULTS)
        request_off(self.cat , 'A')
