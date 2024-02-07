from django.contrib import admin

from resume.models import (
    Skill,
    Resume,
    Specialization,
    WorkExperience,
    TypeOfEmployment
)

admin.site.register(Skill)
admin.site.register(Resume)
admin.site.register(Specialization)
admin.site.register(WorkExperience)
admin.site.register(TypeOfEmployment)
