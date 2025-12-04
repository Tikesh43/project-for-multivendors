from django.contrib import admin
from .models import Registration, RegistrationDetails


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(RegistrationDetails)
class RegistrationDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'state', 'zipcode', 'user_type')
    search_fields = ('user__username', 'phone', 'city')
