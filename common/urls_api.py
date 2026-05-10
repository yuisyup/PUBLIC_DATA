from django.urls import path

from common.views.api.health import health_check
from common.views.api.input_definition import input_definition_choices

app_name = "common_api"

urlpatterns = [
    path("health/", health_check, name="health"),
    path("input-definitions/", input_definition_choices, name="input_definitions"),
]