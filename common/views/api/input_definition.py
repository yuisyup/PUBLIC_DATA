from typing import *
from django.http import HttpRequest, HttpResponse

from django.http import JsonResponse
from common.services.infra.persistance.repositories.input_definition_repository import (
    InputDefinitionRepository,
)


def input_definition_choices(request: HttpRequest):
    input_type = request.GET.get("input_type")

    if not input_type:
        return JsonResponse(
            {"error": "input_type is required."},
            status=400,
        )

    repository = InputDefinitionRepository()
    choices: List[tuple[int, str]] = repository.get_input_def_choices_by_type(
        lookup={"input_type": input_type}
    )

    data = [
        {
            "id": choice_id,
            "displayName": choice_name,
        }
        for choice_id, choice_name in choices
    ]

    return JsonResponse({"results": data})