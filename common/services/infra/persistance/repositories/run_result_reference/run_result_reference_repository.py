from datetime import datetime, time, timedelta
from typing import Dict, List, Optional

from django.utils import timezone

from common.models import IssueRecord, MsInputDef, RunResultRecord
from common.services.domain.run_result_reference.dto import (
    IssueContextDetailRow,
    IssueDetailRow,
    RunResultReferenceCriteria,
    RunResultReferenceDetail,
    RunResultReferenceRow,
)


class RunResultReferenceRepository:
    def search(
        self, criteria: RunResultReferenceCriteria
    ) -> List[RunResultReferenceRow]:
        queryset = RunResultRecord.objects.all().order_by("-created_at")

        if criteria.input_def_id:
            queryset = queryset.filter(input_def_id=str(criteria.input_def_id))

        if criteria.created_at:
            start_at = timezone.make_aware(
                datetime.combine(criteria.created_at, time.min)
            )
            end_at = start_at + timedelta(days=1)
            queryset = queryset.filter(created_at__gte=start_at, created_at__lt=end_at)

        if criteria.input_type:
            input_def_ids = MsInputDef.objects.filter(
                input_type_id=criteria.input_type
            ).values_list("input_id", flat=True)
            queryset = queryset.filter(input_def_id__in=[str(i) for i in input_def_ids])

        records = list(queryset)
        input_def_ids = {
            int(record.input_def_id)
            for record in records
            if record.input_def_id and str(record.input_def_id).isdigit()
        }
        input_def_names: Dict[str, str] = {
            str(input_def.input_id): input_def.input_name
            for input_def in MsInputDef.objects.filter(input_id__in=input_def_ids)
        }

        return [
            RunResultReferenceRow(
                run_id=str(record.run_id),
                input_def_id=record.input_def_id,
                input_def_name=input_def_names.get(str(record.input_def_id)),
                target_model=record.target_model,
                created_at=record.created_at,
            )
            for record in records
        ]

    def get_detail(self, run_id: str) -> Optional[RunResultReferenceDetail]:
        try:
            record = RunResultRecord.objects.get(pk=run_id)
        except RunResultRecord.DoesNotExist:
            return None

        issues = (
            IssueRecord.objects.filter(run=record)
            .prefetch_related("contexts")
            .order_by("created_at", "id")
        )

        issue_rows: List[IssueDetailRow] = []
        for issue in issues:
            context_rows = [
                IssueContextDetailRow(
                    id=str(context.id),
                    issue_id=str(issue.id),
                    key=context.key,
                    value_text=context.value_text,
                    value_json=context.value_json,
                    created_at=context.created_at,
                )
                for context in issue.contexts.all()
            ]
            issue_rows.append(
                IssueDetailRow(
                    id=str(issue.id),
                    run_id=str(record.run_id),
                    domain=issue.domain,
                    phase=issue.phase,
                    severity=issue.severity,
                    code=issue.code,
                    row_index=issue.row_index,
                    message=issue.message,
                    skip_scope=issue.skip_scope,
                    created_at=issue.created_at,
                    contexts=context_rows,
                )
            )

        return RunResultReferenceDetail(
            run_id=str(record.run_id),
            mode=record.mode,
            source=record.source,
            input_def_id=record.input_def_id,
            csv_def_id=record.csv_def_id,
            target_model=record.target_model,
            executed_by=record.executed_by,
            invoked_by=record.invoked_by,
            input_name=record.input_name,
            input_fingerprint=record.input_fingerprint,
            tags_json=record.tags_json,
            started_at=record.started_at,
            finished_at=record.finished_at,
            duration_ms=record.duration_ms,
            status=record.status,
            total_rows=record.total_rows,
            parsed_rows=record.parsed_rows,
            fk_resolved_rows=record.fk_resolved_rows,
            processed_rows=record.processed_rows,
            inserted_rows=record.inserted_rows,
            updated_rows=record.updated_rows,
            skipped_rows=record.skipped_rows,
            error_rows=record.error_rows,
            info_count=record.info_count,
            warn_count=record.warn_count,
            error_count=record.error_count,
            summary_message=record.summary_message,
            exception_type=record.exception_type,
            exception_message=record.exception_message,
            created_at=record.created_at,
            issues=issue_rows,
        )
