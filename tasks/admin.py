from django.contrib import admin

from tasks.models import Employee, Task


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "position")
    list_filter = ("fullname",)
    search_fields = ("fullname", "position")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "parent_task", "executor", "period", "status")
    list_filter = ("name", "executor", "status")
    search_fields = ("name", "executor", "status")
