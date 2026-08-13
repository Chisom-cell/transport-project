from django import forms

from .models import Complaint


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint

        fields = [
            "trip",
            "vehicle",
            "category",
            "description",
        ]

        widgets = {
            "trip": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "vehicle": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "category": forms.Select(
                choices=[
                    ("", "Select complaint category"),
                    ("DRIVER_BEHAVIOUR", "Driver Behaviour"),
                    ("VEHICLE_CONDITION", "Vehicle Condition"),
                    ("FARE", "Fare Issue"),
                    ("SAFETY", "Safety"),
                    ("SERVICE", "Service"),
                    ("OTHER", "Other"),
                ],
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe your complaint...",
                }
            ),
        }