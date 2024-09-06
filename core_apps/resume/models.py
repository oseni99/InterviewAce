from django.db import models
from core_apps.account.models import CustomUser
from django.utils.translation import gettext_lazy as _


class Results(models.Model):
    interview_questions = models.TextField(_("Interview Question"))
    interview_answers = models.TextField(_("Answer"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    user = models.ForeignKey(
        CustomUser, verbose_name=_("User"), on_delete=models.CASCADE
    )
    job_description = models.TextField(
        _("Job Description"), default=None, blank=True, null=True
    )
    analyzed_job_description = models.TextField(
        _("Analyzed Job Description"), default=None, blank=True, null=True
    )
    analyzed_resume = models.TextField(
        _("Analyzed Resume"), default=None, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Result")
        verbose_name_plural = _("Results")

    def __str__(self):
        return f"{self.user} -> {self.interview_questions[:100]}"
