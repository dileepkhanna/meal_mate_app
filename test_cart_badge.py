import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_mate.settings')
django.setup()

from delivery.models import Customer, Cart, CartItem, Restaurant, MenuItem

# Get or create a test user
user, created = Customer.objects.get_or_create(
    username='testcartuser',
    defaults={'email': 'testcart@test.com'}
)
if created:
    user.set_password('test123')
    user.save()
    print(f"✅ Created test user: {user.username}")
else:
    print(f"✅ Using existing user: {user.username}")

# Get or create cart
cart, created = Cart.objects.get_or_create(customer=user)
print(f"✅ Cart: {cart}")

# Get a restaurant and menu item
restaurant = Restaurant.objects.first()
if restaurant:
    menu_item = restaurant.menu_items.first()
    if menu_item:
        # Add item to cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={'quantity': 3}
        )
        if not created:
            cart_item.quantity = 3
            cart_item.save()
        
        print(f"✅ Added {menu_item.name} to cart")
        print(f"✅ Cart total items: {cart.total_items()}")
        print(f"\n🎯 Test the badge by:")
        print(f"   1. Login with username: {user.username}, password: test123")
        print(f"   2. Look at the navbar - you should see a red badge with '3'")
    else:
        print("❌ No menu items found. Please add menu items first.")
else:
    print("❌ No restaurants found. Please add restaurants first.")
