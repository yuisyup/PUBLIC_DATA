from typing import Any, Dict

from django.utils import timezone

from common.services.domain.run_result_reference.dto import RunResultReferenceRow


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
