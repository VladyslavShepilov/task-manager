from django.urls import path

from .views import (
    index,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDetailView,
    TeamDetailView,

)

app_name = "dashboard"

urlpatterns = [
    path("", index, name="index"),
    path("employee/<int:pk>", EmployeeDetailView.as_view(), name="employee-detail"),
    path("employee/edit/<int:pk>", EmployeeUpdateView.as_view() ,name="employee-update"),
    path("team/<int:pk>", TeamDetailView.as_view(), name="team-detail"),

]
