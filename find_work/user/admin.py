from .models import (
    User,
    Profile,
    UserAvatar,
)
from django.contrib import (
    admin,
)

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(UserAvatar)
