from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from .views import AdminLoginView, healthz

urlpatterns = [
    path("admin/login/", AdminLoginView.as_view()),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/users/", include("users.urls", namespace="users")),
    path("api/healthz", healthz, name="healthz"),
]
