from django.test import TestCase, RequestFactory, SimpleTestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth.models import User
from quality.views import *
from unittest.mock import patch, MagicMock
from quality.tests.test_set import *
from quality.models import SelectedProduct, SubstitutProduct, Backup
from django.contrib.sessions.middleware import SessionMiddleware



# class TestClient(Client):
#
#     def login_user(self, username, pwd):
#         """
#         Login as specified user, does not depend on auth backend (hopefully)
#
#         This is based on Client.login() with a small hack that does not
#         require the call to authenticate()
#         """
#         user = User.objects.create(username=username)
#         user.set_password(pwd)
#         user.save()
#         c = Client()
#         c.login(username=username, password=pwd)
#
#
#
#
# class IndexPageTestCase(TestCase):
#
#     # test that index page returns a 200 code
#     def test_index_page(self):
#         response = self.client.get(reverse('quality:accueil'))
#         self.assertEqual(response.status_code, 200)
#
#
# class AccountPageTestCase(TestCase):
#     # test that home page returns a 302 code
#     def test_myaccount_page(self):
#         response = self.client.get(reverse('quality:myaccount'))
#         self.assertEqual(response.status_code, 302)
#
#
# class FoodPageTestCase(TestCase, Client):
#
#     def test_food_page_return_302(self):
#         '''test that food page returns a 302 code'''
#         response = self.client.get(reverse('quality:food'))
#         self.assertEqual(response.status_code, 302)
#
#
# class QueryDataTestCase(TestCase):
#
#     def test_query_data_page_return_200(self):
#         '''test that query data page return a 200 code'''
#         response = self.client.get(reverse('quality:query_data'))
#         self.assertEqual(response.status_code , 200)
#
#     def test_query_data_empty(self):
#         '''a test not very useful ;-)'''
#         query = None
#         if not query:
#             title = "saisissez un produit ! "
#             context = {'title': title}
#         self.assertEqual(context['title'], "saisissez un produit ! ")
#
#     def test_query_data_result(self):
#         '''we test that data lenght is 6 to be sure our methods return results from OFF API'''
#         data = query_off('nutella')
#         self.assertEqual(len(data), 6)


# class SubProductTestCase(TestCase):
#     # choices = "Nutella, Pâtes à tartiner aux noisettes et au cacao," \
#     #           " https://static.openfoodfacts.org/images/products/301/762/404/7813/front_fr.42.100.jpg," \
#     #           " E, https://fr.openfoodfacts.org/produit/3017624047813/nutella"
#     # choices = choices.split(', ')
#     def test_sub_product_page(self):
#         '''test that sub product return a 200 code'''
#         response = self.client.get(reverse('quality:sub_product'))
#         self.assertEqual(response.status_code , 302)

class MyTestCase(TestCase):
    '''Here is a parent class with custom global setup'''
    def setUp(self):
        '''we call the global setup from test_set.py'''
        self.client = Client()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

        self.choices = FAKE_DATA_USER_CHOICES

        self.factory = RequestFactory()

        self.record_selected_session = ['selected_name', 'selected_category', 'selected_img', 'selected_nutriscore', 'selected_url']
        self.record_substitut_session = ['substitut_name', 'substitut_category', 'substitut_img', 'substitut_nutriscore',
                          'substitut_url']
        self.p_selected = FAKE_DATA_SELECTED_PRODUCT

class UserChoiceTestCase(MyTestCase):

    def test_user_choice_page(self):
        # mock_request_get.return_value = MagicMock(FAKE_DATA_USER_CHOICES)
        # request = self.factory.get('/quality/user_choice/')
        # request.user = self.user
        # response = user_choice(request)
        # self.assertEqual(response.status_code , 200)
        # the page return 302 status code
        response = self.client.get(reverse('quality:user_choice'))
        self.assertEqual(response.status_code , 302)

        # define request
        request = response.wsgi_request
        # define loggued user
        request.user = self.user

        # record in session a product selected before and check the record
        before = len(request.session.items())
        for value , choice in zip(self.record_selected_session, self.p_selected):
            request.session[value] = choice
        after_first_record = len(request.session.items())

        self.assertEqual(after_first_record, before + 5)

        # get the choice
        choices = self.choices.get('subscribe', None)
        choices = choices.split(', ')
        self.assertEqual(len(choices), 5)

        #record p_selected in database and check the record

        p_selected = SelectedProduct.objects.create(
            name=request.session['selected_name'] ,
            url=request.session['selected_url'] ,
            img=request.session['selected_img'] ,
            n_grade=request.session['selected_nutriscore'] ,
            category=request.session['selected_category'])
        after_record = SelectedProduct.objects.count()
        self.assertEqual(after_record, 1)

        #record backup and check
        backup = Backup.objects.create(
            user_id=request.user,
            selected_product_id=p_selected)
        after_backup_record = Backup.objects.count()
        self.assertEqual(after_backup_record, 1)

        # record substitut and check
        p_substitut = SubstitutProduct.objects.create(
            name = choices[0],
            category = choices[1],
            img = choices[2],
            n_grade = choices[3],
            url = choices[4],

            backup_id = backup,
            user_id = request.user,
            selected_product_id = p_selected
        )
        after_substitut_record = SubstitutProduct.objects.count()
        self.assertEqual(after_substitut_record, 1)

        # record in session a product substitut before and check the record
        for value , choice in zip(self.record_substitut_session, choices):
            request.session[value] = choice
        after_second_record = len(request.session.items())

        self.assertEqual(after_second_record, after_first_record + 5)

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
        # response = self.client.get(reverse('quality:food'))
        # self.assertEqual(response.status_code, 302)

        request = self.factory.get('/quality/food/')
        # adding session
        # middleware = SessionMiddleware()
        # middleware.process_request(request)
        # request.session.save()


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

        # self.assertRedirects(response, accueil)
        # request = self.factory.get('quality/login/', follow=True)
        # response = LoginView.as_view()(request)
        # self.assertEqual(response.status_code , 200)
        # response = self.client.get(reverse('quality:login'))
        # # last_url , status_code = response.redirect_chain[-1]
        # # print(last_url)
        #
        # # send login data
        # user = User.objects.create(username='testuser')
        # user.set_password('12345')
        # user.save()
        # logged_in = self.client.login(username='testuser', password='12345')
        # self.assertTrue(logged_in)
        #
        # #test get_success_url
        # # self.assertRedirects(response, 'quality')
        # # response=self.client
        # self.assertRedirects(response, expected_url='quality/', status_code=200, target_status_code=200,
        #                              msg_prefix='', fetch_redirect_response=True)


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
#
class LogoutPageTestCase(MyTestCase):
    #test that logout page returns a 200 code
    #here page when an user logged out is index.html

    def test_logout_user(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        logged_in = self.client.login(username='testuser' , password='12345')
        response = self.client.get('/quality/logout/')
        self.assertEqual(response.status_code , 200)
