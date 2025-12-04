from django import forms
from .models import Multivendors, MenuBuild
from django.contrib.auth.models import User


# ----------------------------
# USER REGISTRATION FORM
# ----------------------------
class VendorForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # hash password
        if commit:
            user.save()
        return user


# ----------------------------
# VENDOR PROFILE FORM
# ----------------------------
class VenderReg(forms.ModelForm):
    class Meta:
        model = Multivendors
        fields = [
            'restaurant_name',
            'address',
            'city',
            'state',
            'zip_code',
            'restaurant_lic',
            'restaurant_img',
        ]
        widgets = {
            'restaurant_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ----------------------------
# MENU FORM
# ----------------------------
class MenuBuildForm(forms.ModelForm):
    class Meta:
        model = MenuBuild
        fields = ['food_name', 'price', 'food_img']
        widgets = {
            'food_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Food Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'food_img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }