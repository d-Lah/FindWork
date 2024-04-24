from django.urls import path

from vacancy.api import (
    vacancy_info,
    delete_vacancy,
    create_vacancy,
    edit_vacancy_info,
)

app_name = "vacancy_api"

urlpatterns = [
    path(
        "create-vacancy",
        create_vacancy.CreateVacancy.as_view(),
        name="create_vacancy",
    ),
    path(
        "vacancy-info/<int:vacancy_id>",
        vacancy_info.VacancyInfo.as_view(),
        name="vacancy_info",
    ),
    path(
        "edit-vacancy-info/<int:vacancy_id>",
        edit_vacancy_info.EditVacancyInfo.as_view(),
        name="edit_vacancy_info",
    ),
    path(
        "delete-vacancy/<int:vacancy_id>",
        delete_vacancy.DeleteVacancy.as_view(),
        name="delete_vacancy"
    ),
]
