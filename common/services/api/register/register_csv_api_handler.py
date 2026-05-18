from typing import *
import traceback
from django.http import HttpRequest, JsonResponse

from common.exceptions.register_errors import RegisterError
from common.issue.models import Issue
from common.issue.run_result_dto import RunResult
from common.services.domain.run.run_result_factory import RunResultFactory
from common.services.infra.persistance.run.run_result_persister import (
    RunResultPersister,
)
from common.services.processor.register.factory.register_usecase_factory import (
    RegisterUsecaseFactory,
)
from common.services.usecase.register.register_usecase_protocol import (
    RegisterUsecaseProtocol,
)
from common.services.api.register.api_response import ApiResponse
from common.views.helpers.issue_table_builder import IssueTableBuilder
from common.views.register.register_view_mixin import RegisterViewMixin

from common.views.api.serializers.register_result_serializer import (
    to_register_csv_response,
)


class RegisterCsvApiHandler(RegisterViewMixin):

    def handle(self, request: HttpRequest):

        # 入力データ定義ID
        input_def_id = request.POST.get("input_definition_id")
        # CSVファイル
        csv_file = request.FILES.get("csv_file")

        # 登録処理実行（データ登録基幹モジュール）
        try:
            result_issues: List[Issue] = self.run_register_usecase(
                cleaned_data={
                    "input_def_id": input_def_id,
                    "input_source": csv_file,
                }
            )
        except Exception as e:
            # catchされなかった想定外エラー
            issue = Issue.error(
                phase="UNKNOWN",
                code="REGISTER.UNEXPECTED_ERROR",
                message="予期しないエラーが発生しました。",
                context={
                    "input_id": input_def_id,
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "trace": traceback.format_exc().splitlines()[-5:],
                },
            )
            result_issues: List[Issue] = [issue]

        # issuesからRunResultを生成
        run_result: RunResult = RunResultFactory.from_issues(
            issues=result_issues,
            mode="SCREEN",
            source="CSV",
            input_def_id=str(input_def_id),
            executed_by=getattr(request.user, "username", None),
            input_name=getattr(input_def_id, "name", None),
            tags={
                "feature_key": "register_csv_api",
            },
        )

        # Issue、RunResult永続化
        run_id: str = RunResultPersister().save(run_result)

        # レスポンス用Dict作成
        body: Dict[str, Any] = to_register_csv_response(
            run_result=run_result,
            run_id=run_id,
            issues=result_issues,
        )

        # レスポンス
        status_code = 200
        if run_result.status == "FAILED":
            status_code = 500

        return ApiResponse(body=body, status_code=status_code)

    @override
    def run_register_usecase(self, *, cleaned_data: Dict[str, Any]) -> List[Issue]:

        # データ登録モジュール取得
        try:
            register_usecase_instance: (
                RegisterUsecaseProtocol
            ) = RegisterUsecaseFactory().get_register_usecase(
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

    def _bad_request_issue(
        self,
        *,
        code: str,
        message: str,
        context: Dict[str, Any] | None = None,
    ) -> ApiResponse:
        issue = Issue.error(
            phase="REQUEST",
            code=code,
            message=message,
            context=context or {},
        )

        body = {
            "success": False,
            "runId": None,
            "status": "FAILED",
            "summary": {
                "totalIssues": 1,
                "errorCount": 1,
                "warningCount": 0,
                "infoCount": 0,
            },
            "issues": [
                {
                    "severity": issue.severity,
                    "phase": issue.phase,
                    "code": issue.code,
                    "message": issue.message,
                    "context": issue.context,
                }
            ],
        }

        return ApiResponse(body=body, status_code=400)
