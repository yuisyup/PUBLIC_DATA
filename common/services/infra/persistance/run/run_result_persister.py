from __future__ import annotations

import uuid
from typing import List
from django.db import transaction

from common.issue.run_result_dto import RunResult

from common.models import RunResultRecord
from common.models import IssueRecord
from common.models import IssueContextRecord


class RunResultPersister:
    @transaction.atomic
    def save(self, run_result: RunResult) -> str:
        rr = run_result

        # 1) RunResultRecord（DTO run_id をPKに）
        rr_rec = RunResultRecord.objects.create(
            run_id=rr.context.run_id,  # UUIDをそのまま
            mode=rr.context.mode,
            source=rr.context.source,
            input_def_id=rr.context.input_def_id,
            csv_def_id=getattr(rr.context, "csv_def_id", None),
            target_model=rr.context.target_model,
            executed_by=rr.context.executed_by,
            invoked_by=rr.context.invoked_by,
            input_name=rr.context.input_name,
            input_fingerprint=rr.context.input_fingerprint,
            tags_json=rr.context.tags or {},
            started_at=rr.timing.started_at,
            finished_at=rr.timing.finished_at,
            duration_ms=rr.timing.duration_ms,
            status=rr.status,
            total_rows=rr.counts.total_rows,
            parsed_rows=rr.counts.parsed_rows,
            fk_resolved_rows=rr.counts.fk_resolved_rows,
            processed_rows=rr.counts.processed_rows,
            inserted_rows=rr.counts.inserted_rows,
            updated_rows=rr.counts.updated_rows,
            skipped_rows=rr.counts.skipped_rows,
            error_rows=rr.counts.error_rows,
            info_count=rr.counts.info_count,
            warn_count=rr.counts.warn_count,
            error_count=rr.counts.error_count,
            summary_message=rr.summary_message,
            exception_type=rr.exception_type,
            exception_message=rr.exception_message,
        )

        # 2) IssueRecord（UUIDを明示採番して bulk_create）
        issue_recs: List[IssueRecord] = []
        for dto in rr.issues:
            issue_recs.append(
                IssueRecord(
                    id=uuid.uuid4(),  # ★明示採番：bulkでも確実に手元に残る
                    run=rr_rec,
                    domain=dto.domain,
                    phase=dto.phase,
                    severity=dto.severity,
                    code=dto.code,
                    row_index=dto.row_index,
                    message=dto.message,
                    skip_scope=dto.skip_scope,
                )
            )
        if issue_recs:
            IssueRecord.objects.bulk_create(issue_recs, batch_size=1000)

        # 3) IssueContextRecord（issue_idを直接埋めて bulk）
        ctx_recs: List[IssueContextRecord] = []
        for issue_rec, dto in zip(issue_recs, rr.issues):
            ctx = dto.context or {}
            for k, v in ctx.items():
                if v is None:
                    continue
                if isinstance(v, (str, int, float, bool)):
                    ctx_recs.append(
                        IssueContextRecord(
                            issue_id=issue_rec.id,  # ★再取得不要
                            key=str(k),
                            value_text=str(v),
                        )
                    )
                else:
                    ctx_recs.append(
                        IssueContextRecord(
                            issue_id=issue_rec.id,
                            key=str(k),
                            value_json=v,
                        )
                    )
        if ctx_recs:
            IssueContextRecord.objects.bulk_create(ctx_recs, batch_size=2000)

        return str(rr.context.run_id)
