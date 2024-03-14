from django.urls import path

from .views import (
    index,
    toggle_assign_to_team,
    EmployeeCreateView,
    EmployeeDetailView,
    EmployeeListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListView,
    TeamDetailView,
    TeamListView,
)

app_name = "dashboard"

urlpatterns = [
    path("", index, name="index/"),
    path("employee/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("employee/list/", EmployeeListView.as_view(), name="employee-list"),
    path("team/list/", TeamListView.as_view(), name="team-list"),
    path("team/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("team/<int:pk>/team-assign/", toggle_assign_to_team, name="toggle-team-assign"),
    path("task/list-assigned/<str:assigned>/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]
