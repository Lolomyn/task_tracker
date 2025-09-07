def search_employee(important_tasks, employees_stats, min_tasks_count):
    """Функция для поиска рекомендованного на задачу сотрудника."""
    recommended_employees = {}

    for task in important_tasks:
        suitable_employees = []

        for employee in employees_stats:
            is_least_loaded = employee.active_tasks_count == min_tasks_count

            is_parent_with_tolerance = False
            if task.parent_task and task.parent_task.executor:
                is_parent_with_tolerance = (
                    employee == task.parent_task.executor and employee.active_tasks_count <= min_tasks_count + 2
                )

            if is_least_loaded or is_parent_with_tolerance:

                if is_least_loaded:
                    priority = 1
                else:
                    priority = 2

                suitable_employees.append(
                    {"employee": employee, "priority": priority, "tasks_count": employee.active_tasks_count}
                )

        if suitable_employees:
            suitable_employees.sort(key=lambda x: (x["priority"], x["tasks_count"]))
            best_employee = suitable_employees[0]["employee"]
            recommended_employees[task.id] = best_employee.fullname
        else:
            recommended_employees[task.id] = "Не назначен"

    return recommended_employees
