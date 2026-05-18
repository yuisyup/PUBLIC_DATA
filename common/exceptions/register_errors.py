from typing import Any, Dict, Optional

from common.exceptions.app_error import AppError
from common.issue.models import (
    Issue,
    DomainCode,
    IssueCode,
    IssuePhase,
    IssueSeverity,
    SkipScope,
)


class RegisterError(AppError):
    """
    データ登録・更新基幹モジュール共通例外基底クラス
    """

    _DOMAIN: str = "REGISTER"


class DefinitionNotFoundError(RegisterError):
    _PHASE: IssuePhase = "REGISTER.GET_USECASE"
    _CODE: IssueCode = "REGISTER.DEF_NOT_FOUND"
    _MESSAGE = "入力データ定義が見つかりません。"


class ColumnDefinitionNotFoundError(RegisterError):
    _PHASE: IssuePhase = "REGISTER.GET_USECASE"
    _CODE: IssueCode = "REGISTER.COLUMN_DEF_NOT_FOUND"
    _MESSAGE = "入力データカラム定義が見つかりません。"


class RegisterUsecaseClassNotFoundError(RegisterError):
    _PHASE: IssuePhase = "REGISTER.GET_USECASE"
    _CODE: IssueCode = "REGISTER.USECASE_CLASS_NOT_FOUND"
    _MESSAGE = "データ登録・更新基幹モジュールのユースケースクラスが見つかりません。"


class CsvParseError(RegisterError):
    _PHASE: IssuePhase = "REGISTER.CSV_PARSE"
    _CODE: IssueCode = "REGISTER.UNEXPECTED_ERROR"
    # messageは任意指定


class FkResolveDefIncompleteError(RegisterError):
    _PHASE: IssuePhase = "REGISTER.FK_RESOLVE"
    _CODE: IssueCode = "REGISTER.DEF_ERROR_INCOMPLETE"
    _MESSAGE = "入力データカラム定義に不足があります。"


class FkResolveLookupFieldsMismatchError(RegisterError):
    _PHASE: IssuePhase = "REGISTER.FK_RESOLVE"
    _CODE: IssueCode = "REGISTER.DEF_ERROR_LOOKUP_FIELDS_MISMATCH"
    _MESSAGE = "入力データ定義の検索キー個数（元データ、Model）が一致しません。"


class FkResolveFailedCreateLookupKwargsError(RegisterError):
    _PHASE: IssuePhase = "REGISTER.FK_RESOLVE"
    _CODE: IssueCode = "REGISTER.FAILED_CREATE_FK_LOOKUP_KWARGS"
    _MESSAGE = "FK解決用Moedlの検索条件作成に失敗しました。"


class RegisterPolicyNotFoundError(RegisterError):
    _PHASE: IssuePhase = "REGISTER.GET_POLICY"
    _CODE: IssueCode = "REGISTER.POLICY_CLASS_NOT_FOUND"
    _MESSAGE = "データ登録・更新基幹ポリシークラスが見つかりません。"


class FailedCreateDuplicationLookupKwargsError(RegisterError):
    _PHASE: IssuePhase = "REGISTER.POST_PROCESS"
    _CODE: IssueCode = "REGISTER.FAILED_CREATE_DUPLICATION_LOOKUP_KWARGS"
    _MESSAGE = "重複チェック用Moedlの検索条件作成に失敗しました。"
