from django.urls import path

from common.views.api.health import health_check
from common.views.api.input_definition import (
    input_definition_choices,
    input_definition_types,
)
from common.views.api.register.bulk_register_api import bulk_register
from common.views.api.run_result_reference.run_result_reference_api import (
    run_result_reference,
    run_result_reference_detail,
)

app_name = "common_api"

urlpatterns = [
    path("health/", health_check, name="health"),
    path("input-types/", input_definition_types, name="input_types"),
    path("input-definitions/", input_definition_choices, name="input_definitions"),
    path("bulk-register/", bulk_register, name="bulk_register"),
    path(
        "run-result-reference/",
        run_result_reference,
        name="run_result_reference",
    ),
    path(
        "run-result-reference/detail/<uuid:run_id>/",
        run_result_reference_detail,
        name="run_result_reference_detail",
    ),
]
