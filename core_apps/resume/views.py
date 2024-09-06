from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core_apps.account.models import CustomUser
from .models import Results
from .forms import UpdateDetails
from .service import pdf_to_txt, get_results


def interview_prep_stg(request):
    form = UpdateDetails(instance=request.user)
    if request.method == "POST":
        form = UpdateDetails(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            resume = user.resume
            resume_text = pdf_to_txt(resume)
            user.parsed_resume = resume_text
            user.save()
            return redirect("interview_results", user_id=user.id)
    return render(request, "resume/intstage1.html", {"form": form})


def interview_results(request, user_id):
    results = get_results(user_id)
    if isinstance(results, Results):
        return render(request, "resume/the_results.html", {"results": results})
    else:
        return render(request, "resume/the_results.html", {"error": results})


# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
#         },
#         {
#             "role": "user",
#             "content": "Compose a poem that explains the concept of recursion in programming.",
#         },
#     ],
# )
