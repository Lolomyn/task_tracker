def search_worker(important_tasks, employees_stats, min_tasks_count):
    """Функция для поиска рекомендованного на задачу сотрудника."""
    recommended_employees = {}

    for task in important_tasks:
        suitable_employees = []

        # Проверяем сотрудников на критерии отбора кандидата
        for employee in employees_stats:
            # Наименее загруженный сотрудник
            is_least_loaded = employee.active_tasks_count == min_tasks_count

            # Сотрудник родительской задачи с менее +2 задачи от наименее загруженного
            is_parent_with_tolerance = False
            if task.parent_task and task.parent_task.executor:
                is_parent_with_tolerance = (
                    employee == task.parent_task.executor and employee.active_tasks_count <= min_tasks_count + 2
                )

            # Если сотрудник подходит по одному из критериев
            if is_least_loaded or is_parent_with_tolerance:
                # Выставляем приоритет выбора
                # 1 - наименее загруженный
                # 2 - исполнитель родительской задачи

                priority = 0
                if is_least_loaded:
                    priority = 1  # Высший приоритет
                elif is_parent_with_tolerance:
                    priority = 2

                suitable_employees.append(
                    {"employee": employee, "priority": priority, "tasks_count": employee.active_tasks_count}
                )

                if suitable_employees:
                    # Сортируем по приоритету
                    suitable_employees.sort(key=lambda x: (x["priority"], x["tasks_count"]))
                    # Берем первого в отсортированном списке
                    best_employee = suitable_employees[0]["employee"]
                    recommended_employees[task.id] = best_employee.fullname
                else:
                    recommended_employees[task.id] = "Не назначен"

    return recommended_employees
