from django.contrib import admin
from django.urls import path
from shoppingapp import views


urlpatterns = [
    path("", views.base, name="base"),

    
    path("data/", views.data, name="data"),
    path("display/", views.display, name="display"),

    # Profile & Dashboard
    path("profile_page/", views.Profile, name="profile_page"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("update_details/", views.update_details, name="update_details"),

    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Misc
    path("success/", views.success, name="success"),
]
