from django.db import models
from django.contrib.auth.models import User


class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class RegistrationDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)
    house_no = models.IntegerField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)

    userpic = models.ImageField(upload_to="userpic/", blank=True, null=True)
    user_type = models.CharField(max_length=100, default='customer', editable=False)

    def __str__(self):
        return self.user.username
