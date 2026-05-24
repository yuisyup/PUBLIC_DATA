from django.urls import path

from common.views.api.health import health_check
from common.views.api.input_definition import (
    input_definition_choices,
    input_definition_types,
)
from common.views.api.register.register_csv_api import RegisterCsvApiView

app_name = "common_api"

urlpatterns = [
    path("health/", health_check, name="health"),
    path("input-types/", input_definition_types, name="input_types"),
    path("input-definitions/", input_definition_choices, name="input_definitions"),
    path("bulk-register/", RegisterCsvApiView.as_view(), name="bulk_register"),
]
