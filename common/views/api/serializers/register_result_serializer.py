from typing import Any, Dict, List

from common.issue.models import Issue
from common.issue.run_result_dto import RunResult
from common.views.api.serializers.issue_serializer import to_issue_dto


def to_register_csv_response(
    *,
    run_result: RunResult,
    run_id: str,
    issues: List[Issue],
) -> Dict[str, Any]:

    issue_dtos = [to_issue_dto(issue) for issue in issues]

    return {
        "success": run_result.status in ["SUCCESS", "SUCCESS_WITH_WARN"],
        "runId": run_id,
        "status": run_result.status,
        "summary": {
            "totalIssues": len(issue_dtos),
            "errorCount": sum(1 for i in issue_dtos if i["severity"] == "ERROR"),
            "warningCount": sum(1 for i in issue_dtos if i["severity"] == "WARNING"),
            "infoCount": sum(1 for i in issue_dtos if i["severity"] == "INFO"),
        },
        "issues": issue_dtos,
    }
