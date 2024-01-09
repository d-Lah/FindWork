from .models import (
    User,
    Profile,
    UserAvatar,
    EmployerProfile,
    EmployeeProfile,
    EmployeeSpecialization,
)
from django.contrib import (
    admin,
)

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(UserAvatar)
admin.site.register(EmployerProfile)
admin.site.register(EmployeeProfile)
admin.site.register(EmployeeSpecialization)
