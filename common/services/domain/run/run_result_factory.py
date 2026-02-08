from __future__ import annotations
from typing import Any, Optional, List
from datetime import datetime, timezone

from common.issue.models import Issue
from common.issue.run_result_dto import RunResult


class RunResultFactory:
    @staticmethod
    def from_issues(
        *,
        issues: List[Issue],
        mode: str,
        source: str,
        input_def_id: Optional[str] = None,
        target_model: Optional[str] = None,
        executed_by: Optional[str] = None,
        invoked_by: Optional[str] = None,
        input_name: Optional[str] = None,
        input_fingerprint: Optional[str] = None,
        tags: Optional[dict[str, Any]] = None,
        summary_message: Optional[str] = None,
        exception_type: Optional[str] = None,
        exception_message: Optional[str] = None,
        forced_status: Optional[str] = None,
    ) -> RunResult:
        rr = RunResult.start(
            mode=mode,
            source=source,
            input_def_id=input_def_id,
            target_model=target_model,
            executed_by=executed_by,
            invoked_by=invoked_by,
            input_name=input_name,
            input_fingerprint=input_fingerprint,
            tags=tags,
        )

        rr = rr.add_issues(issues).finish(
            finished_at=datetime.now(timezone.utc),
            summary_message=summary_message or RunResultFactory._pick_summary(issues),
            exception_type=exception_type,
            exception_message=exception_message,
            forced_status=forced_status,
        )
        return rr

    @staticmethod
    def _pick_summary(issues: List[Issue]) -> Optional[str]:
        for sev in ("ERROR", "WARN", "INFO"):
            for i in issues:
                if i.severity == sev and i.message:
                    return i.message
        return None
