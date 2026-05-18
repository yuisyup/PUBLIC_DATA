from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

from common.issue.models import Issue

RunStatus = Literal[
    "SUCCESS",  # エラー無しで完了
    "SUCCESS_WITH_WARN",  # WARNありだが完了
    "FAILED",  # ERRORあり（かつ継続不能 or 仕様上失敗）
    "ABORTED",  # 外部要因/致命的例外などで中断
]

RunMode = Literal[
    "BATCH",
    "SCREEN",
]

RunSource = Literal[
    "CSV",
    "MANUAL",
    "API",
]


@dataclass(frozen=True)
class RunContext:
    """
    実行1回のメタ情報（どこから/何を/誰が）
    """

    run_id: str
    mode: RunMode
    source: RunSource

    # 何の定義で動いたか（あなたの DefSpec の識別子）
    input_def_id: Optional[str] = None
    csv_def_id: Optional[str] = None

    # 対象（あなたの ModelRegistry で解決するキー）
    target_model: Optional[str] = None

    # 実行者や実行元（バッチ名、画面ユーザーなど）
    executed_by: Optional[str] = None
    invoked_by: Optional[str] = None  # e.g. "nightly_register_job"

    # 入力ファイルなど（CSVならファイル名/パス/ハッシュ）
    input_name: Optional[str] = None
    input_fingerprint: Optional[str] = None  # sha256など

    # 任意（後から追跡用）
    tags: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RunCounts:
    """
    バッチ運用で「数字」を見たいので、集計枠を先に用意しておく
    """

    total_rows: int = 0  # 入力行数
    parsed_rows: int = 0  # 読めた行数（CSV→DF）
    fk_resolved_rows: int = 0  # FK解決済みの行数（成功した行）
    processed_rows: int = 0  # 登録処理対象に回した行数
    inserted_rows: int = 0  # INSERT件数
    updated_rows: int = 0  # UPDATE件数（upsert等）
    skipped_rows: int = 0  # スキップした行数（重複/未解決/バリデ等）
    error_rows: int = 0  # エラーのあった行数（ユニークrow_index数）

    # issue集計
    info_count: int = 0
    warn_count: int = 0
    error_count: int = 0


@dataclass(frozen=True)
class RunTiming:
    started_at: datetime
    finished_at: Optional[datetime] = None

    @property
    def duration_ms(self) -> Optional[int]:
        if self.finished_at is None:
            return None
        delta = self.finished_at - self.started_at
        return int(delta.total_seconds() * 1000)


@dataclass(frozen=True)
class RunResult:
    """
    実行1回の最終結果（ログ・制御・永続化の基準点）
    """

    context: RunContext
    timing: RunTiming
    status: RunStatus

    counts: RunCounts = field(default_factory=RunCounts)
    issues: List[Issue] = field(default_factory=list)  # 本番は List[Issue]

    # 失敗/中断の代表メッセージ（運用の一覧画面で見たい）
    summary_message: Optional[str] = None

    # 例外の代表情報（詳細は Issue.context にも持たせる想定）
    exception_type: Optional[str] = None
    exception_message: Optional[str] = None

    # ---------- factory ----------
    @classmethod
    def start(
        cls,
        *,
        mode: RunMode,
        source: RunSource,
        input_def_id: Optional[str] = None,
        csv_def_id: Optional[str] = None,
        target_model: Optional[str] = None,
        executed_by: Optional[str] = None,
        invoked_by: Optional[str] = None,
        input_name: Optional[str] = None,
        input_fingerprint: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
    ) -> "RunResult":
        now = datetime.now(timezone.utc)
        ctx = RunContext(
            run_id=str(uuid4()),
            mode=mode,
            source=source,
            input_def_id=input_def_id,
            csv_def_id=csv_def_id,
            target_model=target_model,
            executed_by=executed_by,
            invoked_by=invoked_by,
            input_name=input_name,
            input_fingerprint=input_fingerprint,
            tags=tags or {},
        )
        return cls(
            context=ctx,
            timing=RunTiming(started_at=now),
            status="SUCCESS",  # 仮。finish()で確定させる
            counts=RunCounts(),
            issues=[],
        )

    # ---------- mutation-like (pure) methods ----------
    def add_issue(self, issue: Any) -> "RunResult":
        # immutable方針：新しいRunResultを返す
        new_issues = [*self.issues, issue]
        new_counts = self._recount(new_issues)
        return RunResult(
            context=self.context,
            timing=self.timing,
            status=self.status,
            counts=new_counts,
            issues=new_issues,
            summary_message=self.summary_message,
            exception_type=self.exception_type,
            exception_message=self.exception_message,
        )

    def add_issues(self, issues: List[Any]) -> "RunResult":
        new_issues = [*self.issues, *issues]
        new_counts = self._recount(new_issues)
        return RunResult(
            context=self.context,
            timing=self.timing,
            status=self.status,
            counts=new_counts,
            issues=new_issues,
            summary_message=self.summary_message,
            exception_type=self.exception_type,
            exception_message=self.exception_message,
        )

    def with_counts(self, **kwargs: int) -> "RunResult":
        # countsの特定フィールド更新用（例：inserted_rows += n など）
        base = self.counts
        new_counts = RunCounts(**{**base.__dict__, **kwargs})
        return RunResult(
            context=self.context,
            timing=self.timing,
            status=self.status,
            counts=new_counts,
            issues=self.issues,
            summary_message=self.summary_message,
            exception_type=self.exception_type,
            exception_message=self.exception_message,
        )

    def finish(
        self,
        *,
        finished_at: Optional[datetime] = None,
        summary_message: Optional[str] = None,
        exception_type: Optional[str] = None,
        exception_message: Optional[str] = None,
        forced_status: Optional[RunStatus] = None,
    ) -> "RunResult":
        end = finished_at or datetime.now(timezone.utc)

        # status決定
        status = forced_status or self._derive_status()

        return RunResult(
            context=self.context,
            timing=RunTiming(started_at=self.timing.started_at, finished_at=end),
            status=status,
            counts=self.counts,
            issues=self.issues,
            summary_message=summary_message or self.summary_message,
            exception_type=exception_type or self.exception_type,
            exception_message=exception_message or self.exception_message,
        )

    # ---------- helpers ----------
    def _derive_status(self) -> RunStatus:
        # issuesの severity を見て status を決める想定
        # Issueが確定していれば issue.severity を見る
        # ここでは Any なので属性が無い時は無視（実装時に型をIssueに固定すればOK）
        has_error = any(getattr(i, "severity", None) == "ERROR" for i in self.issues)
        has_warn = any(getattr(i, "severity", None) == "WARN" for i in self.issues)

        if has_error:
            return "FAILED"
        if has_warn:
            return "SUCCESS_WITH_WARN"
        return "SUCCESS"

    def _recount(self, issues: List[Any]) -> RunCounts:
        # まずは Issue の件数集計だけ。行数集計は Usecase側で入れる運用でOK。
        info = sum(1 for i in issues if getattr(i, "severity", None) == "INFO")
        warn = sum(1 for i in issues if getattr(i, "severity", None) == "WARN")
        error = sum(1 for i in issues if getattr(i, "severity", None) == "ERROR")

        # error_rows は row_index のユニーク数（row_index Noneは除外）
        row_indexes = {
            getattr(i, "row_index", None)
            for i in issues
            if getattr(i, "severity", None) == "ERROR"
        }
        row_indexes.discard(None)

        base = self.counts
        return RunCounts(
            total_rows=base.total_rows,
            parsed_rows=base.parsed_rows,
            fk_resolved_rows=base.fk_resolved_rows,
            processed_rows=base.processed_rows,
            inserted_rows=base.inserted_rows,
            updated_rows=base.updated_rows,
            skipped_rows=base.skipped_rows,
            error_rows=len(row_indexes),
            info_count=info,
            warn_count=warn,
            error_count=error,
        )
