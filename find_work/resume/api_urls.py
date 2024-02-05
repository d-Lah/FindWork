from django.urls import path

from resume.api import (
    resume_info,
    create_resume,
    delete_resume,
    edit_resume_info,
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
    path(
        "edit-resume-info",
        edit_resume_info.EditResumeInfo.as_view(),
        name="edit_resume_info"
    ),
    path(
        "delete-resume",
        delete_resume.DeleteResume.as_view(),
        name="delete_resume"
    )
]
