from django.urls import path
from . import views

urlpatterns = [
    # Vendor-related pages
    path('vendor_list/', views.vendor_list, name='vendor_list'),  # List all vendors/restaurants
    path('ven_register/', views.ven_Register, name='ven_register'),  # Vendor registration form
    path('vendors_details/<int:pk>/', views.vendor_detail, name='vendors_details'),  # Detailed page for a specific vendor
    path('vendor/orders/', views.vendor_orders, name='vendor_orders'),  # List orders received by the vendor

    # Menu management
    path('menu/add/<int:vendor_id>/', views.add_menu, name='add_menu'),  # Add new menu item for a vendor
    path('menu/<int:vendor_id>/', views.get_menu, name='get_menu'),  # View menu of a vendor
    path('menu/edit/<int:id>/', views.edit_menu, name="edit_menu"),  # Edit a specific menu item
    path('menu/delete/<int:id>/', views.delete_menu, name="delete_menu"),  # Delete a specific menu item

    # Ordering & cart
    path('order/', views.order_page, name='order_page'),  # Order page to view items and select quantity
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),  # Add a food item to cart
    path('cart/', views.cart_page, name='cart_page'),  # View cart contents
    path('checkout/', views.checkout, name='checkout'),  # Checkout page to confirm order
    path('place_order/', views.place_order, name='place_order'),  # Finalize and place the order
    path('order_success/', views.order_success, name='order_success'),  # Success page after placing order
    path('order_history/', views.order_history, name='order_history'),

    # Franchise & EMI
    path('franchise/<int:id>/', views.franchise, name='franchise'),  # View franchise details
    path('emi/<int:franchise_id>/', views.emi_cal, name='emi_cal'),  # Calculate EMI for a franchise

    # Order management for vendor
    path('vendor/orders/delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),  # Mark order as delivered
]
