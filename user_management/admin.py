from django.contrib import admin

from .models import CustomUser, CustomUserManager
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser','is_staff')
    