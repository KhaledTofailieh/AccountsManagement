from django.contrib import admin
from accounts.models import User


# registering "User" in admin panel
@admin.register(User)
class UserRegister(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'birth_date', 'created_at', 'type', 'status']
    list_filter = ['status', 'created_at', 'type']
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'created_at'
    ordering = ['status', 'type', 'created_at']
