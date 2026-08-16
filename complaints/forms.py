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
                    "class": "form-select",
                }
            ),

            "vehicle": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "category": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter complaint category",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe your complaint",
                }
            ),
        }