from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.utils import timezone


class Employee(AbstractUser):

    class Role(models.TextChoices):
        DEV = "dev", "Developer"
        PM = "pm", "Project Manager"
        QA = "qa", "QA"
        DESIGNER = "designer", "Designer"
        DEVOPS = "devops", "DevOps"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
    )
    date_joined = models.DateField(
        auto_now_add=True
    )
    team = models.ForeignKey("Team", related_name="members", null=True, on_delete=models.SET_NULL)


class Task(models.Model):
    class Type(models.TextChoices):
        BUG = "bug", "Bug"
        NEW_FEATURE = "new_feature", "New feature"
        CHANGE = "change", "Change"
        REFACTOR = "refactor", "Refactor"
        QA = "qa", "QA"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    name = models.CharField(
        max_length=50,
        null=False,
    )
    description = models.TextField(
        max_length=500,
        blank=True,
    )
    type = models.CharField(
        max_length=20,
        choices=Type.choices
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices
    )
    story_points = models.IntegerField(

    )
    deadline = models.DateTimeField(
        blank=True,
    )
    is_completed = models.BooleanField(

    )
    assigned_to = models.ManyToManyField(
        Employee,
        related_name="tasks_assigned",
        blank=True
    )
    created_at = models.DateField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-priority"]


class Team(models.Model):
    name = models.CharField(max_length=20)
    productivity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def calculate_productivity(self):
        today = timezone.datetime.today()
        start_of_month = today.replace(day=1)
        tasks_this_month = Task.objects.filter(
            assigned_to__team=self,
            created_at__gte=start_of_month,
            created_at__lt=today
        )
        total_story_points = tasks_this_month.aggregate(story_point=Sum("story_points"))
        self.productivity = total_story_points if total_story_points is not None else 0
        self.save()


class VisitCounter(models.Model):
    total_visits = models.IntegerField(default=0)
