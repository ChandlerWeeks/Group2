from django.test import Client, TestCase
from django.urls import reverse
from .models import User, Order, merchandise
from .forms import *
from .views import *

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

class AdminLoginTest(TestCase):
    def setUp(self):
        # create admin
        self.admin = User.objects.create_superuser(
        username='admin', email='admin@example.com', password='something')

    def test_admin_login(self):
        # go to admin login view
        url = reverse('admin:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # login as admin
        response = self.client.post(
            url,
            {
                'username': 'admin',
                'password': 'something'
            }
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url)
        self.assertRedirects(response, reverse('admin:index'), status_code=302)

class AdminApproveUser(TestCase):
    def setUp(self):
        # create admin
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='something')
        # create user
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass')
        self.user.is_approved = None
        self.user.save()
    
    def test_admin_approve_user(self):
        # login as admin
        self.client.force_login(self.admin)
        
        # check user is not approved
        self.assertFalse(User.objects.get(id=self.user.id).is_approved)

        # set is_approved to true
        self.user.is_approved = True
        self.user.save()

        self.assertTrue(User.objects.get(id=self.user.id).is_approved)
        # another way of checking
        #self.user.refresh_from_db()
        #self.assertTrue(self.user.is_approved)

class AdminDisapproveUser(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='something')
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass',
            is_approved = True)

    def test_admin_disapprove_user(self):
        # login as admin
        self.client.force_login(self.admin)
        
        # check user is approved
        self.assertTrue(User.objects.get(id=self.user.id).is_approved)

        # set is_approved to true
        self.user.is_approved = False
        self.user.save()

        self.assertFalse(User.objects.get(id=self.user.id).is_approved)

class AdminApproveMerch(TestCase):
    def setUp(self):
        # create admin
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='something')
        # create merchandise
        self.merch = merchandise.objects.create(
            title = 'TestMerch',
            cost = 10.00,
            description = 'Some description',
            quantity_in_stock = 3,
            quantity_sold = 1,
            is_approved = None,
        )
    
    def test_approve_merch(self):
        # login as admin
        self.client.force_login(self.admin)

        # check merch exists
        self.assertTrue(merchandise.objects.get(id=self.merch.id).title == 'TestMerch')

        # check merch is not approved
        self.assertFalse(merchandise.objects.get(id=self.merch.id).is_approved)
        
        # set merch.is_approved to True and save
        self.merch.is_approved = True
        self.merch.save()

        # Check if the update was successful
        self.merch.refresh_from_db()
        self.assertEqual(self.merch.is_approved, True)

class AdminViewOrderHistory(TestCase):
    def setUp(self):
        # create admin
        self.admin = User.objects.create_superuser(
        username='admin', email='admin@example.com', password='something')

    def test_view_order_history(self):
        # login as admin
        self.client.force_login(self.admin)

        #look at order history
        url = reverse('admin:bigMoney_order_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        



