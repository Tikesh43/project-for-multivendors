from django.urls import path
from . import views

urlpatterns = [
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('ven_register/', views.ven_Register, name='ven_register'),
    path('vendors_details/<int:pk>/', views.vendor_detail, name='vendors_details'),

    # path('add-menu/', views.add_menu, name='add_menu'),
    path('menu/add/<int:vendor_id>/', views.add_menu, name='add_menu'),
    # path('menu-list/', views.menu_list, name='menu_list'),  # NEW URL
]
