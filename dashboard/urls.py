from django.urls import path

from .views import (
    index,
    toggle_assign_to_team,
    toggle_assign_to_task,
    toggle_mark_done_task,
    EmployeeCreateView,
    EmployeeDetailView,
    EmployeeListView,
    TaskDetailView,
    TaskListView,
    TeamDetailView,
    TeamListView,
)

app_name = "dashboard"

urlpatterns = [
    path("", index, name="index"),
    path("employee/<int:pk>", EmployeeDetailView.as_view(), name="employee-detail"),
    path("employee/list", EmployeeListView.as_view(), name="employee-list"),
    path("team/list", TeamListView.as_view(), name="team-list"),
    path("team/<int:pk>", TeamDetailView.as_view(), name="team-detail"),
    path("team/<int:pk>/team-assign", toggle_assign_to_team, name="toggle-team-assign"),
    path("task/list-assigned/<str:assigned>", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("team/<int:pk>/task-assign", toggle_assign_to_task, name="toggle-task-assign"),
    path("task/<int:pk>/task-done", toggle_mark_done_task, name="toggle-task-done"),
]
