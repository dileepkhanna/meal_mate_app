from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from delivery.models import Customer, Restaurant, MenuItem, Cart, CartItem
from django.contrib import messages  # To display messages to the user
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

import razorpay
from django.conf import settings

# CSRF Failure Handler
def csrf_failure(request, reason=""):
    messages.error(request, 'Security token expired. Please try again.')
    return redirect('signin')

# Home Page
def index(request):
    return render(request, 'delivery/index.html')

# Sign In Page
def signin(request):
    # Ensure fresh CSRF token
    get_token(request)
    return render(request, 'delivery/signin.html')

# Sign Up Page
def signup(request):
    # Ensure fresh CSRF token
    get_token(request)
    return render(request, 'delivery/signup.html')

# Handle Login
def handle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        from django.contrib.auth import authenticate, login
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if username == 'admin':
                return redirect('admin_home')
            else:
                return redirect('customer_home', username=username)
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('signin')
    else:
        # Handle GET requests by redirecting to signin page
        return redirect('signin')

# Admin Home Page
def admin_home(request):
    return render(request, 'delivery/admin_home.html')

# Customer Home Page
def customer_home(request, username):
    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/customer_home.html', {
        "restaurants": restaurants, 
        "username": username
    })

# Handle Sign Up
def handle_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        # Check for duplicate username
        if Customer.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('signup')
        
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return redirect('signup')

        # Create user with hashed password
        customer = Customer.objects.create_user(
            username=username,
            password=password,
            email=email,
            mobile=mobile,
            address=address
        )
        messages.success(request, 'Account created successfully! Please sign in.')
        return redirect('signin')
    else:
        # Handle GET requests by redirecting to signup page
        return redirect('signup')

# Add Restaurant Page
def add_restaurant_page(request):
    return render(request, 'delivery/add_restaurant.html')

# Add Restaurant
def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        Restaurant.objects.create(name=name, picture=picture, cuisine=cuisine, rating=rating)

        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

    return HttpResponse("Invalid request")

# Show Restaurants
def show_restaurant_page(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

# Restaurant Menu
def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        picture = request.POST.get('picture')

        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            is_veg=is_veg,
            picture=picture
        )
        return redirect('restaurant_menu', restaurant_id=restaurant.id)

    menu_items = restaurant.menu_items.all()
    return render(request, 'delivery/menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
    })

# Update Restaurant Page
def update_restaurant_page(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'delivery/update_restaurant_page.html', {"restaurant": restaurant})

# Update Restaurant
def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.picture = request.POST.get('picture')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')
        restaurant.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

# Delete Restaurant
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()

    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})


# Update Menu item Page
def update_menuItem_page(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)
    return render(request, 'delivery/update_menuItem_page.html', {"item": menuItem})

# Update MenuItem
def update_menuItem(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)

    if request.method == 'POST':
        menuItem.name = request.POST.get('name')
        menuItem.description = request.POST.get('description')
        menuItem.price = request.POST.get('price')
        menuItem.is_veg = request.POST.get('is_veg') == 'on'
        menuItem.picture = request.POST.get('picture')

        menuItem.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

# Delete menuItem
def delete_menuItem(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)
    menuItem.delete()

    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})


# Customer Menu
def customer_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()
    
    return render(request, 'delivery/customer_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'username': username,
    })

# Add items to cart
def add_to_cart(request, item_id, username):
    customer = get_object_or_404(Customer, username=username)
    menu_item = get_object_or_404(MenuItem, id=item_id)

    # Get or create cart for the customer
    cart, created = Cart.objects.get_or_create(customer=customer)

    # Check if cart has items from a different restaurant
    existing_items = cart.cart_items.all()
    if existing_items.exists():
        first_item_restaurant = existing_items.first().menu_item.restaurant
        if first_item_restaurant.id != menu_item.restaurant.id:
            # Automatically clear cart when adding from different restaurant
            old_restaurant_name = first_item_restaurant.name
            cart.cart_items.all().delete()
            messages.info(request, f'Cart cleared! Items from {old_restaurant_name} were removed to add items from {menu_item.restaurant.name}.')

    # Check if item already exists in cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item,
        defaults={'quantity': 1}
    )

    if not item_created:
        # Item exists, increment quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{menu_item.name} quantity updated to {cart_item.quantity}!")
    else:
        # New item added
        messages.success(request, f"{menu_item.name} added to your cart!")

    return redirect('customer_menu', restaurant_id=menu_item.restaurant.id, username=username)


# Show Cart
def show_cart_page(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    # Fetch cart items with quantities
    cart_items = cart.cart_items.all() if cart else []
    total_price = cart.total_price() if cart else 0
    
    # Calculate additional details
    item_count = cart.total_items() if cart else 0
    delivery_fee = 30 if item_count > 0 else 0
    grand_total = total_price + delivery_fee

    return render(request, 'delivery/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'item_count': item_count,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total,
        'username': username,
    })



# Checkout View
def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.cart_items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'Your cart is empty!',
            'username': username,
        })

    # For testing/development, skip Razorpay integration if keys are not properly set
    try:
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create Razorpay order
        order_data = {
            'amount': int(total_price * 100),  # Amount in paisa
            'currency': 'INR',
            'payment_capture': '1',  # Automatically capture payment
        }
        order = client.order.create(data=order_data)
        order_id = order['id']
    except Exception as e:
        # Fallback for testing/development
        order_id = 'test_order_' + str(int(total_price * 100))

    # Pass the order details to the frontend
    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order_id,
        'amount': total_price,
    })


# Remove item from cart
def remove_from_cart(request, item_id, username):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, username=username)
        cart = Cart.objects.filter(customer=customer).first()
        
        if cart:
            cart_item = CartItem.objects.filter(cart=cart, menu_item_id=item_id).first()
            if cart_item:
                item_name = cart_item.menu_item.name
                cart_item.delete()
                messages.success(request, f'{item_name} removed from cart!')
        
        return redirect('show_cart_page', username=username)
    
    return redirect('show_cart_page', username=username)

# Clear entire cart
def clear_cart(request, username):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, username=username)
        cart = Cart.objects.filter(customer=customer).first()
        
        if cart:
            cart.cart_items.all().delete()
            messages.success(request, 'Cart cleared successfully!')
        
        return redirect('show_cart_page', username=username)
    
    return redirect('show_cart_page', username=username)

# Update cart item quantity (for future enhancement)
def update_cart_quantity(request, item_id, username):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, username=username)
        cart = Cart.objects.filter(customer=customer).first()
        quantity = int(request.POST.get('quantity', 1))
        
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        if cart and quantity > 0:
            # Update the CartItem quantity
            cart_item = CartItem.objects.filter(cart=cart, menu_item=menu_item).first()
            if cart_item:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, f'Updated {menu_item.name} quantity to {quantity}')
        
        return redirect('show_cart_page', username=username)
    
    return redirect('show_cart_page', username=username)

# Orders Page
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    # Fetch cart items and total price before clearing the cart
    cart_items = cart.cart_items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    # Clear the cart after fetching its details
    if cart:
        cart.cart_items.all().delete()

    return render(request, 'delivery/orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })
