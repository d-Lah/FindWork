from rest_framework.serializers import ValidationError


class FieldExistsValidator:
    message = "This field not exists."

    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, value):
        queryset = self.queryset
        filter_kwargs = {"pk": value}

        if not queryset.filter(**filter_kwargs):
            queryset = queryset.none()
        if not queryset.exists():
            raise ValidationError(self.message)
