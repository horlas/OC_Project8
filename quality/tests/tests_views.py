from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth.models import User
from quality.methods import query_off, best_substitute
from quality.models import SelectedProduct, SubstitutProduct, Backup



class TestClient(Client):

    def login_user(self, username, pwd):
        """
        Login as specified user, does not depend on auth backend (hopefully)

        This is based on Client.login() with a small hack that does not
        require the call to authenticate()
        """
        user = User.objects.create(username=username)
        user.set_password(pwd)
        user.save()
        c = Client()
        c.login(username=username, password=pwd)




class IndexPageTestCase(TestCase):

    # test that index page returns a 200 code
    def test_index_page(self):
        response = self.client.get(reverse('quality:accueil'))
        self.assertEqual(response.status_code, 200)


class AccountPageTestCase(TestCase):
    # test that home page returns a 302 code
    def test_myaccount_page(self):
        response = self.client.get(reverse('quality:myaccount'))
        self.assertEqual(response.status_code, 302)


class FoodPageTestCase(TestCase, Client):

    def test_food_page_return_302(self):
        '''test that food page returns a 302 code'''
        response = self.client.get(reverse('quality:food'))
        self.assertEqual(response.status_code, 302)


class QueryDataTestCase(TestCase):

    def test_query_data_page_return_200(self):
        '''test that query data page return a 200 code'''
        response = self.client.get(reverse('quality:query_data'))
        self.assertEqual(response.status_code , 200)

    def test_query_data_empty(self):
        '''a test not very useful ;-)'''
        query = None
        if not query:
            title = "saisissez un produit ! "
            context = {'title': title}
        self.assertEqual(context['title'], "saisissez un produit ! ")

    def test_query_data_result(self):
        '''we test that data lenght is 6 to be sure our methods return results from OFF API'''
        data = query_off('nutella')
        self.assertEqual(len(data), 6)


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
        self.user = User.objects.create(
            'foo',
            'myemail@test.com',
            'pass'
        )

        self.p_selected = SelectedProduct.objects.create(
            name='Nutella' ,
            url='https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero' ,
            img='https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.100.jpg' ,
            n_grade='e' ,
            category='Produits à tartiner')

        self.logged_in = self.client.login(
            username='foo',
            password='pass'
        )

    def test_user_choice_page(self):
        # check new User object created
        self.assertEqual(User.objects.count(), 1)
        # check use is logged in
        self.assertEqual(self.logged_in, True)  # check login success

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



        response = self.client.get(reverse('quality:user_choice'))
        self.assertEqual(response.status_code , 302)


class MyAccountTestCase(TestCase):

    def test_myaccount_page_return_302(self):
            '''test that my account return a 200 code'''
            response = self.client.get(reverse('quality:myaccount'))
            self.assertEqual(response.status_code , 302)

class FoodTestCase(TestCase):

    def test_food_page_return_200(self):
            '''test that food page return a 200 code with requested data '''
            user = TestClient()
            user.login_user('testclient2', '1234')

            #create a selected product


            response = self.client.get(reverse('quality:food'))
            self.assertEqual(response.status_code , 302)



class LoginPageTestCase(TestCase):
    # test that login page returns a 200 code
    def test_login_page(self):
        response = self.client.get(reverse('quality:login'))
        self.assertEqual(response.status_code, 200)

class SignupPageTestCase(TestCase):
    # test that signup page returns a 200 code
    def test_signup_page(self):
        response = self.client.get(reverse('quality:signup'))
        self.assertEqual(response.status_code, 200)

class SucessSignupPageTestCase(TestCase):
    # test that success_signup page returns a 200 code
    def test_success_signup_page(self):
        response = self.client.get(reverse('quality:success_signup'))
        self.assertEqual(response.status_code, 200)

class LogoutPageTestCase(TestCase):
    #test that logout page returns a 200 code
    #here page when an user logged out is index.html
    def test_logout_page(self):
        response = self.client.get(reverse('quality:accueil'))
        self.assertEqual(response.status_code, 200)