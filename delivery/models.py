from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Customer(AbstractUser):
    # Inherits username, password, email, first_name, last_name from AbstractUser
    mobile = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    
    # Add related_name to resolve clashes with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customer_groups",
        related_query_name="customer",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customer_permissions",
        related_query_name="customer",
    )
    
    def __str__(self):
        return self.username

    

class Restaurant(models.Model):
    name = models.CharField(max_length = 20)
    picture = models.URLField(max_length = 200, default="https://cwdaust.com.au/wpress/wp-content/uploads/2015/04/placeholder-restaurant.png")
    cuisine = models.CharField(max_length = 200)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.name} {self.cuisine} {self.rating}/5"
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name = "menu_items")
    name = models.CharField(max_length = 20)
    picture = models.URLField(max_length = 200, default="https://cdn-icons-png.flaticon.com/512/1147/1147856.png")
    description = models.CharField(max_length = 200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_veg = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.name} {self.description} {self.price}"
    
class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete = models.CASCADE, related_name = "cart")
    items = models.ManyToManyField("MenuItem",related_name="carts")

    def total_price(self):
        return self.items.aggregate(total=Sum('price'))['total'] or 0.00

    def __str__(self):
        return f"Cart for {self.customer.username}"