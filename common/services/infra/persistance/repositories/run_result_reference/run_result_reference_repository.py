from datetime import datetime, time, timedelta
from typing import Dict, List

from django.utils import timezone

from common.models import MsInputDef, RunResultRecord
from common.services.domain.run_result_reference.dto import (
    RunResultReferenceCriteria,
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
