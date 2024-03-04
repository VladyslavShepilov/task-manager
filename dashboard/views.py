from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, EmployeeCreateForm, EmployeeSearchForm
from django.contrib.auth.views import LoginView, LogoutView


from .models import (
    Employee,
    Task,
    Team,
    VisitCounter
)


@login_required
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


class EmployeeLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("dashboard:index")


class EmployeeCreateView(generic.CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("dashboard:index")


class EmployeeUpdateView(generic.CreateView):
    pass


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    context_object_name = "employee_list"
    paginate_by = 5

    def get_queryset(self):
        queryset = Employee.objects.select_related("team")
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = EmployeeSearchForm(
            initial={"username": username}
        )
        return context


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee
    context_object_name = "employee"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = self.object.tasks_assigned.all()
        print(tasks)

        paginator = Paginator(tasks, self.paginate_by)
        page = self.request.GET.get("page")

        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        context["task_pagination"] = tasks
        return context


class TeamListView(LoginRequiredMixin, generic.ListView):
    pass


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team


class TaskListView(LoginRequiredMixin, generic.ListView):
    pass


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    pass
