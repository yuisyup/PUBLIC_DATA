# common/views/register/mixins.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type

from django import forms
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from common.issue.models import Issue
from common.issue.run_result_dto import RunResult
from common.services.infra.persistance.repositories.input_definition_repository import InputDefinitionRepository
from common.views.base_view import BaseView


class RegisterViewMixin(BaseView):
    """
    登録系Viewの共通Mixin
    """

    # --- 共通関数 ---
    def get_input_def_choices(
        self,
        lookup: Dict[str, Any]
    ) -> List[tuple[int, str]]:
        """
        検索条件に従い、入力データ定義の選択肢リストを取得する。
        
        :param lookup: 検索条件（カラム名, 値）
        :type lookup: Dict[str, Any]
        :return: 選択肢リスト（id, 名前）
        :rtype: List[tuple[int, str]]
        """

        choices: List[tuple[int, str]] = InputDefinitionRepository().get_input_def_choices_by_type(lookup)
        return choices

    def add_status_message(
        self, 
        request: HttpRequest, 
        result: RunResult,
        run_id: str = None
    ) -> None:
        """
        登録/更新処理の結果に応じたステータス（Django）メッセージを追加する。
        
        :param request: リクエスト
        :type request: HttpRequest
        :param result: 実行結果
        :type result: RunResult
        :param run_id: 実行ID
        :type result: str
        """
        if result.status == "SUCCESS":
            messages.success(request, "登録が完了しました。" + run_id)
        elif result.status == "SUCCESS_WITH_WARN":
            messages.warning(request, "登録は完了しましたが、警告発生行があります。" + run_id)
        else:
            messages.error(request, "登録に失敗しました。" + run_id)
            
    # --- override前提フック ---
    def run_register_usecase(
        self,
        *,
        cleaned_data: Dict[str, Any]
    )-> List[Issue]:
        """
        登録/更新基幹モジュールによる入力データの登録処理を実行する。
        
        cleaned_data:
            - input_def_id：入力データ定義ID
            - input_source：入力データ
            - （その他、実装機能の必要に応じて引数格納）
        実行処理:
            1) DataFrame化
            2) 前処理（処理実行日付与、データクレンジングなど）
            3) Register基幹モジュールFactory呼び出し
            4) Issue/RunResult永続化
            5) List[Issue]返却
        """
        raise NotImplementedError

