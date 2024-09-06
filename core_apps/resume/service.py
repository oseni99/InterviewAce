# after the resume is uploaded i want to take the resume and get the contavcts
import pdfplumber
from env import env
from core_apps.account.models import CustomUser
from .models import Results
from openai import OpenAI


openai_key = env("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)


def pdf_to_txt(filename):
    with pdfplumber.open(filename) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text


# analyze resume to get key skills


def analyze_resume(request):
    try:
        user = request.user
        resume_text = user.parsed_resume
        # using the OPEN AI model to analyze the resume to get key skills
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that specializes in analyzing resumes to extract key skills, experiences, and achievements.",
                },
                {
                    "role": "user",
                    "content": f"Analyze the following resume and extract key skills, experiences, and achievements:\n\n{resume_text}",
                },
            ],
        )
        # Extract the AI's response
        analyze_resume = response.choices[0].message["content"]
        result, created = Results.objects.update_or_create(
            user=user,
            defaults={
                "interview_questions": "N/A",  # Not applicable in this case
                "answer": "N/A",  # Not applicable in this case
                "analyzed_resume": analyze_resume,  # Store the analyzed resume in the database.
            },
        )
        return result
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def analyze_job_description(request):
    user = request.user
    results = Results.objects.filter(user=user).first()
    job_description = results.job_description
    try:
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
        # Be able to now either create or update the analyzed job description if its users first time or subsequent time
        result, created = Results.objects.update_or_create(
            user=user,
            defaults={
                "analyzed_job_description": analyzed_job_description,  # Store the analyzed job description in the db
            },
        )
        return result
    except Exception as e:
        # TODO USE LOGGING LATER WHEN I WANT TO PUSH TO PRODUCTION
        print(f"An error occurred: {str(e)}")
        return None


def generate_interview_questions(request):
    user = request.user
    results = Results.objects.filter(user=user).first()
    job_description = results.job_description
    analyzed_job_description = results.analyzed_job_description
    # use the job description to find interview questions
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that provides interview questions based on a job description.",
                },
                {
                    "role": "user",
                    "content": f"Analyze the following job description and provide Interview questions in respect to it:\n\n{job_description}",
                },
            ],
        )

        interview_questions = response.choices[0].message["content"]
        result, created = Results.objects.update_or_create(
            user=user,
            defaults={
                "analyzed_job_description": analyzed_job_description,
                "interview_questions": interview_questions,
            },
        )
        return result
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


# def get_results(user_id):
#     try:
#         user = CustomUser.objects.get(id=user_id)
#         job_description = user.job_description
#         resume_text = user.parsed_resume
#         background_info = user.background_info
#         achievements = user.achievement
#         yofe = user.year_of_experience
#         industry = user.industry_choice

#         prompt = (
#             f"You are an AI tasked with generating interview questions and answers based on the following details:\n"
#             f"\nJob Description: {job_description}"
#             f"\nYears of Experience: {yofe}"
#             f"\nIndustry: {industry}"
#             f"\n\nNow, generate between 5 and 10 interview questions that are relevant to the job description and industry."
#             f"\n\nAfter generating the questions, provide detailed and creative answers considering the following personal details:"
#             f"\nResume Text: {resume_text}"
#             f"\nBackground Info: {background_info}"
#             f"\nAchievements: {achievements}"
#         )

#         # using the OPEN AI model to generate
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are an AI tasked with generating interview questions and answers.",
#                 },
#                 {"role": "user", "content": prompt},
#             ],
#             max_tokens=500,
#             temperature=0.7,
#         )
#         completion_text = response["choices"][0]["message"]["content"]
#         # parsing the response
#         question, answer = parse_questions_and_answers(completion_text)
#         # save it to my results db
#         results = Results.objects.create(
#             interview_questions="\n".join(question),
#             answer="\n".join(answer),
#             user=user,
#         )
#         return results
#     except CustomUser.DoesNotExist:
#         return "User not found"
#     except Exception as e:
#         return f"An error occurred: {str(e)}"


# def parse_questions_and_answers(text):
#     questions = []
#     answers = []
#     current_question = None
#     current_answer = None

#     for line in text.splitlines():
#         line = line.strip()
#         if line.startswith("Q:") or line[0].isdigit():
#             if current_question:
#                 questions.append(current_question)
#                 answers.append(current_answer)
#             current_question = line
#             current_answer = ""
#         elif line.startswith("Answer:"):
#             current_answer = line
#         else:
#             if current_answer is not None:
#                 current_answer += " " + line

#     if current_question:
#         questions.append(current_question)
#         answers.append(current_answer)

#     return questions, answers


# use that Job description, Resume parsed and background info to get personalized answers
