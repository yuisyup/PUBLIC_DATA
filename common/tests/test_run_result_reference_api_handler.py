from datetime import datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from django.utils import timezone

from common.models import MsInputDef, MsInputType, MsRegisterPolicy, RunResultRecord
from common.services.api.run_result_reference.run_result_reference_api_handler import (
    RunResultReferenceApiHandler,
)
from common.services.domain.run_result_reference.dto import (
    RunResultReferenceCriteria,
    RunResultReferenceRow,
)
from common.services.infra.persistance.repositories.run_result_reference.run_result_reference_repository import (
    RunResultReferenceRepository,
)


def make_request(*, params=None, method="GET"):
    return SimpleNamespace(method=method, GET=params or {})


def test_handle_success_calls_usecase_with_criteria():
    calls = []
    row = RunResultReferenceRow(
        run_id="run-1",
        input_def_id="1",
        input_def_name="Customer CSV",
        target_model="Customer",
        created_at=timezone.make_aware(datetime(2026, 6, 2, 10, 0, 0)),
    )

    class FakeUsecase:
        def search(self, criteria: RunResultReferenceCriteria):
            calls.append(criteria)
            return [row]

    request = make_request(
        params={
            "input_type": "CSV",
            "input_def_id": "1",
            "created_at": "2026-06-02",
        }
    )

    response = RunResultReferenceApiHandler(usecase=FakeUsecase()).handle(request)

    assert response.status_code == 200
    assert response.body["success"] is True
    assert response.body["issues"] == []
    assert response.body["results"][0]["runId"] == "run-1"
    assert response.body["results"][0]["inputDefName"] == "Customer CSV"

    assert calls == [
        RunResultReferenceCriteria(
            input_type="CSV",
            input_def_id="1",
            created_at=datetime(2026, 6, 2).date(),
        )
    ]


def test_handle_invalid_created_at_returns_issue():
    response = RunResultReferenceApiHandler().handle(
        make_request(params={"created_at": "2026/06/02"})
    )

    assert response.status_code == 400
    assert response.body["success"] is False
    assert response.body["results"] == []
    assert response.body["issues"][0]["severity"] == "ERROR"
    assert response.body["issues"][0]["phase"] == "RUN_RESULT_REFERENCE.REQUEST"
    assert response.body["issues"][0]["code"] == (
        "RUN_RESULT_REFERENCE.INVALID_CREATED_AT"
    )


def test_handle_non_get_returns_issue():
    response = RunResultReferenceApiHandler().handle(make_request(method="POST"))

    assert response.status_code == 405
    assert response.body["success"] is False
    assert response.body["issues"][0]["code"] == (
        "RUN_RESULT_REFERENCE.METHOD_NOT_ALLOWED"
    )


@pytest.mark.django_db
def test_repository_search_filters_and_resolves_input_def_name():
    csv_type = MsInputType.objects.create(
        input_type_code="CSV",
        input_type_name="CSV",
        input_type_usecase_class_path="dummy.CsvUsecase",
    )
    api_type = MsInputType.objects.create(
        input_type_code="API",
        input_type_name="API",
        input_type_usecase_class_path="dummy.ApiUsecase",
    )
    policy = MsRegisterPolicy.objects.create(
        policy_code="INSERT",
        policy_name="Insert",
        policy_processor_class_path="dummy.InsertPolicy",
    )
    csv_input = MsInputDef.objects.create(
        input_name="Customer CSV",
        target_model_name="Customer",
        input_type=csv_type,
        register_policy=policy,
    )
    api_input = MsInputDef.objects.create(
        input_name="Partner API",
        target_model_name="Partner",
        input_type=api_type,
        register_policy=policy,
    )

    target_date = timezone.make_aware(datetime(2026, 6, 2, 10, 0, 0))
    other_date = timezone.make_aware(datetime(2026, 6, 1, 10, 0, 0))
    matching = create_run_result_record(
        input_def_id=str(csv_input.input_id),
        target_model="Customer",
        created_at=target_date,
    )
    create_run_result_record(
        input_def_id=str(api_input.input_id),
        target_model="Partner",
        created_at=target_date,
    )
    create_run_result_record(
        input_def_id=str(csv_input.input_id),
        target_model="Customer",
        created_at=other_date,
    )

    rows = RunResultReferenceRepository().search(
        RunResultReferenceCriteria(
            input_type="CSV",
            input_def_id=str(csv_input.input_id),
            created_at=target_date.date(),
        )
    )

    assert len(rows) == 1
    assert rows[0].run_id == str(matching.run_id)
    assert rows[0].input_def_name == "Customer CSV"
    assert rows[0].target_model == "Customer"


def create_run_result_record(
    *, input_def_id: str, target_model: str, created_at: datetime
) -> RunResultRecord:
    record = RunResultRecord.objects.create(
        run_id=uuid4(),
        mode="SCREEN",
        source="CSV",
        input_def_id=input_def_id,
        target_model=target_model,
        started_at=created_at,
        status="SUCCESS",
    )
    RunResultRecord.objects.filter(pk=record.pk).update(created_at=created_at)
    record.refresh_from_db()
    return record
