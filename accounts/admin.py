from django.contrib import admin
from .models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'gender', 'phone_number', 'email', 'is_active', "is_staff", "is_superuser"]
    pass
