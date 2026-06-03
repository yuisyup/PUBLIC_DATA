from datetime import datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from django.utils import timezone

from common.models import (
    IssueContextRecord,
    IssueRecord,
    MsInputDef,
    MsInputType,
    MsRegisterPolicy,
    RunResultRecord,
)
from common.services.api.run_result_reference.run_result_reference_api_handler import (
    RunResultReferenceApiHandler,
    RunResultReferenceDetailApiHandler,
)
from common.services.domain.run_result_reference.dto import (
    IssueDetailRow,
    RunResultReferenceCriteria,
    RunResultReferenceDetail,
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


def test_detail_handle_success_calls_usecase():
    run_id = str(uuid4())
    created_at = timezone.make_aware(datetime(2026, 6, 2, 10, 0, 0))
    detail = RunResultReferenceDetail(
        run_id=run_id,
        mode="SCREEN",
        source="CSV",
        input_def_id="1",
        csv_def_id=None,
        target_model="Customer",
        executed_by="tester",
        invoked_by=None,
        input_name="data.csv",
        input_fingerprint="fingerprint",
        tags_json={"feature_key": "bulk_register"},
        started_at=created_at,
        finished_at=created_at,
        duration_ms=10,
        status="SUCCESS",
        total_rows=1,
        parsed_rows=1,
        fk_resolved_rows=1,
        processed_rows=1,
        inserted_rows=1,
        updated_rows=0,
        skipped_rows=0,
        error_rows=0,
        info_count=1,
        warn_count=0,
        error_count=0,
        summary_message="summary",
        exception_type=None,
        exception_message=None,
        created_at=created_at,
        issues=[
            IssueDetailRow(
                id=str(uuid4()),
                run_id=run_id,
                domain="REGISTER",
                phase="REGISTER.EXECUTE",
                severity="INFO",
                code="REGISTER.SUCCESS",
                row_index=None,
                message="registered",
                skip_scope="NONE",
                created_at=created_at,
                contexts=[],
            )
        ],
    )
    calls = []

    class FakeUsecase:
        def get_detail(self, target_run_id):
            calls.append(target_run_id)
            return detail

    response = RunResultReferenceDetailApiHandler(usecase=FakeUsecase()).handle(
        make_request(),
        run_id=run_id,
    )

    assert response.status_code == 200
    assert response.body["success"] is True
    assert response.body["runResult"]["runId"] == run_id
    assert response.body["runResult"]["mode"] == "SCREEN"
    assert response.body["issues"][0]["code"] == "REGISTER.SUCCESS"
    assert response.body["issuesForError"] == []
    assert calls == [run_id]


def test_detail_handle_not_found_returns_issue():
    run_id = str(uuid4())

    class FakeUsecase:
        def get_detail(self, target_run_id):
            return None

    response = RunResultReferenceDetailApiHandler(usecase=FakeUsecase()).handle(
        make_request(),
        run_id=run_id,
    )

    assert response.status_code == 404
    assert response.body["success"] is False
    assert response.body["runResult"] is None
    assert response.body["issues"] == []
    assert response.body["issuesForError"][0]["code"] == (
        "RUN_RESULT_REFERENCE_DETAIL.NOT_FOUND"
    )
    assert response.body["issuesForError"][0]["context"] == {"run_id": run_id}


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


@pytest.mark.django_db
def test_repository_get_detail_returns_run_issues_and_contexts():
    created_at = timezone.make_aware(datetime(2026, 6, 2, 10, 0, 0))
    record = create_run_result_record(
        input_def_id="1",
        target_model="Customer",
        created_at=created_at,
    )
    issue = IssueRecord.objects.create(
        run=record,
        domain="REGISTER",
        phase="REGISTER.VALIDATE",
        severity="ERROR",
        code="REGISTER.INVALID",
        row_index=2,
        message="invalid row",
        skip_scope="ROW",
    )
    context = IssueContextRecord.objects.create(
        issue=issue,
        key="column",
        value_text="name",
        value_json={"expected": "not blank"},
    )

    detail = RunResultReferenceRepository().get_detail(str(record.run_id))

    assert detail is not None
    assert detail.run_id == str(record.run_id)
    assert detail.mode == "SCREEN"
    assert detail.source == "CSV"
    assert detail.input_def_id == "1"
    assert detail.target_model == "Customer"
    assert len(detail.issues) == 1
    assert detail.issues[0].id == str(issue.id)
    assert detail.issues[0].code == "REGISTER.INVALID"
    assert len(detail.issues[0].contexts) == 1
    assert detail.issues[0].contexts[0].id == str(context.id)
    assert detail.issues[0].contexts[0].value_json == {"expected": "not blank"}


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
