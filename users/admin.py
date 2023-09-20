from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ["email", 'first_name', 'last_name', "is_admin"]
    list_filter = ["is_admin"]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

    # the fieldsets for the user change and user add forms
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ['first_name', 'last_name', "phone", 'address']}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    # Customize the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_admin'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
