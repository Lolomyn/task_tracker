from django.db import models


class Employee(models.Model):
    fullname = models.CharField(
        max_length=255, help_text="Укажите полное имя сотрудника", verbose_name="Полное имя сотрудника"
    )

    position = models.CharField(
        max_length=255, help_text="Укажите должность сотрудника", verbose_name="Должность сотрудника"
    )

    def __str__(self):
        return f"{self.fullname} ({self.position})"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["fullname"]


class Task(models.Model):
    name = models.CharField(
        max_length=255, help_text="Укажите наименование задачи", verbose_name="Наименование задачи"
    )

    description = models.TextField(
        blank=True, null=True, help_text="Укажите подробности задачи", verbose_name="Описание задачи"
    )

    parent_task = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="related_tasks",
        help_text="Укажите родительскую задачу",
        verbose_name="Родительская задача",
    )

    executor = models.ForeignKey(
        Employee,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Выберите исполнителя задачи",
        verbose_name="Исполнитель задачи",
        related_name="tasks",
    )

    period = models.DateTimeField(help_text="Укажите срок выполнения задачи", verbose_name="Срок выполнения задачи")

    STATUS_CHOICES = [
        ("Open", "open"),
        ("To Do", "to do"),
        ("In Progress", "in progress"),
        ("Done", "done"),
        ("Reopened", "reopened"),
        ("Closed", "closed"),
    ]

    status = models.CharField(
        choices=STATUS_CHOICES, default="Open", help_text="Выберите статус задачи", verbose_name="Статус задачи"
    )

    def __str__(self):
        return f"{self.name} ({self.status}) [{self.executor}]"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["name", "executor", "status"]
