from datetime import date
from typing import List

from django.http import HttpRequest

from common.issue.models import Issue
from common.services.api.api_response import ApiResponse
from common.services.domain.run_result_reference.dto import RunResultReferenceCriteria
from common.services.usecase.run_result_reference.run_result_reference_usecase import (
    RunResultReferenceUsecase,
)
from common.views.api.serializers.issue_serializer import to_issue_dto
from common.views.api.serializers.run_result_reference_serializer import (
    to_run_result_reference_detail,
    to_run_result_reference_row,
)


class RunResultReferenceApiHandler:
    def __init__(self, usecase: RunResultReferenceUsecase = None):
        self.usecase = usecase or RunResultReferenceUsecase()

    def handle(self, request: HttpRequest) -> ApiResponse:
        if request.method != "GET":
            issue = Issue.error(
                phase="RUN_RESULT_REFERENCE.REQUEST",
                code="RUN_RESULT_REFERENCE.METHOD_NOT_ALLOWED",
                message="GET method is required.",
            )
            return self._error_response([issue], status_code=405)

        try:
            criteria = self._build_criteria(request)
        except ValueError as error:
            issue = Issue.error(
                phase="RUN_RESULT_REFERENCE.REQUEST",
                code="RUN_RESULT_REFERENCE.INVALID_CREATED_AT",
                message=str(error),
            )
            return self._error_response([issue], status_code=400)

        rows = self.usecase.search(criteria)

        return ApiResponse(
            body={
                "success": True,
                "results": [to_run_result_reference_row(row) for row in rows],
                "issues": [],
            },
            status_code=200,
        )

    def _build_criteria(self, request: HttpRequest) -> RunResultReferenceCriteria:
        created_at = request.GET.get("created_at") or None
        parsed_created_at = None
        if created_at:
            try:
                parsed_created_at = date.fromisoformat(created_at)
            except ValueError as error:
                raise ValueError("created_at must be YYYY-MM-DD.") from error

        return RunResultReferenceCriteria(
            input_type=request.GET.get("input_type") or None,
            input_def_id=request.GET.get("input_def_id") or None,
            created_at=parsed_created_at,
        )

    def _error_response(self, issues: List[Issue], status_code: int) -> ApiResponse:
        return ApiResponse(
            body={
                "success": False,
                "results": [],
                "issues": [to_issue_dto(issue) for issue in issues],
            },
            status_code=status_code,
        )


class RunResultReferenceDetailApiHandler:
    def __init__(self, usecase: RunResultReferenceUsecase = None):
        self.usecase = usecase or RunResultReferenceUsecase()

    def handle(self, request: HttpRequest, *, run_id: str) -> ApiResponse:
        if request.method != "GET":
            issue = Issue.error(
                phase="RUN_RESULT_REFERENCE_DETAIL.REQUEST",
                code="RUN_RESULT_REFERENCE_DETAIL.METHOD_NOT_ALLOWED",
                message="GET method is required.",
            )
            return self._error_response([issue], status_code=405)

        detail = self.usecase.get_detail(run_id)
        if detail is None:
            issue = Issue.error(
                phase="RUN_RESULT_REFERENCE_DETAIL.GET",
                code="RUN_RESULT_REFERENCE_DETAIL.NOT_FOUND",
                message="Run result was not found.",
                context={"run_id": run_id},
            )
            return self._error_response([issue], status_code=404)

        return ApiResponse(
            body={
                "success": True,
                **to_run_result_reference_detail(detail),
                "issuesForError": [],
            },
            status_code=200,
        )

    def _error_response(self, issues: List[Issue], status_code: int) -> ApiResponse:
        return ApiResponse(
            body={
                "success": False,
                "runResult": None,
                "issues": [],
                "issuesForError": [to_issue_dto(issue) for issue in issues],
            },
            status_code=status_code,
        )
