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
        blank=False
    )
    date_joined = models.DateField(
        auto_now_add=True
    )
