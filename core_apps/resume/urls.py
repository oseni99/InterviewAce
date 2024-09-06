from django.urls import path
from . import views


urlpatterns = [
    path("prep/", views.interview_prep_stg, name="interview_stage1"),
    path("results/<int:user_id>", views.interview_results, name="interview_results"),
]
