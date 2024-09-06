from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .services import validate_file, validate_linkedin_profile
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=150)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    resume = models.FileField(
        _("Resume"), upload_to="resumes/", max_length=100, validators=[validate_file]
    )
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)
    linkedin_profile = models.URLField(
        _("Linkedin Profile"),
        max_length=200,
        blank=True,
        null=True,
        validators=[validate_linkedin_profile],
    )
    github_profile = models.CharField(
        _("GitHub Username"), max_length=50, blank=True, null=True
    )
    profile_picture = models.ImageField(
        _("Profile Picture"),
        upload_to="profile_pics",
        max_length=None,
        blank=None,
        null=True,
        help_text="Image size should be png.",
    )
    industry_choice = models.CharField(
        _("Industry"), max_length=80, blank=True, null=True
    )
    year_of_experience = models.PositiveSmallIntegerField(
        _("Year of Experience"), blank=True, null=True
    )
    background_info = models.TextField(
        _("Background Information"), default=None, blank=True, null=True
    )
    achievement = models.TextField(
        _("Achievements"), default=None, blank=True, null=True
    )
    parsed_resume = models.TextField(
        _("Parsed Resume"), default=None, blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "resume"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} -> {self.email}"
