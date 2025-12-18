from django.contrib import admin
from .models import Multivendors, MenuBuild, Franchise


@admin.register(Multivendors)
class MultivendorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant_name', 'city', 'state', 'is_approved')
    list_filter = ('city', 'state', 'is_approved')
    search_fields = ('restaurant_name', 'user__username', 'city')


@admin.register(MenuBuild)
class MenuBuildAdmin(admin.ModelAdmin):
    list_display = ('id', 'food_name', 'price')
    search_fields = ('food_name',)

@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vender',
        'total_investment',
        'total_year_of_agreement',
        'profit_share',
    )

    list_filter = (
        'total_year_of_agreement',
        'profit_share',
        'vender',
    )

    search_fields = (
        'vender__vendor_full_name',  # change field as per Multivendors model
        'description',
    )

    ordering = ('id',)