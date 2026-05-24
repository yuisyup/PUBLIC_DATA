from types import SimpleNamespace

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

import common.services.api.register.bulk_register_api_handler as handler_mod
from common.exceptions.register_errors import DefinitionNotFoundError
from common.issue.models import Issue
from common.services.api.register.bulk_register_api_handler import (
    BulkRegisterApiHandler,
)
from common.services.domain.run.run_result_factory import RunResultFactory


def make_request(*, input_definition_id="input-1", csv_file=None, username="tester"):
    """
    テスト用ダミーリクエスト
    """

    return SimpleNamespace(
        POST={"input_definition_id": input_definition_id},
        FILES={
            "csv_file": csv_file
            or SimpleUploadedFile(
                "data.csv", b"id,name\n1,Alice\n", content_type="text/csv"
            )
        },
        user=SimpleNamespace(username=username),
    )


class FakePersister:
    saved_run_result = None

    def save(self, run_result):
        self.__class__.saved_run_result = run_result
        return "saved-run-id"


def patch_persister(monkeypatch: pytest.MonkeyPatch):
    FakePersister.saved_run_result = None
    monkeypatch.setattr(handler_mod, "RunResultPersister", FakePersister)


def spy_run_result_factory(monkeypatch: pytest.MonkeyPatch):
    calls = []
    original = RunResultFactory.from_issues

    def fake_from_issues(**kwargs):
        calls.append(kwargs)
        return original(**kwargs)

    monkeypatch.setattr(
        handler_mod.RunResultFactory, "from_issues", staticmethod(fake_from_issues)
    )
    return calls


def test_handle_success_calls_factory_execute_run_result_and_persister(
    monkeypatch: pytest.MonkeyPatch,
):
    csv_file = SimpleUploadedFile(
        "data.csv", b"id,name\n1,Alice\n", content_type="text/csv"
    )
    issues = [
        Issue.success(
            domain="REGISTER",
            phase="REGISTER.EXECUTE",
            message="registered",
        )
    ]

    class FakeUsecase:
        called_with = None

        def execute(self, *, input_source):
            self.__class__.called_with = input_source
            return issues

    class FakeFactory:
        called_with = None

        def get_register_usecase(self, *, input_id):
            self.__class__.called_with = input_id
            return FakeUsecase()

    monkeypatch.setattr(handler_mod, "RegisterUsecaseFactory", FakeFactory)
    patch_persister(monkeypatch)
    factory_calls = spy_run_result_factory(monkeypatch)

    request = make_request(input_definition_id="input-1", csv_file=csv_file)

    response = BulkRegisterApiHandler().handle(request)

    assert response.status_code == 200
    assert response.body["success"] is True
    assert response.body["runId"] == "saved-run-id"
    assert response.body["status"] == "SUCCESS"

    assert FakeFactory.called_with == "input-1"
    assert FakeUsecase.called_with is csv_file

    assert len(factory_calls) == 1
    assert factory_calls[0]["issues"] is issues
    assert factory_calls[0]["mode"] == "SCREEN"
    assert factory_calls[0]["source"] == "CSV"
    assert factory_calls[0]["input_def_id"] == "input-1"
    assert factory_calls[0]["executed_by"] == "tester"
    assert factory_calls[0]["tags"] == {"feature_key": "register_csv_api"}

    assert FakePersister.saved_run_result is not None
    assert FakePersister.saved_run_result.status == "SUCCESS"


def test_handle_when_register_usecase_factory_raises_register_error(monkeypatch):
    class FakeFactory:
        def get_register_usecase(self, *, input_id):
            raise DefinitionNotFoundError(context={"input_id": input_id})

    monkeypatch.setattr(handler_mod, "RegisterUsecaseFactory", FakeFactory)
    patch_persister(monkeypatch)
    factory_calls = spy_run_result_factory(monkeypatch)

    request = make_request(input_definition_id="missing-input")

    response = BulkRegisterApiHandler().handle(request)

    assert response.status_code == 500
    assert response.body["success"] is False
    assert response.body["status"] == "FAILED"
    assert response.body["issues"][0]["code"] == "REGISTER.DEF_NOT_FOUND"
    assert response.body["issues"][0]["phase"] == "REGISTER.GET_USECASE"
    assert response.body["issues"][0]["severity"] == "ERROR"
    assert response.body["issues"][0]["context"] == {"input_id": "missing-input"}

    assert factory_calls[0]["issues"][0].code == "REGISTER.DEF_NOT_FOUND"
    assert FakePersister.saved_run_result.status == "FAILED"


def test_handle_when_register_usecase_factory_returns_register_error_object(
    monkeypatch: pytest.MonkeyPatch,
):
    """
    現実装では get_register_usecase が RegisterError を「返す」と、
    run_register_usecase 内で .execute が呼ばれて AttributeError になり、
    handle の UNKNOWN unexpected error として扱われる。
    """

    class FakeFactory:
        def get_register_usecase(self, *, input_id):
            return DefinitionNotFoundError(context={"input_id": input_id})

    monkeypatch.setattr(handler_mod, "RegisterUsecaseFactory", FakeFactory)
    patch_persister(monkeypatch)
    spy_run_result_factory(monkeypatch)

    request = make_request(input_definition_id="bad-input")

    response = BulkRegisterApiHandler().handle(request)

    assert response.status_code == 500
    assert response.body["success"] is False
    assert response.body["status"] == "FAILED"
    assert response.body["issues"][0]["code"] == "REGISTER.UNEXPECTED_ERROR"
    assert response.body["issues"][0]["phase"] == "UNKNOWN"
    assert response.body["issues"][0]["context"]["input_id"] == "bad-input"
    assert response.body["issues"][0]["context"]["exception_type"] == "AttributeError"


def test_handle_when_usecase_execute_returns_issue_list(
    monkeypatch: pytest.MonkeyPatch,
):
    returned_issues = [
        Issue.warn(
            phase="REGISTER.VALIDATE",
            code="REGISTER.CSV_WARNING",
            row_index=2,
            message="warning issue",
        ),
        Issue.error(
            phase="REGISTER.IMPORT",
            code="REGISTER.IMPORT_FAILED",
            row_index=3,
            message="error issue",
            context={"column": "name"},
        ),
    ]

    class FakeUsecase:
        def execute(self, *, input_source):
            return returned_issues

    class FakeFactory:
        def get_register_usecase(self, *, input_id):
            return FakeUsecase()

    monkeypatch.setattr(handler_mod, "RegisterUsecaseFactory", FakeFactory)
    patch_persister(monkeypatch)
    factory_calls = spy_run_result_factory(monkeypatch)

    request = make_request(input_definition_id="input-1")

    response = BulkRegisterApiHandler().handle(request)

    assert response.status_code == 500
    assert response.body["success"] is False
    assert response.body["status"] == "FAILED"

    assert factory_calls[0]["issues"] is returned_issues
    assert response.body["issues"][0]["severity"] == "WARN"
    assert response.body["issues"][0]["code"] == "REGISTER.CSV_WARNING"
    assert response.body["issues"][1]["severity"] == "ERROR"
    assert response.body["issues"][1]["code"] == "REGISTER.IMPORT_FAILED"

    assert FakePersister.saved_run_result.issues == returned_issues
    assert FakePersister.saved_run_result.counts.warn_count == 1
    assert FakePersister.saved_run_result.counts.error_count == 1
