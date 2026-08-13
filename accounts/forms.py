from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class PassengerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "username",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = User.Role.PASSENGER

        if commit:
            user.save()

        return user