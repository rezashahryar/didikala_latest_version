from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ('mobile',)
    search_fields = ('mobile',)
    list_filter = ('is_active', 'is_superuser')
    list_display = ['mobile', 'is_superuser', 'is_staff', 'is_active', 'email']

    fieldsets = (
        ('Authentication', {
            "fields": (
                'mobile', 'email', 'password', 'first_name', 'last_name'
            ),
        }),
        ('group permissions', {
            'fields': (
                'user_permissions', 'groups',
            )
        }),
        ('Permissions', {
            'fields': (
            'is_staff', 'is_active', 'is_superuser'
            ),
        }),
        ('last login', {
            'fields': (
            'last_login',
            ),
        }),
    )

    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')
        }),
    )
    