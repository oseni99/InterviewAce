# after the resume is uploaded i want to take the resume and get the contavcts
import pdfplumber
from env import env
from core_apps.account.models import CustomUser
from .models import Results
from openai import OpenAI, OpenAIError


openai_key = env("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)


def pdf_to_txt(filename):
    try:
        with pdfplumber.open(filename) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            if not text:
                raise ValueError("No text could be extracted from this document")
            return text
    except Exception as e:
        print(f"An error occurred while parsing PDF: {str(e)}")
        return None


# analyze resume to get key skills


def analyze_resume(resume_text):
    try:
        # to be sure the resume text is provided or not
        if not resume_text:
            return None

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that specializes in analyzing resumes to extract key skills, experiences,and achievements.",
                },
                {
                    "role": "user",
                    "content": f"Analyze the following resume and extract key skills, experiences, and achievements:\n\n{resume_text}",
                },
            ],
        )
        # Extract the AI's response
        analyze_resume = response.choices[0].message["content"]
        return analyze_resume

    except OpenAIError as e:
        # Handle errors related to the OpenAI API
        print(f"An error occurred with OpenAI: {str(e)}")
        return None
    except Exception as e:
        # Handle any other generic errors
        print(f"An error occurred: {str(e)}")
        return None


def analyze_job_description(job_description):
    try:
        if not job_description:
            return None
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that specializes in  identifying key skills, responsibilities in a job description.",
                },
                {
                    "role": "user",
                    "content": f"Analyze the following job description and extract key skills and responsibilities:\n\n{job_description}",
                },
            ],
        )

        analyzed_job_description = response.choices[0].message["content"]
        return analyzed_job_description
    except OpenAIError as e:
        print(f"An error occurred with OpenAI: {str(e)}")
        return None
    except Exception as e:
        # TODO USE LOGGING LATER WHEN I WANT TO PUSH TO PRODUCTION
        print(f"An error occurred: {str(e)}")
        return None


def generate_interview_questions(user):
    results = Results.objects.filter(user=user).first()
    analyzed_job_description = results.analyzed_job_description

    if not analyzed_job_description:
        return None

    try:
        # use the job description to find interview questions
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that provides interview questions based on a job description.",
                },
                {
                    "role": "user",
                    "content": f"Analyze the following job description and provide Interview questions in respect to it:\n\n{analyzed_job_description}",
                },
            ],
        )

        interview_questions = response.choices[0].message["content"]
        if not interview_questions:
            print("No interview questions returned from OpenAI.")
            return None
        return interview_questions
    except OpenAIError as e:
        print(f"An error occurred with OpenAI: {str(e)}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def generate_interview_answers(request):
    user = request.user
    resume_text = user.parsed_resume  # in custom user model
    user_background = user.background_info  # in Custon user model
    results = Results.objects.filter(user=user).first()
    analyzed_job_description = results.analyzed_job_description  # in results model
    interview_questions = results.interview_questions  # in results model
    # use the resume and job description to find interview answers
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that provides answers to interview questions based on a job description, resume, and interview questions.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Given the following job description, resume details, and interview questions, "
                        f"provide well-crafted answers.\n\n"
                        f"Job Description: {analyzed_job_description}\n\n"
                        f"Resume: {resume_text}\n\n"
                        f"Interview Questions: {interview_questions}"
                    ),
                },
            ],
        )
        interview_answers = response.choices[0].message["content"]
        result, created = Results.objects.update_or_create(
            user=user,
            defaults={
                "analyzed_job_description": analyzed_job_description,
                "interview_questions": interview_questions,
                "interview_answers": interview_answers,
            },
        )
        return result
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
