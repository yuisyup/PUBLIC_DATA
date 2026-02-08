from dataclasses import dataclass
from typing import *

from common.issue.codes import DomainCode, IssueCode, IssuePhase, IssueSeverity, SkipScope

@dataclass(frozen=True)
class Issue:
    """
    実行中に発生した事象（成功/警告/エラー）を統一的に保持するDTO

    """
    
    # 系コード
    domain: DomainCode

    # どの局面で起きたか
    phase: IssuePhase

    # 成功/警告/エラー
    severity: IssueSeverity

    # 事象コード
    code: IssueCode

    # 行No（DataFrameのindex）
    row_index: Optional[int] = None

    # 検索条件 / 例外情報 / 入力値など（機械処理＆デバッグ用）
    context: Optional[Dict[str, Any]] = None

    # 人間向けメッセージ
    message: Optional[str] = None

    # スキップの範囲
    skip_scope: SkipScope = "NONE"

    # ---------- factory methods ----------

    @classmethod
    def success(
        cls,
        domain: DomainCode,
        phase: IssuePhase,
        row_index: Optional[int] = None,
        message: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> "Issue":
        return cls(
            domain=domain,
            phase=phase,
            severity="INFO",
            code=domain + ".SUCCESS",
            row_index=row_index,
            message=message,
            context=context,
            skip_scope="NONE",
        )

    @classmethod
    def warn(
        cls,
        phase: IssuePhase,
        code: IssueCode,
        row_index: Optional[int] = None,
        message: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        skip_scope: SkipScope = "NONE",  # 重複ならROWスキップにしたい、などもここで表現可
    ) -> "Issue":
        return cls(
            domain=code.split(".")[0],
            phase=phase,
            severity="WARN",
            code=code,
            row_index=row_index,
            message=message,
            context=context,
            skip_scope=skip_scope,
        )

    @classmethod
    def error(
        cls,
        phase: IssuePhase,
        code: IssueCode,
        row_index: Optional[int] = None,
        message: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        skip_scope: SkipScope = "ALL",
    ) -> "Issue":
        return cls(
            domain=code.split(".")[0],
            phase=phase,
            severity="ERROR",
            code=code,
            row_index=row_index,
            message=message,
            context=context,
            skip_scope=skip_scope,
        )