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