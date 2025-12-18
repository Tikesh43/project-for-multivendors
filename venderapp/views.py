from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden,HttpResponse

from .models import Multivendors, MenuBuild, CartItem, Order, OrderItem,Franchise
from .forms import VenderReg, VendorForm, MenuBuildForm


# ====================== VENDOR REGISTER =========================

def ven_Register(request):
    registered = False

    if request.method == 'POST':
        form1 = VendorForm(request.POST)
        form2 = VenderReg(request.POST, request.FILES)
        
        if form1.is_valid() and form2.is_valid():

            vendor = form1.save(commit=False)
            vendor.set_password(form1.cleaned_data['password'])
            vendor.save()

            vendorprofile = form2.save(commit=False)
            vendorprofile.user = vendor
            vendorprofile.save()

            registered = True

    else:
        form1 = VendorForm()
        form2 = VenderReg()

    return render(request, 'vendors/ven_register.html', {
        "form1": form1,
        "form2": form2,
        "registered": registered,
    })


# ====================== MENU ADD ================================
# @login_required(login_url='login')
# def add_menu(request, vendor_id):
#     vendor = get_object_or_404(Multivendors, id=vendor_id)

#     if request.method == 'POST':
#         form = MenuBuildForm(request.POST, request.FILES)
#         if form.is_valid():
#             menu_item = form.save(commit=False)
#             menu_item.vendor = vendor
#             menu_item.save()
#             return redirect('dashboard')
#     form = MenuBuildForm()
#     return render(request, 'vendors/add_menu.html', {'form': form, 'vendor': vendor})

@login_required(login_url='login')
def add_menu(request, vendor_id):
    # Logged in vendor
    logged_in_vendor = request.user.multivendors 
    # Vendor from URL
    vendor = get_object_or_404(Multivendors, id=vendor_id)
    # SECURITY CHECK: Prevent adding menu to other vendors
    if vendor != logged_in_vendor:
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        form = MenuBuildForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.vendor = vendor
            menu_item.save()
            return redirect('dashboard')

    form = MenuBuildForm()
    return render(request, 'vendors/add_menu.html', {
        'form': form,
        'vendor': vendor
    })


# ====================== VENDOR LIST & DETAILS ====================

@login_required(login_url="login")
def vendor_list(request):
    vendors = Multivendors.objects.all()
    return render(request, 'vendors/shop_list.html', {'vendors': vendors})


@login_required(login_url="login")
def vendor_detail(request, pk):
    vendor = Multivendors.objects.get(id=pk)
    menus = MenuBuild.objects.filter(vendor=vendor)
    return render(request, 'vendors/vendors_details.html', {
        'vendor': vendor,
        'menus': menus
    })

@login_required(login_url="login")
def get_menu(request, vendor_id):
    vendor = get_object_or_404(Multivendors, id=vendor_id)
    menus = MenuBuild.objects.filter(vendor=vendor)
    return render(request, 'vendors/vendors_details.html', {
        'vendor': vendor,
        'menus': menus
    })


# ====================== ORDER PAGE ===============================
@login_required(login_url="login")
def order_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'vendors/order.html', {
        'cart_items': cart_items
    })

# ====================== CART COUNTER =============================
@login_required(login_url="login")
def cart_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'cart_count': count}


# ====================== ADD TO CART ==============================

@login_required(login_url="login")
def add_to_cart(request, food_id):

    food = get_object_or_404(MenuBuild, id=food_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        food=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('order_page')   # FIXED


# ====================== EDIT MENU ===============================
@login_required(login_url="login")
def edit_menu(request, id):
    menu = get_object_or_404(MenuBuild, id=id)

    if request.user != menu.vendor.user:
        return HttpResponseForbidden("Not authorized")

    if request.method == "POST":
        form = MenuBuildForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            return redirect("vendors_details", pk=menu.vendor.id)

    form = MenuBuildForm(instance=menu)
    return render(request, "vendors/edit_food.html", {"form": form, "menu": menu})


# ====================== DELETE MENU ===============================
@login_required(login_url="login")
def delete_menu(request, id):
    menu = get_object_or_404(MenuBuild, id=id)

    if request.user != menu.vendor.user:
        return HttpResponseForbidden("Not authorized")

    vendor_id = menu.vendor.id
    menu.delete()

    return redirect("vendors_details", pk=vendor_id)


# ====================== CART PAGE ===============================
@login_required(login_url="login")
def cart_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'vendors/cart.html', {
        'cart_items': cart_items
    })


@login_required(login_url="login")
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.total_price for item in cart_items)
    return render(request, 'vendors/checkout.html', {'cart_items': cart_items, 'cart_total': cart_total})


@login_required(login_url="login")
def place_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('checkout')

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method', 'Cash')

        # Update quantities and calculate total
        total_amount = 0
        for item in cart_items:
            qty_str = request.POST.get(f'item_{item.id}')
            if qty_str and qty_str.isdigit():
                item.quantity = int(qty_str)
                item.save()
            total_amount += item.total_price

        # Ensure all items are from the same vendor
        vendors = set(item.food.vendor for item in cart_items)
        if len(vendors) > 1:
            return HttpResponse("Cart contains items from multiple vendors. Please checkout separately.")
        vendor = vendors.pop()

        # Create order
        order = Order.objects.create(
            user=request.user,
            vendor=vendor,
            name=name,
            phone=phone,
            address=address,
            payment_method=payment_method,
            total_amount=total_amount
        )

        # Save ordered items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food=item.food,
                quantity=item.quantity,
                price=item.food.price
            )

        # Clear cart
        cart_items.delete()

        return redirect('order_success')

    return redirect('checkout')


@login_required(login_url="login")
def order_success(request):
    return render(request, 'vendors/order_success.html')


# def franchise(request, id):
#     vendor = Multivendors.objects.get(id=id)

#     franchise, created = Franchise.objects.get_or_create(vender=vendor)

#     return render(request, "franchise.html", {"franchise": franchise, "vendor": vendor})

@login_required(login_url="login")
def franchise(request, id):
    vendor = Multivendors.objects.get(id=id)
    franchise = Franchise.objects.filter(vender=vendor).first()

    return render(request, "vendors/franchise.html", {
        "franchise": franchise,
        "vendor": vendor
    })

# def emi_cal(request, franchise_id):
#     franchise = get_object_or_404(Franchise, id=franchise_id)
#     return render(request, 'vendors/emi_cal.html', {'franchise': franchise})


@login_required(login_url="login")
def emi_cal(request, franchise_id):
    franchise = get_object_or_404(Franchise, id=franchise_id)
    
    result = None
    error = None
    
    # Allowed tenure and corresponding interest rates
    interest_rates = {1: 13, 2: 11, 5: 10, 7: 9, 10: 8}
    allowed_tenures = interest_rates.keys()

    if request.method == 'POST':
        try:
            loan_amount = float(request.POST.get('loan_amount', franchise.total_investment))
            loan_tenure = int(request.POST.get('loan_tenure', franchise.total_year_of_agreement))
            
            # Validation checks
            if loan_amount <= 0 or loan_amount > franchise.total_investment:
                error = f"Loan amount must be greater than 0 and less than or equal to ₹{franchise.total_investment}."
            elif loan_tenure not in allowed_tenures:
                error = f"Loan tenure must be one of the following: {', '.join(map(str, allowed_tenures))} years."
            else:
                interest_rate = interest_rates[loan_tenure]
                
                P = loan_amount
                annual_rate = interest_rate
                R = annual_rate / 12 / 100
                N = loan_tenure * 12
                
                if R == 0:
                    emi = P / N
                else:
                    numerator = P * R * (1 + R) ** N
                    denominator = (1 + R) ** N - 1
                    emi = numerator / denominator
                
                total_payment = emi * N
                total_interest = total_payment - P
                
                result = {
                    'emi': round(emi, 2),
                    'total_payment': round(total_payment, 2),
                    'total_interest': round(total_interest, 2),
                    'loan_amount': loan_amount,
                    'loan_tenure': loan_tenure,
                    'interest_rate': interest_rate,
                }
        except Exception:
            error = "Invalid input. Please enter valid numbers."
    
    else:
        # Default values on GET
        default_tenure = franchise.total_year_of_agreement if franchise.total_year_of_agreement in allowed_tenures else 5
        default_rate = interest_rates.get(default_tenure, 10)
        result = {
            'loan_amount': franchise.total_investment,
            'loan_tenure': default_tenure,
            'interest_rate': default_rate,
        }
    
    context = {
        'franchise': franchise,
        'result': result,
        'error': error,
    }
    return render(request, 'vendors/emi_cal.html', context)


@login_required(login_url="login")
def mark_order_delivered(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'delivered'
    order.save()
    return redirect('dashboard')

@login_required(login_url="login")
def vendor_orders(request):
    user = request.user

    # Only vendors can access
    if not hasattr(user, 'multivendors'):
        return redirect('dashboard')

    multivendors = user.multivendors

    orders = Order.objects.filter(vendor=multivendors).order_by('-created_at')

    context = {
        'orders': orders,
        'multivendors': multivendors,
        'user_type': 'vendor',
    }

    return render(request, 'vendor_orders.html', context)

@login_required(login_url="login")
def mark_order_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'delivered'
    order.save()
    return redirect('vendor_orders')


@login_required(login_url="login")
def order_history(request):
    if not request.user.is_authenticated:
        # Redirect to login if not logged in
        return redirect('login')

    # Fetch only the orders for the logged-in customer
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'vendors/order_history.html', context)