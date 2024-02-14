from django.db import models
from django.contrib.auth.models import AbstractUser


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
        null=True
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

    class Meta:
        ordering = ["-priority"]


class Team(models.Model):
    name = models.CharField(max_length=20)
