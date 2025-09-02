from django.db.models import Count, Min, Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employee, Task
from .serializers import CreateTaskSerializer, EmployeeSerializer, ImportantTaskSerializer, TaskSerializer
from .services import search_employee


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet для задачи."""

    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTaskSerializer
        else:
            return TaskSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        task = serializer.save()
        if task.executor:
            task.status = "To Do"
        else:
            task.status = "Open"

        task.save()

    def perform_create(self, serializer):
        task = serializer.save()
        if task.executor:
            task.status = "To Do"
        else:
            task.status = "Open"

        task.save()


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для сотрудника."""

    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class BusyEmployeesAPIView(APIView):
    """Представление для занятых сотрудников"""

    def get(self, request):
        employees = Employee.objects.annotate(
            active_tasks_count=Count("tasks", filter=~Q(tasks__status="Closed"))
        ).order_by("-active_tasks_count")

        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class ImportantTasksViewSet(viewsets.ModelViewSet):
    """Viewset для важных задач."""

    serializer_class = ImportantTaskSerializer

    def get_queryset(self):
        return Task.objects.filter(status="Open", parent_task__isnull=False, parent_task__status="In Progress")

    def list(self, request, *args, **kwargs):
        important_tasks = self.get_queryset()

        if not important_tasks.exists():
            return Response({"message": "Важные задачи не найдены", "important_tasks": []})

        # Информация о сотруднике
        employees_stats = Employee.objects.annotate(
            active_tasks_count=Count("tasks", filter=~Q(tasks__status__in=["Closed"]))
        )

        # Вычисление минимального количества задач у сотрудника
        min_tasks_count = employees_stats.aggregate(
            min_tasks=Min("active_tasks_count", filter=~Q(tasks__status__in=["Closed"]))
        )["min_tasks"]

        recommended_employees = search_employee(important_tasks, employees_stats, min_tasks_count)

        serializer = self.get_serializer(
            important_tasks, many=True, context={"recommended_employees": recommended_employees}
        )

        return Response(serializer.data)
