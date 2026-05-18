from dataclasses import dataclass
from typing import *
from copy import deepcopy
import traceback

from django.views import View
from django.http import HttpRequest, JsonResponse

from common.services.api.register.register_csv_api_handler import RegisterCsvApiHandler
from common.services.api.register.api_response import ApiResponse


class RegisterCsvApiView(View):

    def post(self, request: HttpRequest) -> JsonResponse:

        # データ登録ハンドラ起動
        response: ApiResponse = RegisterCsvApiHandler().handle(request)

        # JSONレスポンス返却
        return JsonResponse(response.body, status=response.status_code)
