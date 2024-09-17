from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core_apps.account.models import CustomUser
from .models import Results
from .forms import UpdateDetails, JobDescriptionForm
from .service import (
    pdf_to_txt,
    get_results,
    analyze_resume,
    analyze_job_description,
    generate_interview_answers,
    generate_interview_questions,
)
from django.contrib import messages


@login_required
def interview_preparation(request):
    result, created = Results.objects.get_or_create(user=request.user)

    # Initializing the forms to be able to update previous user details or update job description / upload newly created
    user_form = UpdateDetails(instance=request.user)
    job_form = JobDescriptionForm(instance=result)

    if request.method == "POST":
        # handle both forms requests
        user_form = UpdateDetails(request.POST, request.FILES, instance=request.user)
        job_form = JobDescriptionForm(request.POST, instance=result)

        if user_form.is_valid() and job_form.is_valid():
            user = user_form.save(commit=False)
            resume = user.resume

            resume_text = pdf_to_txt(resume)
            if resume_text:
                user.parsed_resume = resume_text
            user.save()
            try:
                result.analyzed_resume = analyze_resume(resume_text)
                result.analyzed_job_description = analyze_job_description(
                    result.job_description
                )
                result.save()
            except Exception as e:
                print(f"Error processing resume: {str(e)}")
                messages.error(
                    request,
                    "There was an error processing your resume. Please try again.",
                )
                return render(
                    request,
                    "resume/interview_stage_1.html",
                    {
                        "user_form": user_form,
                        "job_form": job_form,
                        "user_id": request.user.id,
                    },
                )
        return redirect(
            "interview_prep", user_id=user.id
        )  # Redirect to the next step or success page
    return render(
        request,
        "resume/interview_stage_1.html",
        {"user_form": user_form, "job_form": job_form, "user_id": request.user.id},
    )

@login_required
def interview_results(request, user_id):
    interview_questions_results = generate_interview_questions_results(