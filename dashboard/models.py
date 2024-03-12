import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, F
from django.utils import timezone


class Employee(AbstractUser):

    class Role(models.TextChoices):
        DEV = "Developer", "dev"
        PM = "Project Manager", "pm",
        QA = "QA", "qa"
        DESIGNER = "Designer", "designer"
        DEVOPS = "DevOps", "devops"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
    )
    date_joined = models.DateField(
        auto_now_add=True
    )
    team = models.ForeignKey("Team", related_name="members", null=True, blank=True, on_delete=models.SET_NULL)


class Task(models.Model):
    class Type(models.TextChoices):
        BUG = "bug", "Bug"
        NEW_FEATURE = "New feature", "new_feature"
        CHANGE = "Change", "change"
        REFACTOR = "Refactor", "refactor"
        QA = "QA", "qa"

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

    def __str__(self):
        return str(self.name)


class Team(models.Model):
    name = models.CharField(max_length=20)
    productivity = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-productivity"]

    def calculate_productivity(self):
        tasks_done = Task.objects.filter(
            assigned_to__in=self.members.all(),
            is_completed=True
        )
        total_story_points = tasks_done.aggregate(story_point=Sum("story_points"))
        productivity = total_story_points["story_point"] if total_story_points is not None else 0
        self.productivity = productivity
        self.save()
        return productivity

    def __str__(self):
        return str(self.name)


class VisitCounter(models.Model):
    total_visits = models.IntegerField(default=0)
