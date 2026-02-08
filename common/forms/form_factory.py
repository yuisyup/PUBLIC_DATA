from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Type

from django import forms

from common.exceptions.app_error import FeatureKeyFormNotFoundError
from common.forms.register.register_csv_form import RegisterCsvForm


class FormFactory:
    """
    画面/機能キー -> Formクラス を解決する共通Factory
    """

    # 画面側で "feature_key" を固定で持つ
    _map: Dict[str, Type[forms.Form]] = {
        # ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ 登録系 ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
        
        # CSV登録画面
        "register_csv": RegisterCsvForm,
        
        # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ 登録系 ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
    }

    @classmethod
    def get_form_class(
        cls,
        feature_key: str
    ) -> Type[forms.Form]:
        """
        feature_key から Formクラスを取得する
        
        :param cls: クラスメソッド
        :param feature_key: 画面/機能キー
        :type feature_key: str
        :return: FORMクラス
        :rtype: type[Form]
        """
        try:
            return cls._map[feature_key]
        except KeyError as e:
            raise FeatureKeyFormNotFoundError(f"Form定義が見つかりません feature_key={feature_key}") from e
