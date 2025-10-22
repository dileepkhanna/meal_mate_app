#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_mate.settings')
django.setup()

from delivery.models import Restaurant, MenuItem

# Create sample restaurants
restaurants_data = [
    {
        'name': 'Pizza Palace',
        'picture': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400',
        'cuisine': 'Italian',
        'rating': 4.5
    },
    {
        'name': 'Burger Barn',
        'picture': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400',
        'cuisine': 'American',
        'rating': 4.2
    },
    {
        'name': 'Sushi Zen',
        'picture': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400',
        'cuisine': 'Japanese',
        'rating': 4.8
    },
    {
        'name': 'Spice Garden',
        'picture': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400',
        'cuisine': 'Indian',
        'rating': 4.3
    }
]

# Create restaurants
for restaurant_data in restaurants_data:
    restaurant, created = Restaurant.objects.get_or_create(
        name=restaurant_data['name'],
        defaults=restaurant_data
    )
    if created:
        print(f"Created restaurant: {restaurant.name}")

# Create sample menu items
menu_items_data = [
    # Pizza Palace items
    {
        'restaurant_name': 'Pizza Palace',
        'name': 'Margherita Pizza',
        'picture': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=300',
        'description': 'Classic pizza with tomato sauce, mozzarella, and fresh basil',
        'price': 12.99,
        'is_veg': True
    },
    {
        'restaurant_name': 'Pizza Palace',
        'name': 'Pepperoni Pizza',
        'picture': 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300',
        'description': 'Delicious pizza topped with pepperoni and cheese',
        'price': 15.99,
        'is_veg': False
    },
    # Burger Barn items
    {
        'restaurant_name': 'Burger Barn',
        'name': 'Classic Cheeseburger',
        'picture': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300',
        'description': 'Juicy beef patty with cheese, lettuce, tomato, and pickles',
        'price': 9.99,
        'is_veg': False
    },
    {
        'restaurant_name': 'Burger Barn',
        'name': 'Veggie Burger',
        'picture': 'https://images.unsplash.com/photo-1525059696034-4967a729002e?w=300',
        'description': 'Plant-based patty with fresh vegetables and special sauce',
        'price': 8.99,
        'is_veg': True
    },
    # Sushi Zen items
    {
        'restaurant_name': 'Sushi Zen',
        'name': 'Salmon Roll',
        'picture': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=300',
        'description': 'Fresh salmon with avocado and cucumber',
        'price': 13.99,
        'is_veg': False
    },
    {
        'restaurant_name': 'Sushi Zen',
        'name': 'Vegetable Roll',
        'picture': 'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=300',
        'description': 'Cucumber, avocado, and carrot with sesame seeds',
        'price': 10.99,
        'is_veg': True
    },
    # Spice Garden items
    {
        'restaurant_name': 'Spice Garden',
        'name': 'Chicken Tikka Masala',
        'picture': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=300',
        'description': 'Tender chicken in creamy tomato-based curry sauce',
        'price': 16.99,
        'is_veg': False
    },
    {
        'restaurant_name': 'Spice Garden',
        'name': 'Paneer Butter Masala',
        'picture': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300',
        'description': 'Soft paneer cubes in rich, creamy tomato gravy',
        'price': 14.99,
        'is_veg': True
    }
]

# Create menu items
for item_data in menu_items_data:
    restaurant = Restaurant.objects.get(name=item_data['restaurant_name'])
    item_data.pop('restaurant_name')
    item_data['restaurant'] = restaurant
    
    menu_item, created = MenuItem.objects.get_or_create(
        restaurant=restaurant,
        name=item_data['name'],
        defaults=item_data
    )
    if created:
        print(f"Created menu item: {menu_item.name} for {restaurant.name}")

print("Sample data created successfully!")