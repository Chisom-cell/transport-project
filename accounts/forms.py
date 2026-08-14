from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

User = get_user_model()




class PassengerRegistrationForm(forms.ModelForm):
    ...
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            password_validation.validate_password(password)
        return password
    # forms.py — PassengerRegistrationForm
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "minlength": 8, "maxlength": 64})
    )
    confirm_password = forms.CharField(
            widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "minlength": 8, "maxlength": 64})
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

class IdentityVerificationForm(forms.Form):
    nin = forms.CharField(max_length=11, label="NIN")
    abssin = forms.CharField(max_length=10, label="ABSSIN")

    def clean_nin(self):
        nin = self.cleaned_data.get("nin")
        if not nin.isdigit() or len(nin) != 11:
            raise ValidationError("NIN must be an 11-digit number.")
        return nin

    def clean_abssin(self):
        abssin = self.cleaned_data.get("abssin")
        if not abssin.isdigit() or len(abssin) != 10:
            raise ValidationError("ABSSIN must be a 10-digit number.")
        return abssin