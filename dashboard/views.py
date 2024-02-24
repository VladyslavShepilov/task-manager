from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import (
    Employee,
    Task,
    Team,
    VisitCounter
)


def index(request: HttpRequest):
    num_employers = Employee.objects.count()
    num_teams = Team.objects.count()

    num_visits, created = VisitCounter.objects.get_or_create(pk=1)
    num_visits.total_visits += 1
    num_visits.save()
    context = {
        "num_employers": num_employers,
        "num_teams": num_teams,
        "num_visits": num_visits,
    }

    return render(request, "dashboard/index.html", context=context)


class TeamListView(LoginRequiredMixin, generic.ListView):
    pass


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    pass


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    pass


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    pass


class TaskListView(LoginRequiredMixin, generic.ListView):
    pass


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    pass
