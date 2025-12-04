from django.contrib import admin
from .models import Multivendors, MenuBuild


@admin.register(Multivendors)
class MultivendorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant_name', 'city', 'state', 'is_approved')
    list_filter = ('city', 'state', 'is_approved')
    search_fields = ('restaurant_name', 'user__username', 'city')


@admin.register(MenuBuild)
class MenuBuildAdmin(admin.ModelAdmin):
    list_display = ('id', 'food_name', 'price')
    search_fields = ('food_name',)
