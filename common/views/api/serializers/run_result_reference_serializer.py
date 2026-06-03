from typing import Any, Dict

from django.utils import timezone

from common.services.domain.run_result_reference.dto import (
    IssueContextDetailRow,
    IssueDetailRow,
    RunResultReferenceDetail,
    RunResultReferenceRow,
)


def to_run_result_reference_row(row: RunResultReferenceRow) -> Dict[str, Any]:
    created_at = row.created_at
    if timezone.is_naive(created_at):
        created_at = timezone.make_aware(created_at)

    return {
        "runId": row.run_id,
        "inputDefId": row.input_def_id,
        "inputDefName": row.input_def_name,
        "targetModel": row.target_model,
        "createdAt": created_at.isoformat(),
    }


def to_run_result_reference_detail(
    detail: RunResultReferenceDetail,
) -> Dict[str, Any]:
    return {
        "runResult": {
            "runId": detail.run_id,
            "mode": detail.mode,
            "source": detail.source,
            "inputDefId": detail.input_def_id,
            "csvDefId": detail.csv_def_id,
            "targetModel": detail.target_model,
            "executedBy": detail.executed_by,
            "invokedBy": detail.invoked_by,
            "inputName": detail.input_name,
            "inputFingerprint": detail.input_fingerprint,
            "tagsJson": detail.tags_json,
            "startedAt": _format_datetime(detail.started_at),
            "finishedAt": _format_datetime(detail.finished_at),
            "durationMs": detail.duration_ms,
            "status": detail.status,
            "totalRows": detail.total_rows,
            "parsedRows": detail.parsed_rows,
            "fkResolvedRows": detail.fk_resolved_rows,
            "processedRows": detail.processed_rows,
            "insertedRows": detail.inserted_rows,
            "updatedRows": detail.updated_rows,
            "skippedRows": detail.skipped_rows,
            "errorRows": detail.error_rows,
            "infoCount": detail.info_count,
            "warnCount": detail.warn_count,
            "errorCount": detail.error_count,
            "summaryMessage": detail.summary_message,
            "exceptionType": detail.exception_type,
            "exceptionMessage": detail.exception_message,
            "createdAt": _format_datetime(detail.created_at),
        },
        "issues": [to_issue_detail_row(issue) for issue in detail.issues],
    }


def to_issue_detail_row(issue: IssueDetailRow) -> Dict[str, Any]:
    return {
        "id": issue.id,
        "runId": issue.run_id,
        "domain": issue.domain,
        "phase": issue.phase,
        "severity": issue.severity,
        "code": issue.code,
        "rowIndex": issue.row_index,
        "message": issue.message,
        "skipScope": issue.skip_scope,
        "createdAt": _format_datetime(issue.created_at),
        "contexts": [to_issue_context_detail_row(row) for row in issue.contexts],
    }


def to_issue_context_detail_row(row: IssueContextDetailRow) -> Dict[str, Any]:
    return {
        "id": row.id,
        "issueId": row.issue_id,
        "key": row.key,
        "valueText": row.value_text,
        "valueJson": row.value_json,
        "createdAt": _format_datetime(row.created_at),
    }


def _format_datetime(value):
    if value is None:
        return None
    if timezone.is_naive(value):
        value = timezone.make_aware(value)
    return value.isoformat()
