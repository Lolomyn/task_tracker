from rest_framework import serializers

from .models import Employee, Task


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор задачи"""

    class Meta:
        model = Task
        fields = "__all__"


class ImportantTaskSerializer(serializers.ModelSerializer):
    """Сериализатор важной задачи"""

    executor_name = serializers.SerializerMethodField()

    def get_executor_name(self, obj):
        recommended_employees = self.context.get("recommended_employees", {})
        return recommended_employees.get(obj.id, "Не назначен")

    class Meta:
        model = Task
        fields = ["name", "period", "executor_name"]


class CreateTaskSerializer(serializers.ModelSerializer):
    """Сериализатор создания задачи"""

    class Meta:
        model = Task
        fields = ["id", "name", "description", "parent_task", "executor", "period"]


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор сотрудника"""

    tasks = TaskSerializer(read_only=True, many=True)
    active_tasks_count = serializers.SerializerMethodField()

    def get_active_tasks_count(self, obj):
        return obj.tasks.exclude(status="Closed").count()

    class Meta:
        model = Employee
        fields = ["id", "fullname", "position", "active_tasks_count", "tasks"]
