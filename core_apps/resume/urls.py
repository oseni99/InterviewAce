from django.urls import path
from . import views


urlpatterns = [
    path("prep/", views.interview_preparation, name="interview_prep"),
    path("results/<int:user_id>", views.interview_results, name="interview_results"),
]
