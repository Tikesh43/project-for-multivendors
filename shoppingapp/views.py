from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  BasicUpdateForm
from .models import  RegistrationDetails
from venderapp.models import Multivendors,MenuBuild,Order
from shoppingapp.forms import RegistrationForm, RegisterDetails
from django.contrib.auth.models import User


# ------------------- Employee Views -------------------

def data(request):
    employees = Employee.objects.all()
    return render(request, "data.html", {"employees": employees})


def display(request):
    emp_data = Employee.objects.all()
    return render(request, "display.html", {"emp_data": emp_data})


def success(request):
    return render(request, 'success.html')


def base(request):
    user = request.user
    context = {}
    if hasattr(user, "multivendors"):
        context['user_type'] = 'vendor'
    elif hasattr(user, "registrationdetails"):
        context['user_type'] = 'customer'
    else:
        context['user_type'] = 'unknown'
    # return render(request, "dashboard.html", context)
    return render(request, "base.html", context)

def Profile(request):
    return render(request, "profile_page.html")


# ------------------- Registration -------------------
def register(request):
    if request.method == 'POST':
        forms1 = RegistrationForm(request.POST)
        forms2 = RegisterDetails(request.POST, request.FILES)

        if forms1.is_valid() and forms2.is_valid():
            # Create user
            user = forms1.save(commit=False)
            user.set_password(forms1.cleaned_data['password'])
            user.save()

            # Create customer profile
            profile = forms2.save(commit=False)
            profile.user = user
            profile.user_type = "customer"  # IMPORTANT
            profile.save()

            messages.success(request, "Registration successful!")
            return redirect("login")

    else:
        forms1 = RegistrationForm()
        forms2 = RegisterDetails()

    return render(request, "registration.html", {
        "forms1": forms1,
        "forms2": forms2,
    })


# ------------------- Login -------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            # Vendor?
            if hasattr(user, "multivendors"):
                return redirect("dashboard")

            # Customer?
            if hasattr(user, "registrationdetails"):
                return redirect("dashboard")

            messages.error(request, "User type not found!")
            return redirect("login")

        messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# ------------------- Dashboard -------------------
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    context = {}

    # ================= VENDOR DASHBOARD =================
    if hasattr(user, "multivendors"):
        multivendors = user.multivendors

        context['user_type'] = 'vendor'
        context['multivendors'] = multivendors

        # ✅ Vendor-wise menu items
        context['menu_items'] = MenuBuild.objects.filter(
            vendor=multivendors
        )

        # ✅ ORDER COUNTS (ADD HERE 👇)
        context['received_orders_count'] = Order.objects.filter(
            status='received'
        ).count()

        context['cancelled_orders_count'] = Order.objects.filter(
            status='cancelled'
        ).count()

        context['delivered_orders_count'] = Order.objects.filter(
            status='delivered'
        ).count()

    # ================= CUSTOMER DASHBOARD =================
    elif hasattr(user, "registrationdetails"):
        customer = user.registrationdetails

        context['user_type'] = 'customer'
        context['customer'] = customer

    # ================= UNKNOWN =================
    else:
        context['user_type'] = 'unknown'

    return render(request, "dashboard.html", context)

# ------------------- Logout -------------------

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------- Update Profile -------------------

@login_required(login_url="login")
def update_details(request):
    user = request.user

    if request.method == 'POST':
        user_form = BasicUpdateForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard')

    else:
        user_form = BasicUpdateForm(instance=user)

    return render(request, 'update_basic.html', {
        'user_form': user_form,
    })
