from typing import Any, Dict

from common.issue.models import Issue


def to_issue_dto(issue: Issue) -> Dict[str, Any]:
    return {
        "severity": issue.severity,
        "phase": issue.phase,
        "code": issue.code,
        "row": issue.row_index,
        "message": issue.message,
        "skip": issue.skip_scope,
        "context": issue.context,
    }
