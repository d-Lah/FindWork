from .models import (
    User,
    Profile,
    UserAvatar,
    EmployerProfile,
    EmployeeProfile,
)
from django.contrib import (
    admin,
)

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(UserAvatar)
admin.site.register(EmployerProfile)
admin.site.register(EmployeeProfile)
