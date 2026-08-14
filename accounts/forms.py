from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class PassengerRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone",
            "nin",
            "abssin",
            "first_name",
            "last_name",
        ]

    def clean_nin(self):
        nin = self.cleaned_data.get("nin")
        if nin and (not nin.isdigit() or len(nin) != 11):
            raise ValidationError("NIN must be an 11-digit number.")
        return nin

    def clean_abssin(self):
        abssin = self.cleaned_data.get("abssin")
        if abssin and (not abssin.isdigit() or len(abssin) != 10):
            raise ValidationError("ABSSIN must be a 10-digit number.")
        return abssin

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = User.Role.PASSENGER
        if commit:
            user.save()
        return user