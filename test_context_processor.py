import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_mate.settings')
django.setup()

from delivery.models import Customer, Cart
from delivery.context_processors import cart_count
from django.test import RequestFactory

# Create a mock request
factory = RequestFactory()
request = factory.get('/')

# Get the test user
user = Customer.objects.get(username='testcartuser')
request.user = user

# Test the context processor
result = cart_count(request)

print(f"✅ User: {user.username}")
print(f"✅ Cart count from context processor: {result}")

# Verify cart directly
cart = Cart.objects.filter(customer=user).first()
if cart:
    print(f"✅ Direct cart total_items(): {cart.total_items()}")
    print(f"✅ Cart items: {cart.cart_items.count()}")
    for item in cart.cart_items.all():
        print(f"   - {item.menu_item.name}: quantity {item.quantity}")
else:
    print("❌ No cart found")
