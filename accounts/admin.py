from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "role",
            "organization",
            "nin",
            "abssin",
            "password1",
            "password2",
        )


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm

    readonly_fields = (
        "date_joined",
        "last_login",
    )

    list_display = (
        "username",
        "email",
        "phone",
        "role",
        "organization",
        "is_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "role",
        "organization",
        "is_verified",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone",
        "nin",
        "abssin",
        "organization__name",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Transport & Verification Profile",
            {
                "fields": (
                    "phone",
                    "role",
                    "organization",
                    "nin",
                    "abssin",
                    "is_verified",
                )
            },
        ),
    )

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
                    "organization",
                    "nin",
                    "abssin",
                ),
            },
        ),
    )

    actions = [
        "mark_verified",
        "make_driver",
        "make_passenger",
    ]

    @admin.action(description="Mark selected users as Verified")
    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Mark selected users as Drivers")
    def make_driver(self, request, queryset):
        queryset.update(role=User.Role.DRIVER)

    @admin.action(description="Mark selected users as Passengers")
    def make_passenger(self, request, queryset):
        queryset.update(role=User.Role.PASSENGER)