from django.db.models import Count, Min, Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Employee, Task
from tasks.services import search_employee
from tasks.views import ImportantTasksViewSet
from users.models import User


class TaskTestCase(APITestCase):
    """Тестирование CRUD операций объекта Задача."""

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
        )

        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            name="Test task", description="Task for tests", period="2025-08-30T11:49:00Z", status="Open"
        )

        self.employee = Employee.objects.create(fullname="Test", position="Test")

    def test_create_task(self):
        """Тестирование создания объекта Задача."""
        data = {
            "name": "test create",
            "period": "2025-08-31T11:49:00Z",
            "executor": self.employee.id,
            "status": "To Do",
        }

        response = self.client.post("/tasks/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_no_auth(self):
        """Тестирование создания объекта Задача без авторизации."""
        self.client.logout()

        data = {
            "name": "test create",
            "period": "2025-08-31T11:49:00Z",
            "executor": self.employee.id,
            "status": "To Do",
        }

        response = self.client.post("/tasks/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_task(self):
        """Тестирование вывода всех объектов Задача."""
        Task.objects.all().delete()

        Task.objects.create(
            name="test list",
            period="2025-08-31T11:49:00Z",
            status="To Do",
        )

        response = self.client.get("/tasks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "test list")

    def test_list_task_no_auth(self):
        """Тестирование вывода всех объектов Задача без авторизации."""
        self.client.logout()
        Task.objects.all().delete()

        Task.objects.create(
            name="test list",
            period="2025-08-31T11:49:00Z",
            status="To Do",
        )

        response = self.client.get("/tasks/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task(self):
        """Тестирование обновления объекта Задача."""
        update_data = {"name": "test update"}

        response = self.client.patch(
            reverse("tasks:task-update", kwargs={"pk": self.task.id}),
            data=update_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "test update")

    def test_update_task_no_auth(self):
        """Тестирование обновления объекта Задача без авторизации."""
        self.client.logout()
        update_data = {"name": "test update"}

        response = self.client.patch(
            reverse("tasks:task-update", kwargs={"pk": self.task.id}),
            data=update_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.task.name, "Test task")

    def test_delete_task(self):
        """Тестирование удаления объекта Задача."""
        response = self.client.delete(
            reverse("tasks:task-delete", kwargs={"pk": self.task.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_no_auth(self):
        """Тестирование удаления объекта Задача без авторизации."""
        self.client.logout()
        response = self.client.delete(
            reverse("tasks:task-delete", kwargs={"pk": self.task.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.task.name, "Test task")


class EmployeeTestCase(APITestCase):
    """Тестирование CRUD операций объекта Сотрудник."""

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
        )
        self.client.force_authenticate(user=self.user)

        self.employee = Employee.objects.create(fullname="Test", position="Test")

    def test_create_employee(self):
        """Тестирование создания объекта Сотрудник."""
        data = {"fullname": "test create", "position": "test"}

        response = self.client.post("/employees/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_create_employee_no_auth(self):
        """Тестирование создания объекта Сотрудник без авторизации."""
        self.client.logout()

        data = {"fullname": "test create", "position": "test"}

        response = self.client.post("/employees/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_employee(self):
        """Тестирование вывода всех объектов Сотрудник."""
        Employee.objects.all().delete()

        Employee.objects.create(fullname="test list", position="-")

        response = self.client.get("/employees/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["fullname"], "test list")

    def test_list_employee_no_auth(self):
        """Тестирование вывода всех объектов Сотрудник без авторизации."""
        self.client.logout()
        Employee.objects.all().delete()

        Employee.objects.create(fullname="test list", position="-")

        response = self.client.get("/employees/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_employee(self):
        """Тестирование обновления объекта Сотрудник."""
        update_data = {"fullname": "test update"}

        response = self.client.patch(
            reverse("tasks:employee-update", kwargs={"pk": self.employee.id}),
            data=update_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.fullname, "test update")

    def test_update_employee_no_auth(self):
        """Тестирование обновления объекта Сотрудник без авторизации."""
        self.client.logout()
        update_data = {"fullname": "test update"}

        response = self.client.patch(
            reverse("tasks:employee-update", kwargs={"pk": self.employee.id}),
            data=update_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.employee.fullname, "Test")

    def test_delete_employee(self):
        """Тестирование удаления объекта Сотрудник."""
        response = self.client.delete(
            reverse("tasks:employee-delete", kwargs={"pk": self.employee.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_employee_no_auth(self):
        """Тестирование удаления объекта Сотрудник без авторизации."""
        self.client.logout()
        response = self.client.delete(
            reverse("tasks:employee-delete", kwargs={"pk": self.employee.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.employee.fullname, "Test")


class BusyEmployeesAPIViewTestCase(APITestCase):
    """Тестирование API занятости сотрудников."""

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
        )
        self.client.force_authenticate(user=self.user)

        #  Сотрудники
        self.employee1 = Employee.objects.create(fullname="Employee 1", position="Dev")
        self.employee2 = Employee.objects.create(fullname="Employee 2", position="Tester")
        self.employee3 = Employee.objects.create(fullname="Employee 3", position="Manager")

        # Задачи
        self.task1 = Task.objects.create(
            name="ToDo task", period="2025-08-30T11:49:00Z", status="To Do", executor=self.employee1
        )
        self.task2 = Task.objects.create(
            name="In progress task", period="2025-08-31T12:00:00Z", status="In Progress", executor=self.employee1
        )
        self.task3 = Task.objects.create(
            name="Closed task", period="2025-08-29T10:00:00Z", status="Closed", executor=self.employee2
        )
        self.task4 = Task.objects.create(
            name="ToDo task 2", period="2025-09-01T09:00:00Z", status="To Do", executor=self.employee3
        )

    def test_busy_employees_ordering(self):
        """Тестирование правильной сортировки сотрудников по убыванию активности."""

        response = self.client.get("/busy_employees/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        employees_data = response.data
        self.assertEqual(len(employees_data), 3)

        self.assertEqual(employees_data[0]["fullname"], "Employee 1")
        self.assertEqual(employees_data[0]["active_tasks_count"], 2)

        task_counts = [emp["active_tasks_count"] for emp in employees_data]
        self.assertIn(2, task_counts)
        self.assertIn(1, task_counts)
        self.assertIn(1, task_counts)

    def test_employee_without_tasks(self):
        """Тестирование сотрудника без задач."""

        Employee.objects.create(fullname="No tasks employee", position="newer")

        response = self.client.get("/busy_employees/")

        empty_employee_data = next((emp for emp in response.data if emp["fullname"] == "No tasks employee"), None)
        self.assertIsNotNone(empty_employee_data)
        self.assertEqual(empty_employee_data["active_tasks_count"], 0)

    def test_unauthenticated_access(self):
        """Тестирование доступа без аутентификации."""

        self.client.logout()
        response = self.client.get("/busy_employees/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_employees_with_same_task_count(self):
        """Тестирование когда у сотрудников одинаковое количество задач."""

        Task.objects.create(name="AddTask", period="2025-09-02T10:00:00Z", status="To Do", executor=self.employee3)

        response = self.client.get("/busy_employees/")

        task_counts = [emp["active_tasks_count"] for emp in response.data]
        self.assertEqual(task_counts.count(2), 2)
        self.assertEqual(task_counts.count(0), 1)


class ImportantTasksViewSetTestCase(APITestCase):
    """Тестирование ImportantTasksViewSet"""

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
        )
        self.client.force_authenticate(user=self.user)

        # Сотрудники
        self.employee1 = Employee.objects.create(fullname="Employee 1", position="Dev")
        self.employee2 = Employee.objects.create(fullname="Employee 2", position="Tester")

        # Родительские задачи
        self.parent_task_open = Task.objects.create(
            name="Parent Open Task", period="2025-08-30T11:49:00Z", status="Open", executor=self.employee1
        )
        self.parent_task_in_progress = Task.objects.create(
            name="Parent In Progress Task",
            period="2025-08-31T12:00:00Z",
            status="In Progress",
            executor=self.employee2,
        )
        self.parent_task_closed = Task.objects.create(
            name="Parent Closed Task", period="2025-08-29T10:00:00Z", status="Closed", executor=self.employee1
        )

        # Дочерние задачи
        self.child_task1 = Task.objects.create(
            name="Child task 1", period="2025-09-01T09:00:00Z", status="Open", parent_task=self.parent_task_in_progress
        )
        self.child_task2 = Task.objects.create(
            name="Child task 2", period="2025-09-02T10:00:00Z", status="Open", parent_task=self.parent_task_closed
        )
        self.child_task3 = Task.objects.create(
            name="Child task 3",
            period="2025-09-03T11:00:00Z",
            status="In Progress",
            parent_task=self.parent_task_in_progress,
        )
        self.child_task4 = Task.objects.create(
            name="Child task 4", period="2025-09-04T12:00:00Z", status="Open", parent_task=self.parent_task_open
        )

    def test_get_queryset_filters_correctly(self):
        """Тестирование правильной фильтрации важных задач."""
        viewset = ImportantTasksViewSet()
        queryset = viewset.get_queryset()

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().name, "Child task 1")

        task = queryset.first()
        self.assertEqual(task.status, "Open")
        self.assertIsNotNone(task.parent_task)
        self.assertNotEqual(task.parent_task.status, "Open")

    def test_no_important_tasks_found(self):
        """Тестирование случая, когда важные задачи не найдены."""

        Task.objects.filter(parent_task__isnull=False).delete()

        response = self.client.get("/important_tasks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Важные задачи не найдены")
        self.assertEqual(response.data["important_tasks"], [])


class SearchEmployeeTestCase(APITestCase):
    """Тестирование функции поиска сотрудника."""

    def setUp(self):
        #  Сотрудники
        self.employee1 = Employee.objects.create(fullname="Employee 1", position="Dev")
        self.employee2 = Employee.objects.create(fullname="Employee 2", position="Tester")
        self.employee3 = Employee.objects.create(fullname="Employee 3", position="Manager")

        # Родительские задачи
        self.parent_task1 = Task.objects.create(
            name="Parent task 1", period="2025-08-30T11:49:00Z", status="In Progress", executor=self.employee1
        )
        self.parent_task2 = Task.objects.create(
            name="Parent task 2", period="2025-08-31T12:00:00Z", status="In Progress", executor=self.employee2
        )

        # Важные задачи
        self.important_task1 = Task.objects.create(
            name="Important task 1", period="2025-09-01T09:00:00Z", status="Open", parent_task=self.parent_task1
        )
        self.important_task2 = Task.objects.create(
            name="Important task 2", period="2025-09-02T10:00:00Z", status="Open", parent_task=self.parent_task2
        )

    def test_search_worker_with_least_loaded_employee(self):
        """Тестирование выбора наименее загруженного сотрудника."""
        employees_stats = Employee.objects.annotate(
            active_tasks_count=Count("tasks", filter=~Q(tasks__status__in=["Closed"]))
        )

        min_tasks_count = employees_stats.aggregate(min_tasks=Min("active_tasks_count"))["min_tasks"] or 0

        important_tasks = Task.objects.filter(pk=self.important_task1.pk)

        result = search_employee(important_tasks, employees_stats, min_tasks_count)

        self.assertEqual(len(result), 1)
        # Должен выбрать employee3 (наименее загруженный), а не employee1 (исполнитель родительской)
        self.assertEqual(result[self.important_task1.id], "Employee 3")

    def test_search_worker_with_parent_executor_within_tolerance(self):
        """Тестирование выбора исполнителя родительской задачи в пределах допуска."""
        Task.objects.create(name="Add task 1", period="2025-09-03T11:00:00Z", status="To Do", executor=self.employee1)
        Task.objects.create(name="Add task 2", period="2025-09-04T12:00:00Z", status="To Do", executor=self.employee2)

        employees_stats = Employee.objects.annotate(
            active_tasks_count=Count("tasks", filter=~Q(tasks__status__in=["Closed"]))
        )

        min_tasks_count = employees_stats.aggregate(min_tasks=Min("active_tasks_count"))["min_tasks"] or 0

        important_tasks = Task.objects.filter(pk=self.important_task1.pk)

        result = search_employee(important_tasks, employees_stats, min_tasks_count)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[self.important_task1.id], "Employee 3")
