from django import forms
from django.contrib.auth.models import User
from shoppingapp.models import RegistrationDetails

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


# ---------------- User Registration Form ---------------- #

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# ---------------- Registration Details Form ---------------- #

class RegisterDetails(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = RegistrationDetails
        fields = [
            'phone', 'house_no', 'street',
            'city', 'state', 'zipcode', 'userpic'
        ]


# ---------------- Update Basic User Details ---------------- #

class BasicUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        }


# ---------------- Update Only Phone Number ---------------- #

class PhoneUpdateForm(forms.ModelForm):
    class Meta:
        model = RegistrationDetails
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
        }
