from django import forms
from core_apps.account.models import CustomUser


class UpdateDetails(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("resume", "job_description", "background_info", "achievement")
