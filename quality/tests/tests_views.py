from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class IndexPageTestCase(TestCase):

    #test that index page returns a 200 code

    def test_index_page(self):
        response = self.client.get(reverse('quality:accueil'))
        self.assertEqual(response.status_code, 200)


class HomePageTestCase(TestCase):
    #test that home page returns a 200 code
    def test_home_page(self):
        response = self.client.get(reverse('quality:home'))
        self.assertEqual(response.status_code, 200)


class LoginPageTestCase(TestCase):
    #test that login page returns a 200 code
    def test_login_page(self):
        response = self.client.get(reverse('quality:login'))
        self.assertEqual(response.status_code, 200)

class SignupPageTestCase(TestCase):
    #test that signup page returns a 200 code
    def test_signup_page(self):
        response = self.client.get(reverse('quality:signup'))
        self.assertEqual(response.status_code, 200)

class SucessSignupPageTestCase(TestCase):
    #test that success_signup page returns a 200 code
    def test_success_signup_page(self):
        response = self.client.get(reverse('quality:success_signup'))
        self.assertEqual(response.status_code, 200)



class LogoutPageTestCase(TestCase):
    #test that logout page returns a 200 code
    #here page when an user logged out is index.html
    def test_logout_page(self):
        response = self.client.get(reverse('quality:index'))
        self.assertEqual(response.status_code, 200)