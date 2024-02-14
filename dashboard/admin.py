from django.contrib import admin

from dashboard.models import (
    Employee,
    Team,
    Task
)

admin.site.register(Employee)
admin.site.register(Team)
admin.site.register(Task)
