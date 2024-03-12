from django.urls import path

from vacancy.api import (
    create_vacancy,
    vacancy_info,
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
]
