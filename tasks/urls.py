from django.urls import path

from tasks.apps import TasksConfig

from .views import BusyEmployeesAPIView, EmployeeViewSet, ImportantTasksViewSet, TaskViewSet

app_name = TasksConfig.name

urlpatterns = [
    # Задачи
    path("tasks/create/", TaskViewSet.as_view({"post": "create"}), name="task-create"),
    path("tasks/", TaskViewSet.as_view({"get": "list"}), name="task-list"),
    path("tasks/<int:pk>/", TaskViewSet.as_view({"get": "retrieve"}), name="task-list"),
    path("tasks/<int:pk>/update/", TaskViewSet.as_view({"put": "update", "patch": "update"}), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskViewSet.as_view({"delete": "destroy"}), name="task-delete"),
    path("important_tasks/", ImportantTasksViewSet.as_view({"get": "list"}), name="important-task"),
    # Сотрудники
    path("employees/create/", EmployeeViewSet.as_view({"post": "create"}), name="employee-create"),
    path("employees/", EmployeeViewSet.as_view({"get": "list"}), name="employee-list"),
    path("employees/<int:pk>/", EmployeeViewSet.as_view({"get": "retrieve"}), name="employee-list"),
    path(
        "employees/<int:pk>/update/",
        EmployeeViewSet.as_view({"put": "update", "patch": "update"}),
        name="employee-update",
    ),
    path("employees/<int:pk>/delete/", EmployeeViewSet.as_view({"delete": "destroy"}), name="employee-delete"),
    path("busy_employees/", BusyEmployeesAPIView.as_view(), name="busy-employee-list"),
]
