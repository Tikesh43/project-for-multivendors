from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Multivendors
from .forms import VenderReg, VendorForm, MenuBuildForm



def ven_Register(request):
    registered = False

    if request.method == 'POST':
        form1 = VendorForm(request.POST)
        form2 = VenderReg(request.POST, request.FILES)
        
        if form1.is_valid() and form2.is_valid():

            # SAVE USER
            vendor = form1.save(commit=False)
            vendor.set_password(form1.cleaned_data['password'])   # Hash password
            vendor.save()

            # SAVE VENDOR PROFILE
            vendorprofile = form2.save(commit=False)
            vendorprofile.user = vendor
            vendorprofile.save()

            registered = True

    else:
        form1 = VendorForm()
        form2 = VenderReg()

    context = {
        "form1": form1,
        "form2": form2,
        "registered": registered,
    }

    return render(request, 'vendors/ven_register.html', context)


@login_required(login_url='login')
def add_menu(request, vendor_id):
    vendor = get_object_or_404(Multivendors, id=vendor_id)

    if request.method == 'POST':
        form = MenuBuildForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.vendor = vendor  # link menu to vendor
            menu_item.save()
            return redirect('dashboard')  # redirect to dashboard after saving
    else:
        form = MenuBuildForm()

    context = {
        'form': form,
        'vendor': vendor
    }
    return render(request, 'vendors/add_menu.html', context)

@login_required(login_url="login")
def vendor_list(request):
    vendors = Multivendors.objects.all()
    return render(request, 'vendors/shop_list.html', {'vendors': vendors})

@login_required(login_url="login")
def vendor_detail(request, pk):
    vendor = Multivendors.objects.get(id=pk)
    return render(request, 'vendors/vendors_details.html', {'vendor': vendor})
