from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "resume",
            "linkedin_profile",
            "github_profile",
            "profile_picture",
            "industry_choice",
            "year_of_experience",
            "password1",
            "password2",
        )

    usable_password = None
