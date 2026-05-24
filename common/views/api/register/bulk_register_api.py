from dataclasses import dataclass
from typing import *
from copy import deepcopy
import traceback
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views import View
from django.http import HttpRequest, JsonResponse

from common.services.api.register.bulk_register_api_handler import (
    BulkRegisterApiHandler,
)
from common.services.api.register.api_response import ApiResponse


@csrf_exempt
def bulk_register(request: HttpRequest) -> JsonResponse:

    # データ登録ハンドラ起動
    response: ApiResponse = BulkRegisterApiHandler().handle(request)

    # JSONレスポンス返却
    return JsonResponse(response.body, status=response.status_code)
