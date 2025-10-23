from django.contrib import admin

# Register your models here.
from .models import Customer, Restaurant, MenuItem, Cart, CartItem
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(CartItem)
