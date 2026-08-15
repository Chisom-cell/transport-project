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
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Describe your complaint..."
                }
            ),
        }