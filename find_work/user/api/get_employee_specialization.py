from rest_framework import generics

from user.models import EmployeeSpecialization
from user.serializer import EmployeeSpecializationSerializer


class GetEmployeeSpecialization(generics.ListAPIView):
    queryset = EmployeeSpecialization.objects.all()
    serializer_class = EmployeeSpecializationSerializer
