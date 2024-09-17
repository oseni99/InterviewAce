from django import forms
from .models import Results
from core_apps.account.models import CustomUser


class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = Results
        fields = [
            "job_description",
        ]


class UpdateDetails(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["resume", "background_info", "achievement"]
