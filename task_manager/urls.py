from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from dashboard.views import EmployeeCreateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/register", EmployeeCreateView.as_view(), name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("dashboard.urls", namespace="dashboard")),
    path("__debug__/", include("debug_toolbar.urls")),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
