from django.test import TestCase, RequestFactory, SimpleTestCase
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from quality.views import *
from unittest.mock import patch, MagicMock
from quality.tests.test_set import *
from quality.models import SelectedProduct, SubstitutProduct, Backup
from django.contrib.sessions.middleware import SessionMiddleware


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

# class SubProductTestCase(TestCase):
#     def test_sub_product_page(self):
#         '''test that sub product return a 200 code'''
#         response = self.client.get(reverse('quality:sub_product'))
#         self.assertEqual(response.status_code , 302)




#####essai avec patch substitut product en cours de developpement#######
# class SubProductTestCase(MyTestCase):
#
#     @patch('best_substitut') # la fonction que l'on souhaite partcher
#     def test_sub_product_page(self, mock_best_substitut):
#         best_substitut = MagicMock(return_value=FAKE_RETURN_BESTSUBSTITUT)
#         request = self.factory.get('/quality/sub_product/', {'subscribe' : self.choices})
#         request.user = self.user
#         #adding session
#         middleware = SessionMiddleware()
#         middleware.process_request(request)
#
#         request.session.save()
#         record_session = self.record_selected_session
#         for values in record_session:
#             request.session[values] = values
#             print(request.session[values])
#
#         response = sub_product(request)
#
#
#         self.assertEqual(response.status_code , 200)












class UserChoiceTestCase(MyTestCase):

    def test_user_choice_page(self):

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

class SuccessSignupTestCase(TestCase):
     def test_success_signup_page(self):
        response = self.client.get(reverse('quality:success_signup'))
        self.assertEqual(response.status_code, 200)
        #test that class which contains sucess_message exists
        self.assertContains(response , 'class="text-account' , 1)


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
