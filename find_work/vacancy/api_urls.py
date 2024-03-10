from django.urls import path

from vacancy.api import (
    create_vacancy
)

app_name = "vacancy_api"

urlpatterns = [
    path(
        "create-vacancy",
        create_vacancy.CreateVacancy.as_view(),
        name="create_vacancy",
    ),
]
