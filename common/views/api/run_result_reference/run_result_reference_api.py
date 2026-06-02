from django.http import HttpRequest, JsonResponse

from common.services.api.api_response import ApiResponse
from common.services.api.run_result_reference.run_result_reference_api_handler import (
    RunResultReferenceApiHandler,
)


def run_result_reference(request: HttpRequest) -> JsonResponse:
    response: ApiResponse = RunResultReferenceApiHandler().handle(request)
    return JsonResponse(response.body, status=response.status_code)
