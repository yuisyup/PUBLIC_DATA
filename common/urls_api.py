from django.urls import path

from common.views.api.health import health_check

app_name = "common_api"

urlpatterns = [
    path("health/", health_check, name="health"),
]