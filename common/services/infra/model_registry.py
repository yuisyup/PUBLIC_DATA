from __future__ import annotations

from dataclasses import dataclass
from typing import *

from django.apps import apps
from django.db import models

from common.exceptions.app_error import ModelRegistryError


@dataclass(frozen=True)
class ModelRegistry:
    """
    Djangoのモデル解決（apps.get_model）をinfraに隔離するためのレジストリ。

    - Processor / Domain が django.apps に直接依存しないための薄いラッパー。
    - "app_label.ModelName" 形式のラベルを受け取る想定。
    """

    def resolve(self, model_label: str) -> Optional[Type[models.Model]]:
        """
        モデルラベルから Django Model クラスを解決する。<br>
        見つからない場合独自例外を返す。<br>
        ※contextへのModel情報格納は呼び出し元で行う。

        :param model_label: apps.Model
        :type model_label: str
        :return: Modelクラス（解決失敗の場合None）
        :rtype: type[Model] | None
        :raises ModelRegistryError: モデルクラス解決失敗
        """

        try:
            model_class = apps.get_model(*model_label.split("."))
        except (LookupError, ValueError):
            raise ModelRegistryError()

        return model_class
