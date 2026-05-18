from typing import Any, Dict, Optional

from common.issue.models import (
    Issue,
    DomainCode,
    IssueCode,
    IssuePhase,
    IssueSeverity,
    SkipScope,
)


class AppError(Exception):
    """
    アプリケーション共通の基底例外。
    想定内エラーは必ずこれ（またはサブクラス）を継承する。
    """

    # ===== クラス定数（サブクラスで上書きする前提） =====
    _DOMAIN: DomainCode = "COMMON"
    _PHASE: IssuePhase = "UNKNOWN"
    _CODE: IssueCode = "COMMON.UNSPECIFIED"
    _MESSAGE: str = "Application error occurred."
    _SEVERITY: IssueSeverity = "ERROR"
    _ROW_INDEX: Optional[int] = None
    _SKIP_SCOPE: SkipScope = "ALL"

    def __init__(
        self,
        *,
        context: Optional[Dict[str, Any]] = None,
        message: Optional[str] = None,
    ):
        # Exceptionのメッセージは最終的に人間が見る文字列
        super().__init__(message or self._MESSAGE)

        # context は「状況情報」なので instance が持つ
        self.context: Dict[str, Any] = context or {}

        # メッセージだけは instance override を許可（任意）
        self._message_override: Optional[str] = message

    # ===== 読み取り専用プロパティ（外部から上書き不可） =====
    @property
    def domain(self) -> str:
        return self._DOMAIN

    @property
    def phase(self) -> str:
        return self._PHASE

    @property
    def code(self) -> str:
        return self._CODE

    @property
    def severity(self) -> str:
        return self._SEVERITY

    @property
    def skip_scope(self) -> SkipScope:
        return self._SKIP_SCOPE

    @property
    def message(self) -> str:
        return self._message_override or self._MESSAGE

    @property
    def row_index(self) -> Optional[int]:
        return self._ROW_INDEX

    # ===== Issue 変換（Usecaseで一元利用） =====

    def to_issue(self, row_index: Optional[int] = None) -> Issue:
        """
        【汎用】独自例外クラスからIssueオブジェクトへの変換を行う。

        （備考）Issueセット内容一覧:
            - domain
            - phase
            - code
            - severity
            - message
            - context
            - skip_scope
            - row_index（引数優先）

        :param self: インスタンスメソッド
        :param row_index: 列数
        :type row_index: Optional[int]
        :return: 発生事象リスト
        :rtype: Issue
        """

        if row_index is not None:
            use_row_index = row_index
        else:
            use_row_index = self.row_index

        return Issue(
            domain=self.domain,
            phase=self.phase,
            code=self.code,
            severity=self.severity,
            message=self.message,
            context=self.context,
            skip_scope=self.skip_scope,
            row_index=use_row_index,
        )


class ModelRegistryError(AppError):
    """
    モデルクラス生成失敗時の例外

    ⚠CAUTION:
        - 例外発生後の処理を呼出し元で実装すること
        - Issueへの変換を行う場合、処理の文脈にphase, code等を合わせること
    """

    ...


class FeatureKeyFormNotFoundError(AppError):
    """
    feature_key（画面/機能キー）からFormクラス解決失敗時の例外

    ⚠CAUTION:
        - 例外発生後の処理を呼出し元で実装すること
        - Issueへの変換を行う場合、処理の文脈にphase, code等を合わせること
    """

    ...


class FailedCreateInputDefChoicesError(AppError):
    """
    入力データ定義選択肢を生成できない場合の例外<br>
    （画面からの呼び出しを想定）

    ⚠CAUTION:
        - 例外発生後の処理を呼出し元で実装すること
        - Issueへの変換を行う場合、処理の文脈にphase, code等を合わせること
    """

    ...


class NormalizerRegistryError(Exception):
    """
    前処理実行クラス生成に失敗した場合の例外<br>

    ⚠CAUTION:
        - 例外発生後の処理を呼出し元で実装すること
        - Issueへの変換を行う場合、処理の文脈にphase, code等を合わせること
    """

    ...


class NormalizerDefinitionError(Exception):
    """
    前処理定義の解決に失敗した場合の例外
    ⚠CAUTION:
        - 例外発生後の処理を呼出し元で実装すること
        - Issueへの変換を行う場合、処理の文脈にphase, code等を合わせること
    """
