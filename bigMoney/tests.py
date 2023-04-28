from django.test import Client, TestCase
from django.urls import reverse
from .models import User, Order, merchandise
from bigMoney.models import CartItem
from bigMoney.models import shoppingCart as ShoppingCart
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import merchandise
from .views import *

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
    #succesful login test
    def test_login_success(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('home'), status_code=302)
    #unsuccessful login test
    def test_login_failure(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')
    
    def test_logout_success(self):
        # Login first
        self.client.login(username='testuser', password='testpassword')

        # Logout
        response = self.client.get(reverse('logout'))

        # Check that the user is logged out
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'), status_code=302)
        
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

#seller tests
class CreateListingTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword', role='S', email="test@test.com", is_approved=True)
        # Create a merchandise item associated with the test user
        self.item = merchandise.objects.create(title='Test', description='This is a test item', cost=9.99, quantity_in_stock=10, poster=self.user, is_approved=True)

    def test_create_listing_view(self):
        self.client.login(username='testuser', password='testpassword')
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg") # Create a test image file for the form
        # Create a merchandise item data for the form
        form_data = {
            'title': 'Test Item',
            'description': 'This is a test item',
            'cost': 9.99,
            'quantity_in_stock': 10,
            'genre': "outdoors"
        }
        # Make a POST request to the create_listing view with the form data and image file
        response = self.client.post(reverse('create-listing'), data=form_data, files={'image': image})

        self.assertTrue(merchandise.objects.filter(title='Test Item').exists()) # Check that the merchandise item was created in the database
        self.assertRedirects(response, reverse('home'))# Check that the response redirects to the home view

    def test_view_my_merchandise_with_authenticated_user(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
        # Query the merchandise objects associated with the test user from the database
        my_merchandise = merchandise.objects.filter(poster=self.user)
        # Get the URL for the view_my_merchandise function
        url = reverse('view-my-listings')
        # Send GET request to the view_my_merchandise function
        response = self.client.get(url)
        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if 'listings' exists in the response context
        self.assertIn('listings', response.context)
        # Assert that the rendered 'listings' context contains the expected item
        self.assertIn(self.item, my_merchandise)
        # Assert that the response uses the 'view_my_listings.html' template
        self.assertTemplateUsed(response, 'view_my_listings.html')
    def test_view_my_merchandise_with_unauthenticated_user(self):
        # Log out the test user
        self.client.logout()
        # Get the URL for the view_my_merchandise function
        url = reverse('view-my-listings')
        # Send GET request to the view_my_merchandise function
        response = self.client.get(url)
        # Assert that the response has a status code of 302 (Redirect)
        self.assertEqual(response.status_code, 302)
    
    def test_view_my_sales_authenticated_user(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Send a GET request to view_my_sales with a query string parameter
        response = self.client.get(reverse('view-my-sales'), {'message': 'Test message'})

        # Assert that the response has a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the rendered HTML contains the username of the logged-in user
        self.assertContains(response, 'testuser')

        # Assert that the rendered HTML contains the message parameter value
        self.assertContains(response, 'Test message')

    def test_view_my_sales_unauthenticated_user(self):
        # Log out the test user
        self.client.logout()

        # Send a GET request to view_my_sales with a query string parameter
        response = self.client.get(reverse('view-my-sales'), {'message': 'Test message'})

        # Assert that the response has a 302 status code, indicating a redirect to the login page
        self.assertEqual(response.status_code, 302)

# cart tests
class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', role='C', email="test@test.com", is_approved=True)
        self.item = merchandise.objects.create(title='Test', description='This is a test item', cost=9.99, 
        quantity_in_stock=10, poster=self.user, is_approved=True)
        self.cart = ShoppingCart.objects.create(customer=self.user)
        self.cartItem = CartItem.objects.create(item = self.item, customer = self.user, quantity = 1)
        self.client = Client()

    def test_add_to_cart(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Add our item to the cart
        self.cart.items.add(self.cartItem)
        self.cart.save()

        # Assert that the CartItem object is in the shoppingCart's items
        self.assertIn(self.cartItem, self.cart.items.all())

    def test_view_cart(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Send a request to the view-cart URL
        response = self.client.get(reverse('view-cart'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_checkout(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Add our item to the cart
        self.cart.items.add(self.cartItem)
        self.cart.save()

        # Send a request to the checkout URL
        response = self.client.post(reverse('checkout'))

        # Check if the response status code is 302
        self.assertEqual(response.status_code, 302)

        # Create the order (modified code from checkout view)
        order = Order.objects.create(customer=self.user)
        for item in self.cart.items.all():
            order.items.add(item)
        order.customer = self.user
        self.user.Orders.add(order)
        order.save()

        # Empty cart (code from checkout view)
        self.cart.items.clear()

        # Check if the cart is empty after the checkout
        self.assertEqual(self.cart.items.count(), 0)

        # Check if the created Order has the correct information
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertIn(self.cartItem, order.items.all())

class BuyerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', role='C', email="test@test.com", 
        is_approved=True)

    def test_edit_account_details(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
    
        # Send a request to the edit-account URL
        response = self.client.post(reverse('edit-account'))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Define form data
        form_data = {
            'name': 'John Doe',
            'email': 'email@example.com',
            'card_number': '1234567890123456',
        }

        # Send a POST request to the edit_account URL with the form data
        response = self.client.post(reverse('edit-account'), form_data)

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Refresh the user instance from the database
        self.user.refresh_from_db()

        # Check if the user's information has been updated correctly
        self.assertEqual(self.user.name, form_data['name'])
        self.assertEqual(self.user.email, form_data['email'])
        self.assertEqual(self.user.card_number, form_data['card_number'])

    def test_change_address(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Send a request to the change_address URL
        response = self.client.post(reverse('change-address'))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Define the form data
        form_data = {
            'RecipiantName': 'Jane Doe',
            'StreetAddress': '100 Dawg Rd',
            'City': 'Starkville',
            'State': 'MS',
            'zipcode': '39759',
        }

        # Send a POST request to the change_address URL with the form data
        response = self.client.post(reverse('change-address'), form_data)

        # Refresh the user instance from the database
        self.user.refresh_from_db()

        # Check if the user's address has been updated correctly
        self.assertEqual(self.user.address.RecipiantName, form_data['RecipiantName'])
        self.assertEqual(self.user.address.StreetAddress, form_data['StreetAddress'])
        self.assertEqual(self.user.address.City, form_data['City'])
        self.assertEqual(self.user.address.State, form_data['State'])
        self.assertEqual(str(self.user.address.zipcode), form_data['zipcode'])
