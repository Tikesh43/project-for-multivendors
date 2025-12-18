from django.db import models
from django.contrib.auth.models import User


# ------------ Vendor Registration (Basic) ------------ #

class VendorRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# ------------ Vendor Full Profile (Multi-Vendor) ------------ #

class Multivendors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    restaurant_name = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    restaurant_lic = models.ImageField(upload_to="licence_pic/", blank=True, null=True)
    restaurant_img = models.ImageField(upload_to="restaurant_pic/", blank=True, null=True)

    user_type = models.CharField(max_length=100, default='vendor', editable=False)
    is_approved = models.BooleanField(default=False)

    franchise = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# ------------ Menu Build (Add Food Items) ------------ #

class MenuBuild(models.Model):
    vendor = models.ForeignKey(Multivendors, on_delete=models.CASCADE, related_name="menu_items")  # link to vendor
    food_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    food_img = models.ImageField(upload_to="food_img/", blank=True, null=True)

    def __str__(self):
        return f"{self.food_name} - {self.vendor.restaurant_name}"
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional if you want user-based cart
    food = models.ForeignKey(MenuBuild, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.food.price * self.quantity

    def __str__(self):
        return f"{self.food.food_name} x {self.quantity}"
    
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Multivendors, on_delete=models.CASCADE)  # Add this

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(MenuBuild, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of food price

    def __str__(self):
        return f"{self.food.food_name} ({self.quantity})"


class Franchise(models.Model):
    vender = models.ForeignKey(
        Multivendors,
        on_delete=models.CASCADE,
        related_name='franchises'
    )
    total_investment = models.DecimalField(max_digits=10, decimal_places=2)
    total_year_of_agreement = models.IntegerField()
    profit_share = models.IntegerField()
    description = models.TextField(null=True, blank=True)
