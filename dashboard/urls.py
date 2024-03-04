from django.urls import path

from .views import (
    index,
    EmployeeCreateView,
    EmployeeUpdateView,
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
    path("employee/edit/<int:pk>", EmployeeUpdateView.as_view(), name="employee-update"),
    path("employee/<int:pk>", EmployeeDetailView.as_view(), name="employee-detail"),
    path("employee/list", EmployeeListView.as_view(), name="employee-list"),
    path("team/list", TeamListView.as_view(), name="team-list"),
    path("team/<int:pk>", TeamDetailView.as_view(), name="team-detail"),
    path("task/list-assigned/<str:assigned>", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
]
