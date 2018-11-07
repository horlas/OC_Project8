from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from quality.views import *
from unittest.mock import patch
from quality.tests.fake import *
from django.contrib.sessions.middleware import SessionMiddleware

class MyTestCase(TestCase):
    '''Here is a parent class with custom global setup'''
    def setUp(self):
        '''we call the global setup from fake.py'''
        self.client = Client()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

        self.choices = FAKE_DATA_USER_CHOICES

        self.factory = RequestFactory()

        self.record_selected_session = ['selected_name', 'selected_category', 'selected_img', 'selected_nutriscore', 'selected_url']
        self.record_substitut_session = ['substitut_name', 'substitut_category', 'substitut_img', 'substitut_nutriscore',
                          'substitut_url']
        self.p_selected = FAKE_DATA_SELECTED_PRODUCT

class AccueilTest(MyTestCase):
    def test_accueil(self):
        request = self.factory.get('')
        response = accueil(request)
        self.assertEqual(response.status_code , 200)

class CreditsTest(MyTestCase):
    def test_credits(self):
        request = self.factory.get('/quality/credits/')
        response = credits(request)
        self.assertEqual(response.status_code , 200)

class QueryDataTest(MyTestCase):
    def test_query_data(self):
        request = self.factory.get('/quality/query_data/')
        response = query_data(request)
        self.assertEqual(response.status_code , 200)

class SubProductTestCase(MyTestCase):

    @patch('quality.methods.best_substitut') # la fonction que l'on souhaite patcher
    def test_sub_product_page(self, mock_best_substitut):

        mock_best_substitut.return_value = FAKE_RETURN_BESTSUBSTITUT # return fake datas

        request = self.factory.get('/quality/sub_product/', {'subscribe' : self.choices}) #self.choices = FAKE_DATA_USER_CHOICES
        request.user = self.user
        #adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)

        request.session.save()
        record_session = self.record_selected_session
        for values in record_session:
            request.session[values] = values

        response = sub_product(request)
        self.assertEqual(response.status_code , 200)

class UserChoiceTestCase(MyTestCase):
    def test_user_choice_page(self):
        request = self.factory.get('/quality/sub_product/', {'subscribe': FAKE_DATA_USER_CHOICES2})
        request.user = self.user
        # adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)

        request.session.save()

        # record in session a product selected before and check the record
        before = len(request.session.items())
        for value , choice in zip(self.record_selected_session, self.p_selected):
            request.session[value] = choice
        after_first_record = len(request.session.items())

        self.assertEqual(after_first_record, before + 5)

        response = user_choice(request)
        self.assertEqual(response.status_code , 200)

class Myaccount(MyTestCase):

    def test_myaccount(self):
        request = self.factory.get('/quality/myaccount/')
        request.user = self.user
        response = myaccount(request)
        self.assertEqual(response.status_code , 200)
        self.assertEqual(self.user.email, 'jacob@…')
        self.assertEqual(self.user.username, 'jacob')

class Food(MyTestCase):
    def test_food(self):
        request = self.factory.get('/quality/food/')
        request.user = self.user
        response = food(request)
        self.assertEqual(response.status_code , 200)

class CustomLoginView(MyTestCase):

    def test_login(self):
        response = self.client.get(reverse('quality:login'))
        self.assertEqual(response.status_code , 200)

    def test_logged_user_and_redirect(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        logged_in = self.client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get("/")
        self.assertEqual(response.status_code , 200)

    def test_invalid_user_login(self):
        response = self.client.login(username= "toto", password= "n'importe quoi")
        self.assertFalse(response)

class SignupPageTestCase(MyTestCase):
    # test that success_signup page returns a 200 code
    def test_signup_page(self):
        response = self.client.get(reverse('quality:signup'))
        self.assertEqual(response.status_code, 200)

    def test_logged_user_and_redirect(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        logged_in = self.client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get("/")
        self.assertEqual(response.status_code , 200)

class LogoutPageTestCase(MyTestCase):
    #test that logout page returns a 200 code
    #here page when an user logged out is index.html

    def test_logout_user(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        logged_in = self.client.login(username='testuser', password='12345')
        response = self.client.get('/quality/logout/')
        self.assertEqual(response.status_code , 302)
