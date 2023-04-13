from django.test import Client, TestCase
from django.urls import reverse
from .models import User
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import merchandise

# Create your tests here.

class RegisterPageTest(TestCase):
    def setUp(self):
            # Set up any necessary data for the test
            self.url = reverse('register')

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

#seller tests
class CreateListingTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword', role='S',email="test@test.com")

    def test_create_listing_view(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
        
        # Create a test image file for the form
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        # Create a merchandise item data for the form
        form_data = {
            'title': 'Test Item',
            'description': 'This is a test item',
            'cost': 9.99,
            'quantity_in_stock': 10,
            # Add any other required form fields
        }
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg") # Create a test image file for the form
        # Make a POST request to the create_listing view with the form data and image file
        response = self.client.post(reverse('create-listing'), data=form_data, files={'image': image})

        self.assertTrue(merchandise.objects.filter(title='Test Item').exists()) # Check that the merchandise item was created in the database
        self.assertRedirects(response, reverse('home'))# Check that the response redirects to the home view

    