from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, EmployeeCreateForm, SearchForm
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


@login_required
def toggle_assign_to_team(request, pk):
    employee = Employee.objects.get(id=request.user.id)
    team = get_object_or_404(Team, id=pk)

    if employee.team == team:
        employee.team = None
    else:
        employee.team = team
    employee.save()

    return HttpResponseRedirect(reverse_lazy("dashboard:team-detail", args=[pk]))


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
        username = self.request.GET.get("search_key")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("search_key", "")
        context["search_form"] = SearchForm(
            initial={"search_key": username}
        )
        return context


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee
    context_object_name = "employee"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = self.object.tasks_assigned.all()

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
    model = Team
    context_object_name = "team_list"
    paginate_by = 10

    def get_queryset(self):
        search_key = self.request.GET.get("search_key", "")
        if search_key:
            return Team.objects.filter(name__icontains=search_key)
        return Team.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_key = self.request.GET.get("search_key", "")
        context["search_form"] = SearchForm(
            initial={"search_key": search_key}
        )
        return context


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employees = self.object.members.all().order_by("role")

        paginator = Paginator(employees, self.paginate_by)
        page = self.request.GET.get("page")

        try:
            employees = paginator.page(page)
        except PageNotAnInteger:
            employees = paginator.page(1)
        except EmptyPage:
            employees = paginator.page(paginator.num_pages)

        context["employee_pagination"] = employees
        print(context["employee_pagination"])
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 15

    def get_queryset(self):
        assigned = bool(self.request.GET.get("assigned"))
        if assigned:
            return Task.objects.filter(assigned_to__isnull=True)
        return Task.objects.filter(
            assigned_to__isnull=False,
            is_completed=False
        )


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

