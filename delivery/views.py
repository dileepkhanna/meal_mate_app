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
    # Get the referer to redirect back to the appropriate page
    referer = request.META.get('HTTP_REFERER', '')
    
    # Determine which page to redirect to
    if 'signup' in referer:
        redirect_page = 'signup'
        page_name = 'sign up'
    else:
        redirect_page = 'signin'
        page_name = 'sign in'
    
    messages.error(request, f'Security token expired. Please refresh and try to {page_name} again.')
    return redirect(redirect_page)

# Home Page
def index(request):
    return render(request, 'delivery/index.html')

# Sign In Page (handles both GET and POST)
def signin(request):
    if request.method == 'POST':
        # Handle signin submission
        return handle_login(request)
    else:
        # Show signin form
        get_token(request)
        return render(request, 'delivery/signin.html')

# Sign Up Page (handles both GET and POST)
def signup(request):
    if request.method == 'POST':
        # Handle signup submission
        return handle_signup(request)
    else:
        # Show signup form
        get_token(request)
        return render(request, 'delivery/signup.html')

# Handle Customer Login
def handle_login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        from django.contrib.auth import authenticate, login
        
        # Try to find customer by mobile number
        try:
            customer = Customer.objects.get(mobile=mobile)
            # Authenticate using username (since Django auth uses username)
            user = authenticate(request, username=customer.username, password=password)
            
            if user is not None and isinstance(user, Customer):
                # Check if user is not staff (regular customer)
                if not user.is_staff and not user.is_superuser:
                    login(request, user)
                    return redirect('customer_home', username=user.username)
                else:
                    messages.error(request, 'Please use admin login for admin accounts.')
                    return redirect('signin')
            else:
                messages.error(request, 'Invalid phone number or password.')
                return redirect('signin')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid phone number or password.')
            return redirect('signin')
    else:
        return redirect('signin')

# Handle Admin Login
def handle_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        from django.contrib.auth import authenticate, login
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is staff or superuser (admin)
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('admin_home')
            else:
                messages.error(request, 'Access denied. Admin credentials required.')
                return redirect('admin_signin')
        else:
            messages.error(request, 'Invalid admin username or password.')
            return redirect('admin_signin')
    else:
        return redirect('admin_signin')

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

        # Validate password strength
        import re
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('signup')
        if not re.search(r'[A-Z]', password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return redirect('signup')
        if not re.search(r'[a-z]', password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            return redirect('signup')
        if not re.search(r'\d', password):
            messages.error(request, 'Password must contain at least one number.')
            return redirect('signup')
        if not re.search(r'[@$!%*?&]', password):
            messages.error(request, 'Password must contain at least one special character (@$!%*?&).')
            return redirect('signup')

        # Check for duplicate username
        if Customer.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('signup')
        
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return redirect('signup')
        
        if Customer.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Phone number already registered. Please use a different number.')
            return redirect('signup')

        # Create customer user with hashed password (not staff)
        customer = Customer.objects.create_user(
            username=username,
            password=password,
            email=email,
            mobile=mobile,
            address=address,
            is_staff=False,  # Ensure customer is not staff
            is_superuser=False  # Ensure customer is not superuser
        )
        messages.success(request, 'Account created successfully! Please sign in.')
        return redirect('signin')
    else:
        # Handle GET requests by redirecting to signup page
        return redirect('signup')

# Admin Sign In Page (handles both GET and POST)
def admin_signin(request):
    if request.method == 'POST':
        # Handle admin signin submission
        return handle_admin_login(request)
    else:
        # Show admin signin form
        get_token(request)
        return render(request, 'delivery/admin_signin.html')

# Admin Sign Up Page (handles both GET and POST)
def admin_signup(request):
    if request.method == 'POST':
        # Handle admin signup submission
        return handle_admin_signup(request)
    else:
        # Show admin signup form
        get_token(request)
        return render(request, 'delivery/admin_signup.html')

# Handle Admin Sign Up
def handle_admin_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        admin_code = request.POST.get('admin_code')

        # Verify admin access code (you should change this to a secure code)
        ADMIN_ACCESS_CODE = "1425"  # Change this to your secure code
        
        if admin_code != ADMIN_ACCESS_CODE:
            messages.error(request, 'Invalid admin access code. Contact system administrator.')
            return redirect('admin_signup')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('admin_signup')

        # Validate password strength
        import re
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('admin_signup')
        if not re.search(r'[A-Z]', password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return redirect('admin_signup')
        if not re.search(r'[a-z]', password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            return redirect('admin_signup')
        if not re.search(r'\d', password):
            messages.error(request, 'Password must contain at least one number.')
            return redirect('admin_signup')
        if not re.search(r'[@$!%*?&]', password):
            messages.error(request, 'Password must contain at least one special character (@$!%*?&).')
            return redirect('admin_signup')

        # Check for duplicate username in Customer model
        if Customer.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('admin_signup')
        
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return redirect('admin_signup')

        # Create admin user using Customer model with staff privileges
        admin_user = Customer.objects.create_user(
            username=username,
            password=password,
            email=email,
            mobile='',  # Admin doesn't need mobile
            address='',  # Admin doesn't need address
            is_staff=True,  # Make them staff (admin)
            is_superuser=False  # Not superuser by default
        )
        
        messages.success(request, 'Admin account created successfully! Please sign in.')
        return redirect('admin_signin')
    else:
        return redirect('admin_signup')

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





# ================================
# PASSWORD RESET SYSTEM
# ================================

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string

def forgot_password(request):
    """Show forgot password page"""
    if request.method == 'POST':
        return handle_forgot_password(request)
    else:
        get_token(request)
        return render(request, 'delivery/forgot_password.html')

def handle_forgot_password(request):
    """Handle forgot password request"""
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # Can be email, username, or phone
        
        # Find user by email, username, or phone
        user = None
        try:
            if '@' in identifier:
                user = Customer.objects.get(email=identifier)
            elif identifier.isdigit() and len(identifier) == 10:
                user = Customer.objects.get(mobile=identifier)
            else:
                user = Customer.objects.get(username=identifier)
        except Customer.DoesNotExist:
            # Don't reveal if user exists or not (security)
            messages.success(request, 'If an account exists with that information, a password reset link has been sent.')
            return redirect('signin')
        
        # Check if user has email
        if not user.email:
            messages.error(request, 'No email associated with this account. Please contact support.')
            return redirect('forgot_password')
        
        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset link
        reset_link = request.build_absolute_uri(
            f'/reset-password/{uid}/{token}/'
        )
        
        # Send email
        subject = 'Reset Your Meal Mate Password'
        message = f"""
Hello {user.username},

You requested to reset your password for Meal Mate.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
Meal Mate Team
"""
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link has been sent to your email.')
        except Exception as e:
            print(f"Error sending email: {e}")
            messages.error(request, 'Failed to send reset email. Please try again.')
            return redirect('forgot_password')
        
        return redirect('signin')
    
    return redirect('forgot_password')

def reset_password(request, uidb64, token):
    """Show reset password page"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            return handle_reset_password(request, user)
        else:
            get_token(request)
            return render(request, 'delivery/reset_password.html', {
                'uidb64': uidb64,
                'token': token,
                'validlink': True
            })
    else:
        messages.error(request, 'Password reset link is invalid or has expired.')
        return redirect('forgot_password')

def handle_reset_password(request, user):
    """Handle password reset submission"""
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect(request.path)
        
        # Validate password strength
        import re
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect(request.path)
        if not re.search(r'[A-Z]', password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return redirect(request.path)
        if not re.search(r'[a-z]', password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            return redirect(request.path)
        if not re.search(r'\d', password):
            messages.error(request, 'Password must contain at least one number.')
            return redirect(request.path)
        if not re.search(r'[@$!%*?&]', password):
            messages.error(request, 'Password must contain at least one special character (@$!%*?&).')
            return redirect(request.path)
        
        # Set new password
        user.set_password(password)
        user.save()
        
        messages.success(request, 'Password reset successful! Please sign in with your new password.')
        return redirect('signin')
    
    return redirect('signin')
