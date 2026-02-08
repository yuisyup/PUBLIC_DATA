from __future__ import annotations

from typing import Any, Dict, List, Optional
import json

from common.issue.models import Issue


class IssueTableBuilder:
    """
    table.html 用の columns / rows / top_groups を構築
    - rows は "key -> value" のdict（テンプレ側で get_item 参照される）
    """

    @staticmethod
    def build(
        issues: List[Issue],
        *,
        include_context: bool = True,
        context_max_len: int = 400,
    ) -> Dict[str, Any]:
        columns = [
            {"key": "severity", "label": "Severity"},
            {"key": "domain", "label": "Domain"},
            {"key": "phase", "label": "Phase"},
            {"key": "code", "label": "Code"},
            {"key": "row_index", "label": "Row"},
            {"key": "message", "label": "Message"},
            {"key": "skip_scope", "label": "Skip"},
        ]

        if include_context:
            columns.append({"key": "context", "label": "Context"})

        rows: List[Dict[str, Any]] = []
        for i in issues:
            row = {
                "severity": i.severity,
                "domain": i.domain,
                "phase": i.phase,
                "code": i.code,
                "row_index": i.row_index,
                "message": i.message,
                "skip_scope": i.skip_scope,
            }
            if include_context:
                row["context"] = IssueTableBuilder._context_to_str(i.context, context_max_len)
            rows.append(row)

        # top_groups は使わないなら空でOK（table.html は無ければ通常theadになる）
        top_groups: List[Dict[str, Any]] = []

        return {
            "columns": columns,
            "rows": rows,
            "top_groups": top_groups,
        }

    @staticmethod
    def _context_to_str(ctx: Optional[Dict[str, Any]], max_len: int) -> str:
        if not ctx:
            return ""
        try:
            s = json.dumps(ctx, ensure_ascii=False, default=str, separators=(",", ":"))
        except Exception:
            s = str(ctx)
        if len(s) > max_len:
            return s[: max_len - 3] + "..."
        return s
