from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth.models import User
from quality.views import *
from unittest.mock import patch, MagicMock
from quality.tests.test_set import *
from quality.methods import query_off, best_substitut
from quality.models import SelectedProduct, SubstitutProduct, Backup



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

class UserChoiceTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user, created = User.objects.get_or_create(username='testuser')
        if created == True:
            self.user.set_password('12345')

            self.user.save()

        self.choices = FAKE_DATA_USER_CHOICES


        self.factory = RequestFactory()

        self.record_selected_session = ['selected_name', 'selected_category', 'selected_img', 'selected_nutriscore', 'selected_url']
        self.record_substitut_session = ['substitut_name' , 'substitut_category' , 'substitut_img' , 'substitut_nutriscore' ,
                          'substitut_url']
        self.p_selected = FAKE_DATA_SELECTED_PRODUCT

    def test_user_choice(self):
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
            user_id=request.user ,
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

        self.assertEqual(after_second_record, after_first_record+5)

    def test_myaccount(self):
        response = self.client.get(reverse('quality:myaccount'))
        self.assertEqual(response.status_code , 302)





    #
    # def test_user_choice_page(self):
    #     # check new User object created
    #     self.assertEqual(User.objects.count(), 1)
    #     # check user is logged in
    #     logged_in = self.client.login(username='testuser', password='12345')
    #     self.assertEqual(logged_in, True)  # check login success
    #     #mock request.GET.get


        # choices = self.choices.split(', ')
        #test record p_selected in database


        # mock_request_GET.return_value = MagicMock(response=self.choices)




        # p_selected = SelectedProduct.objects.create(
        #     name='Nutella',
        #     url='https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero',
        #     img='https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.100.jpg',
        #     n_grade='e',
        #     category='Produits à tartiner')
        #
        # backup = Backup.objects.create(
        #     user_id=,
        #     selected_product_id=p_selected
        # )


        #
        # response = self.client.get(reverse('quality:user_choice'))
        # self.assertEqual(response.status_code , 302)


# class MyAccountTestCase(TestCase):
#
#     def test_myaccount_page_return_302(self):
#             '''test that my account return a 200 code'''
#             response = self.client.get(reverse('quality:myaccount'))
#             self.assertEqual(response.status_code , 302)
#
# class FoodTestCase(TestCase):
#
#     def test_food_page_return_200(self):
#             '''test that food page return a 200 code with requested data '''
#             user = TestClient()
#             user.login_user('testclient2', '1234')
#
#             #create a selected product
#
#
#             response = self.client.get(reverse('quality:food'))
#             self.assertEqual(response.status_code , 302)
#
#
#
# class LoginPageTestCase(TestCase):
#     # test that login page returns a 200 code
#     def test_login_page(self):
#         response = self.client.get(reverse('quality:login'))
#         self.assertEqual(response.status_code, 200)
#
# class SignupPageTestCase(TestCase):
#     # test that signup page returns a 200 code
#     def test_signup_page(self):
#         response = self.client.get(reverse('quality:signup'))
#         self.assertEqual(response.status_code, 200)
#
# class SucessSignupPageTestCase(TestCase):
#     # test that success_signup page returns a 200 code
#     def test_success_signup_page(self):
#         response = self.client.get(reverse('quality:success_signup'))
#         self.assertEqual(response.status_code, 200)
#
# class LogoutPageTestCase(TestCase):
#     #test that logout page returns a 200 code
#     #here page when an user logged out is index.html
#     def test_logout_page(self):
#         response = self.client.get(reverse('quality:accueil'))
#         self.assertEqual(response.status_code, 200)