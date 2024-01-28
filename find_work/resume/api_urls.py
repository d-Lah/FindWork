from django.urls import path

# from resume.api.create_resume import CreateResume
from resume.api import (
    resume_info,
    create_resume,
)

app_name = "resume_api"

urlpatterns = [
    path(
        "create-resume",
        create_resume.CreateResume.as_view(),
        name="create_resume"
    ),
    path(
        "resume-info/<int:resume_id>",
        resume_info.ResumeInfo.as_view(),
        name="resume_info"
    ),
]
