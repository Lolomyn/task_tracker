from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task, Employee

from .serializers import EmployeeSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet для задачи."""

    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    queryset = Task.objects.all()


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для сотрудника."""

    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]
    queryset = Employee.objects.all()
