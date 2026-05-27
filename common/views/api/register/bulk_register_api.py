from typing import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse

from common.services.api.register.bulk_register_api_handler import (
    BulkRegisterApiHandler,
)
from common.services.api.api_response import ApiResponse


@csrf_exempt
def bulk_register(request: HttpRequest) -> JsonResponse:

    # データ登録ハンドラ起動
    response: ApiResponse = BulkRegisterApiHandler().handle(request)

    # JSONレスポンス返却
    return JsonResponse(response.body, status=response.status_code)
