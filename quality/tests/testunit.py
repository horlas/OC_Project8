from django.test import TestCase
from unittest.mock import patch, MagicMock
from quality.methods import *
import requests
import json
from quality.tests.test_set import *


#test tests!
class MyTest(TestCase):
    def test_is_even(self):
        self.assertTrue(is_even(2))
        self.assertFalse(is_even(1))
        self.assertEqual(is_even(0), True)


class MyTestCase(TestCase):
    '''Here is a parent class with custom global setup'''
    def setUp(self):
        '''we call the global setup from test_set.py'''
        self.results = FAKE_RESULTS['products']
        self.products = FAKE_PRODUCTS #return of data_process
        self.url = FAKE_URL
        self.cat = FAKE_CAT
        self.substituts = FAKE_RETURN_BESTSUBSTITUT


class QueryOffTest(MyTestCase):
    def test_data_process_results(self):
        '''we tested that data_process returns a list of 6 products, containing 5 items,
         with the following data'''

        products = self.results
        self.assertEqual(data_process(products).__len__(), 6)
        self.assertEqual(data_process(products)[0].__len__(), 5)
        self.assertEqual(data_process(products)[0]['product_name'], 'Nutella')
        self.assertEqual(data_process(products)[1]['img'], 'https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.100.jpg')
        self.assertEqual(data_process(products)[2]['url'], 'https://fr.openfoodfacts.org/produit/3017620401473/nutella-ferrero')
        self.assertEqual(data_process(products)[3]['category'], 'Pâtes à tartiner aux noisettes et au cacao')
        self.assertEqual(data_process(products)[4]['nutriscore'], 'E')

    def test_query_off(self):
        '''the function query_off must return a status_200 and processed datas'''
        response = requests.get(self.url)
        products = data_process(self.results) # the return of query_off
        self.assertEqual(response.status_code, 200)
        self.assertEqual(products, self.products)

    def test_best_substitut(self):
        '''the function should returns with parameters cat = FAKE_CAT a list.
        This list should have a lenght=18.
        And the data_process of this list should have 6 products, the first one with a nutriscore "A"
        and the last one with a nutriscore B'''

        #this test should fail if the OpenfoodFacts database changes. The test set (FAKE_RETURN_BESTSUBSTITUT will no longer be valid

        cat = self.cat
        data = best_substitut(cat)
        self.assertEqual(len(data) , 6)
        self.assertEqual(data[0]['nutriscore'], 'A')
        self.assertEqual(data[5]['nutriscore'] , 'C')
        self.assertEqual(data, self.substituts)



    # an other way to do that
    @patch('requests.get')#la fonction que l'on souhaite partcher
    def test_request_off(self, mock_requests_get):
        mock_requests_get.return_value = MagicMock(status_code=200, response=FAKE_RESULTS)
        request_off(self.cat,'A')
