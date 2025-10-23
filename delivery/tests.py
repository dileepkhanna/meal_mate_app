from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from delivery.models import Customer, Restaurant, MenuItem, Cart

class MealMateTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test customer
        self.customer = Customer.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            mobile='1234567890',
            address='Test Address'
        )
        
        # Create admin user
        self.admin = Customer.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            is_staff=True,
            is_superuser=True
        )
        
        # Create test restaurant
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='Italian',
            rating=4.5,
            picture='https://example.com/restaurant.jpg'
        )
        
        # Create test menu items
        self.menu_item1 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Pizza',
            description='Delicious pizza',
            price=Decimal('12.99'),
            is_veg=True,
            picture='https://example.com/pizza.jpg'
        )
        
        self.menu_item2 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Burger',
            description='Tasty burger',
            price=Decimal('8.99'),
            is_veg=False,
            picture='https://example.com/burger.jpg'
        )

class ViewsTestCase(MealMateTestCase):
    """Test all view functions"""
    
    def test_index_view(self):
        """Test home page loads correctly"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Meal Mate')
    
    def test_signin_view(self):
        """Test signin page loads correctly"""
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')
    
    def test_signup_view(self):
        """Test signup page loads correctly"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')

class AuthenticationTestCase(MealMateTestCase):
    """Test authentication functionality"""
    
    def test_valid_login(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('handle_login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('handle_login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
    
    def test_admin_login(self):
        """Test admin login redirects to admin home"""
        response = self.client.post(reverse('handle_login'), {
            'username': 'admin',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')
    
    def test_signup_new_user(self):
        """Test signup with new user data"""
        response = self.client.post(reverse('handle_signup'), {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'new@example.com',
            'mobile': '9876543210',
            'address': 'New Address'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Customer.objects.filter(username='newuser').exists())
    
    def test_signup_duplicate_username(self):
        """Test signup with existing username"""
        response = self.client.post(reverse('handle_signup'), {
            'username': 'testuser',  # Already exists
            'password': 'newpass123',
            'email': 'new@example.com',
            'mobile': '9876543210',
            'address': 'New Address'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username already exists')
    
    def test_signup_duplicate_email(self):
        """Test signup with existing email"""
        response = self.client.post(reverse('handle_signup'), {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'test@example.com',  # Already exists
            'mobile': '9876543210',
            'address': 'New Address'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already registered')

class RestaurantTestCase(MealMateTestCase):
    """Test restaurant management functionality"""
    
    def test_show_restaurants(self):
        """Test restaurant listing page"""
        response = self.client.get(reverse('show_restaurant_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')
    
    def test_add_restaurant(self):
        """Test adding a new restaurant"""
        response = self.client.post(reverse('add_restaurant'), {
            'name': 'New Restaurant',
            'cuisine': 'Mexican',
            'rating': '4.0',
            'picture': 'https://example.com/new.jpg'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Restaurant.objects.filter(name='New Restaurant').exists())
    
    def test_update_restaurant(self):
        """Test updating restaurant details"""
        response = self.client.post(reverse('update_restaurant', args=[self.restaurant.id]), {
            'name': 'Updated Restaurant',
            'cuisine': 'Updated Cuisine',
            'rating': '5.0',
            'picture': 'https://example.com/updated.jpg'
        })
        self.assertEqual(response.status_code, 200)
        updated_restaurant = Restaurant.objects.get(id=self.restaurant.id)
        self.assertEqual(updated_restaurant.name, 'Updated Restaurant')
    
    def test_delete_restaurant(self):
        """Test deleting a restaurant"""
        restaurant_id = self.restaurant.id
        response = self.client.get(reverse('delete_restaurant', args=[restaurant_id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Restaurant.objects.filter(id=restaurant_id).exists())

class MenuTestCase(MealMateTestCase):
    """Test menu management functionality"""
    
    def test_restaurant_menu_view(self):
        """Test restaurant menu page"""
        response = self.client.get(reverse('restaurant_menu', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pizza')
        self.assertContains(response, 'Burger')
    
    def test_add_menu_item(self):
        """Test adding a new menu item"""
        response = self.client.post(reverse('restaurant_menu', args=[self.restaurant.id]), {
            'name': 'Pasta',
            'description': 'Creamy pasta',
            'price': '10.99',
            'is_veg': 'on',
            'picture': 'https://example.com/pasta.jpg'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(MenuItem.objects.filter(name='Pasta').exists())
    
    def test_update_menu_item(self):
        """Test updating menu item"""
        response = self.client.post(reverse('update_menuItem', args=[self.menu_item1.id]), {
            'name': 'Updated Pizza',
            'description': 'Updated description',
            'price': '15.99',
            'is_veg': 'on',
            'picture': 'https://example.com/updated-pizza.jpg'
        })
        self.assertEqual(response.status_code, 200)
        updated_item = MenuItem.objects.get(id=self.menu_item1.id)
        self.assertEqual(updated_item.name, 'Updated Pizza')
    
    def test_delete_menu_item(self):
        """Test deleting menu item"""
        item_id = self.menu_item1.id
        response = self.client.get(reverse('delete_menuItem', args=[item_id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(MenuItem.objects.filter(id=item_id).exists())

class CartTestCase(MealMateTestCase):
    """Test shopping cart functionality"""
    
    def test_add_to_cart(self):
        """Test adding item to cart"""
        response = self.client.get(reverse('add_to_cart', args=[self.menu_item1.id, 'testuser']))
        self.assertEqual(response.status_code, 302)  # Redirect after adding
        
        # Check if cart was created and item added
        cart = Cart.objects.get(customer=self.customer)
        self.assertIn(self.menu_item1, cart.items.all())
    
    def test_show_cart_empty(self):
        """Test showing empty cart"""
        response = self.client.get(reverse('show_cart_page', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your cart is empty')
    
    def test_show_cart_with_items(self):
        """Test showing cart with items"""
        # Add item to cart first
        cart, created = Cart.objects.get_or_create(customer=self.customer)
        cart.items.add(self.menu_item1, self.menu_item2)
        
        response = self.client.get(reverse('show_cart_page', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pizza')
        self.assertContains(response, 'Burger')
    
    def test_cart_total_calculation(self):
        """Test cart total price calculation"""
        cart, created = Cart.objects.get_or_create(customer=self.customer)
        cart.items.add(self.menu_item1, self.menu_item2)
        
        expected_total = self.menu_item1.price + self.menu_item2.price
        self.assertEqual(cart.total_price(), expected_total)

class CheckoutTestCase(MealMateTestCase):
    """Test checkout functionality"""
    
    def test_checkout_empty_cart(self):
        """Test checkout with empty cart"""
        response = self.client.get(reverse('checkout', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your cart is empty')
    
    def test_checkout_with_items(self):
        """Test checkout with items in cart"""
        # Add items to cart
        cart, created = Cart.objects.get_or_create(customer=self.customer)
        cart.items.add(self.menu_item1)
        
        response = self.client.get(reverse('checkout', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pizza')

class OrderTestCase(MealMateTestCase):
    """Test order functionality"""
    
    def test_orders_page(self):
        """Test orders confirmation page"""
        # Add items to cart first
        cart, created = Cart.objects.get_or_create(customer=self.customer)
        cart.items.add(self.menu_item1)
        
        response = self.client.get(reverse('orders', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order Confirmed')
        
        # Check if cart is cleared after order
        cart.refresh_from_db()
        self.assertEqual(cart.items.count(), 0)

class ModelTestCase(MealMateTestCase):
    """Test model functionality"""
    
    def test_customer_str_method(self):
        """Test Customer string representation"""
        self.assertEqual(str(self.customer), 'testuser')
    
    def test_restaurant_str_method(self):
        """Test Restaurant string representation"""
        expected = f"{self.restaurant.name} {self.restaurant.cuisine} {self.restaurant.rating}/5"
        self.assertEqual(str(self.restaurant), expected)
    
    def test_menu_item_str_method(self):
        """Test MenuItem string representation"""
        expected = f"{self.menu_item1.name} {self.menu_item1.description} {self.menu_item1.price}"
        self.assertEqual(str(self.menu_item1), expected)
    
    def test_cart_str_method(self):
        """Test Cart string representation"""
        cart = Cart.objects.create(customer=self.customer)
        expected = f"Cart for {self.customer.username}"
        self.assertEqual(str(cart), expected)

class SecurityTestCase(MealMateTestCase):
    """Test security aspects"""
    
    def test_password_hashing(self):
        """Test that passwords are properly hashed"""
        # Password should not be stored in plain text
        self.assertNotEqual(self.customer.password, 'testpass123')
        # But should be able to check password
        self.assertTrue(self.customer.check_password('testpass123'))
    
    def test_unauthorized_access(self):
        """Test accessing protected views without authentication"""
        # This would depend on your authentication requirements
        # For now, most views don't require authentication in your current setup
        pass

class URLTestCase(MealMateTestCase):
    """Test URL routing"""
    
    def test_all_urls_resolve(self):
        """Test that all URLs resolve correctly"""
        urls_to_test = [
            ('index', []),
            ('signin', []),
            ('signup', []),
            ('show_restaurant_page', []),
            ('restaurant_menu', [self.restaurant.id]),
            ('customer_menu', [self.restaurant.id, 'testuser']),
            ('show_cart_page', ['testuser']),
            ('checkout', ['testuser']),
            ('orders', ['testuser']),
        ]
        
        for url_name, args in urls_to_test:
            try:
                url = reverse(url_name, args=args)
                response = self.client.get(url)
                # Should not get 404 or 500 errors
                self.assertIn(response.status_code, [200, 302, 405])
            except Exception as e:
                self.fail(f"URL {url_name} failed to resolve: {e}")

class IntegrationTestCase(MealMateTestCase):
    """Test complete user workflows"""
    
    def test_complete_order_workflow(self):
        """Test complete order process from login to order confirmation"""
        # 1. Login
        login_response = self.client.post(reverse('handle_login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(login_response.status_code, 200)
        
        # 2. View restaurants
        restaurants_response = self.client.get(reverse('show_restaurant_page'))
        self.assertEqual(restaurants_response.status_code, 200)
        
        # 3. View menu
        menu_response = self.client.get(reverse('customer_menu', args=[self.restaurant.id, 'testuser']))
        self.assertEqual(menu_response.status_code, 200)
        
        # 4. Add to cart
        add_cart_response = self.client.get(reverse('add_to_cart', args=[self.menu_item1.id, 'testuser']))
        self.assertEqual(add_cart_response.status_code, 302)
        
        # 5. View cart
        cart_response = self.client.get(reverse('show_cart_page', args=['testuser']))
        self.assertEqual(cart_response.status_code, 200)
        
        # 6. Checkout
        checkout_response = self.client.get(reverse('checkout', args=['testuser']))
        self.assertEqual(checkout_response.status_code, 200)
        
        # 7. Complete order
        order_response = self.client.get(reverse('orders', args=['testuser']))
        self.assertEqual(order_response.status_code, 200)