from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

User = get_user_model()


class PassengerRegistrationForm(forms.ModelForm):
    
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "minlength": 8,
                "maxlength": 64,
            }
        ),
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm password",
                "minlength": 8,
                "maxlength": 64,
            }
        ),
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
            "password",
            "confirm_password",
        ]

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if password:
            password_validation.validate_password(password)

        return password

    def clean(self):
        cleaned_data = super().clean() 

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Store the password securely using Django's password hashing
        user.set_password(self.cleaned_data["password"])

        # Every user created through this form is a passenger
        user.role = User.Role.PASSENGER

        if commit:
            user.save()

        return user


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