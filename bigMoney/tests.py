from django.test import Client, TestCase
from django.urls import reverse
from .models import User
from .forms import *

# Create your tests here.

class RegisterPageTest(TestCase):
    def setUp(self):
            # Set up any necessary data for the test
            self.url = reverse('register')  # Replace 'register' with the URL name of your register view

    def test_register_page_status_code(self):
            # Test that the register page returns a 200 status code
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)


    def test_register_page_contains_form(self):
        # Test that the register page contains a form
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], RegistrationForm)
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'type="submit"')


    def test_register_page_form_submission(self):
        # Test that the register page form submission creates a new user
        data = {
            'username': 'yee',
            'email': 'testuser@example.com',
            'role' : 'S',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
         }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='yee').exists())

    def test_register_page_form_submission_invalid(self):
        # Test that the register page form submission creates a new user
        data = {
            'username': 'yee',
            'email': 'testuser@example.com',
            'role' : 'S',
            'password1': 'testpassword123',
            'password2': 'anythingelse'
         }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='yee').exists())


#login tests
class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')

    def test_login_success(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('home'), status_code=302)

    def test_login_failure(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')
