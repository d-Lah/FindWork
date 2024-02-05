from django.urls import path

from company.api import (
    create_company
)

app_name = "company_api"

urlpatterns = [
    path(
        "create-company",
        create_company.CreateCompany.as_view(),
        name="create_company"
    )
]
