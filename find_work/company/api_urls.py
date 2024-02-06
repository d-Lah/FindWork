from django.urls import path

from company.api import (
    company_info,
    create_company,
    edit_company_info,
    upload_company_avatar,
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
    path(
        "edit-company-info",
        edit_company_info.EditCompanyInfo.as_view(),
        name="edit_company_info"
    ),
    path(
        "upload-company-avatar",
        upload_company_avatar.UploadCompanyAvatar.as_view(),
        name="upload_company_avatar"
    ),
]
