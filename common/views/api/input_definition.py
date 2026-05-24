from typing import *
from django.http import HttpRequest, JsonResponse

from common.services.infra.persistance.repositories.input_definition_repository import (
    InputDefinitionRepository,
)


def input_definition_choices(request: HttpRequest):
    """
    入力データ定義を種別を条件として取得する。

    :param request: リクエストパラメータ（input_type: 入力データ種別）
    :type request: HttpRequest
    :return: 選択肢リスト（CODE, 名前）
    :rtype: JsonResponse
    """

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

    print(data)

    return JsonResponse({"results": data})


def input_definition_types(request: HttpRequest):
    """
    入力データ種別を全件取得する。

    :param request: リクエストパラメータ（input_type: 入力データ種別）
    :type request: HttpRequest
    :return: 選択肢リスト（CODE, 名前）
    :rtype: JsonResponse
    """

    repository = InputDefinitionRepository()
    choices: List[tuple[int, str]] = repository.get_input_def_types_all()

    data = [
        {
            "code": type_code,
            "displayName": type_name,
        }
        for type_code, type_name in choices
    ]

    print(data)

    return JsonResponse({"results": data})
