from .models import Cart

def cart_count(request):
    """Add cart item count to all templates"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(customer=request.user).first()
            if cart:
                count = cart.total_items()
                return {'cart_count': count}
        except Exception as e:
            print(f"Cart count error: {e}")
            return {'cart_count': 0}
    return {'cart_count': 0}