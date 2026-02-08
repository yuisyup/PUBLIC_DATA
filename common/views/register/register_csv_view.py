# common/views/register/base.py
from __future__ import annotations

from dataclasses import dataclass
from typing import *
from copy import deepcopy
import traceback

from django import forms
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from common.exceptions.register_errors import RegisterError
from common.forms.register.register_csv_form import RegisterCsvForm
from common.issue.models import Issue
from common.issue.run_result_dto import RunResult
from common.services.domain.run.run_result_factory import RunResultFactory
from common.services.infra.persistance.run.run_result_persister import RunResultPersister
from common.services.domain.register.register_usecase_factory import RegisterUsecaseFactory
from common.services.usecase.register.register_usecase_protocol import RegisterUsecaseProtocol
from common.views.helpers.issue_table_builder import IssueTableBuilder
from common.views.register.register_view_mixin import RegisterViewMixin

CSV_ONLY_CFG = {
    "fields": [
        {"name": "csv_file", "type": "file", "label": "CSVファイル"},
    ],
    "search_cols": {"default": 1, "md": 2},
    "actions": {"placement": "below", "justify": "center", "buttons": ["register", "reset"]},
    "columns": [], "top_groups": [],
}

class RegisterCsvView(RegisterViewMixin):
    """
    CSV登録View
    - feature_key だけ子で差し替えれば動く
    - 入力定義一覧の取得や、Usecaseの呼び出しだけ差し込む
    """
    template_name = "common/list.html"
    feature_key: str = "register_csv"
    
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        GETリクエスト処理
        
        :param self: 説明
        :param request: 説明
        :type request: HttpRequest
        :return: 説明
        :rtype: HttpResponse
        """
        
        cfg = deepcopy(CSV_ONLY_CFG)
        
        # FORMインスタンス生成
        FormClass: Type[forms.Form] = self.get_form_class()
        form: RegisterCsvForm = FormClass()

        # 入力データ定義一覧取得 
        input_def_choices: List[tuple[int, str]] = self.get_input_def_choices(
            {"input_type": "CSV"}
        )
        form.fields['input_data_choices'].choices = input_def_choices
        
        fields = [
            {"name": "input_data_choices", "type": "select", "label": "入力データ定義", "choices": input_def_choices},
            {"name": "csv_file", "type": "file", "label": "CSVファイル", "accept": ".csv,text/csv"},
        ]

        # 画面表示
        context = {
            "form":         form,
            "form_action":  request.path,
            "page_title":   "CSV読み込み",
            "form_method":  "post",
            "form_enctype": "multipart/form-data",
            "input_title":  "入力項目",
            "fields":       fields,
            "input_cols":   cfg["search_cols"],
            "actions":      cfg["actions"],
            "main_menu_url":"on",
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        POSTリクエスト処理
        
        :param self: 説明
        :param request: 説明    
        :type request: HttpRequest
        :return: 説明
        :rtype: HttpResponse
        """
        cfg = deepcopy(CSV_ONLY_CFG)
        
        # FORMインスタンス生成
        FormClass: Type[forms.Form] = self.get_form_class()
        form: RegisterCsvForm = FormClass(data=request.POST, files=request.FILES)

        # 入力データ定義一覧取得 
        input_def_choices: List[tuple[int, str]] = self.get_input_def_choices(
            {"input_type": "CSV"}
        )
        form.fields['input_data_choices'].choices = input_def_choices
        fields = [
            {"name": "input_data_choices", "type": "select", "label": "入力データ定義", "choices": input_def_choices},
            {"name": "csv_file", "type": "file", "label": "CSVファイル", "accept": ".csv,text/csv"},
        ]

        # FORMバリデーションチェック
        if not form.is_valid():
            context = {
                "form":         form,
                "form_action":  request.path,
                "page_title":   "CSV読み込み",
                "form_method":  "post",
                "form_enctype": "multipart/form-data",
                "input_title":  "入力項目",
                "fields":       fields,
                "input_cols":   cfg["search_cols"],
                "actions":      cfg["actions"],
                "main_menu_url":"on",
            }
            # 画面再表示（エラー）
            return render(request, self.template_name, context)
        
        
        # 選択されたCSV種別のID
        selected_input_id = form.cleaned_data['input_data_choices']
        # 添付されたCSVファイル
        attached_csv_file = form.cleaned_data['csv_file']
        

        # 登録処理実行（データ登録基幹モジュール）
        try:
            result_issues: List[Issue] = self.run_register_usecase(
                cleaned_data={
                    "input_def_id": selected_input_id,
                    "input_source": attached_csv_file,
                }
            )
        except Exception as e:
            # catchされなかった想定外エラー
            issue = Issue.error(
                phase="UNKNOWN",
                code="REGISTER.UNEXPECTED_ERROR",
                message="予期しないエラーが発生しました。",
                context={
                    "input_id": selected_input_id,
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "trace": traceback.format_exc().splitlines()[-5:], 
                }
            )
            result_issues: List[Issue] = [issue]

        # issuesからRunResultを生成
        run_result: RunResult = RunResultFactory.from_issues(
            issues=result_issues,
            mode="SCREEN",
            source="CSV",
            input_def_id=str(selected_input_id),
            executed_by=getattr(request.user, "username", None),
            input_name=getattr(attached_csv_file, "name", None),
            tags={
                "feature_key": getattr(self, "feature_key", None),
            },
        )

        # Issue、RunResult永続化
        run_id: str = RunResultPersister().save(run_result)
        
        # 画面table要素構成
        issue_table: Dict[str, Any] = IssueTableBuilder.build(
            issues=result_issues,
            include_context=False
        )
        
        # 画面表示
        context = {
            "form":         form,
            "form_action":  request.path,
            "page_title":   "CSV読み込み共通",
            "form_method":  "post",
            "form_enctype": "multipart/form-data",
            "input_title":  "入力項目",
            "fields":       fields,
            "input_cols":   cfg["search_cols"],
            "actions":      cfg["actions"],
            "main_menu_url":"on",
            
            # ★ table.html用
            "columns":      issue_table["columns"],
            "rows":         issue_table["rows"],
            "top_groups":   issue_table["top_groups"],
        }
        
        # 画面表示メッセージ
        self.add_status_message(
            request=request,
            result=run_result,
            run_id=run_id
        )    
            
        return render(request, self.template_name, context)
        

    @override
    def run_register_usecase(
        self,
        *,
        cleaned_data: Dict[str, Any]
    ) -> List[Issue]:

        # データ登録モジュール取得
        try:
            register_usecase_instance: RegisterUsecaseProtocol = RegisterUsecaseFactory().get_register_usecase(
                input_id=cleaned_data["input_def_id"]
            )
        except RegisterError as e:
            issues: List[Issue] = [e.to_issue()]
            return issues
        
        # 登録処理実行
        issues: List[Issue] = register_usecase_instance.execute(
            input_source=cleaned_data["input_source"]
        )
        
        return issues