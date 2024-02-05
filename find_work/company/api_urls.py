from django.urls import path

from company.api import (
    company_info,
    create_company,
)

app_name = "company_api"

urlpatterns = [
    path(
        "create-company",
        create_company.CreateCompany.as_view(),
        name="create_company"
    ),
    path(
        "company-info/<int:company_id>",
        company_info.CompanyInfo.as_view(),
        name="company_info"
    ),
]
