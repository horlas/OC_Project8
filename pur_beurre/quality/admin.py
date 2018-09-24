from django.contrib import admin
from .models import CustonUserModel


class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['username', "email", "password"]
    readonly_fields = ['created_at']

admin.site.register(CustonUserModel, CustomUserAdmin)