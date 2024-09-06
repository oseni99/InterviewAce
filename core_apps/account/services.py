import os
from django.core.exceptions import ValidationError


def validate_file(file):
    allowed_extensions = [".pdf", ".docx", ".doc"]
    ext = os.path.splitext(file.name)[1].lower()  # Get the file extension
    if ext not in allowed_extensions:
        raise ValidationError(
            f"Invalid file extension. Only {', '.join(allowed_extensions)} are allowed."
        )

    max_file_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_file_size:
        raise ValidationError("File size exceeds the maximum allowed size of 5MB.")

    return True


# Validate the LinkedIn profile Bio
def validate_linkedin_profile(profile):
    # Check if the URL starts with either of the valid LinkedIn URL patterns
    if not (
        profile.startswith("https://www.linkedin.com/in/")
        or profile.startswith("https://linkedin.com/in/")
    ):
        raise ValidationError(
            "Invalid LinkedIn profile URL. Ensure it starts with 'https://www.linkedin.com/in/'."
        )

    return True
