from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


# 1. Custom User Creation Form (For "Add User +" in Admin)
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "role",
            "nin",
            "abssin",
            "password1",
            "password2",
        )

# 2. Single Admin Registration for User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    # Prevents FieldError on non-editable date fields
    readonly_fields = ("date_joined", "last_login")

    # Table columns in admin panel
    list_display = (
        "username",
        "email",
        "phone",
        "role",
        "is_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )

    # Sidebar filter options
    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    # Search bar fields
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone",
        "nin",
        "abssin",
    )

    # Editing existing user form layout
    fieldsets = UserAdmin.fieldsets + (
        (
            "Transport & Verification Profile",
            {"fields": ("phone", "role", "nin", "abssin", "is_verified")},
        ),
    )

    # Adding new user form layout - Define explicitly without using UserAdmin.add_fieldsets
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "phone",
                    "role",
                    "nin",
                    "abssin",
                ),
            },
        ),
    )

    # Bulk actions for quick verification/role updates
    actions = ["mark_verified", "make_driver", "make_passenger"]

    @admin.action(description="Mark selected users as Verified")
    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Mark selected users as Drivers")
    def make_driver(self, request, queryset):
        queryset.update(role=User.Role.DRIVER)

    @admin.action(description="Mark selected users as Passengers")
    def make_passenger(self, request, queryset):
        queryset.update(role=User.Role.PASSENGER)