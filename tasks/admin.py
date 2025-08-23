from django.contrib import admin

from tasks.models import Employee, Task


@admin.register(Employee)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "position")
    list_filter = ("fullname",)
    search_fields = ("fullname", "position")


@admin.register(Task)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "parent_task", "executor", "period", "status")
    list_filter = ("name", "executor", "status")
    search_fields = ("name", "executor", "status")
