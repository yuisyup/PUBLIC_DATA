from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class RunResultReferenceCriteria:
    input_type: Optional[str] = None
    input_def_id: Optional[str] = None
    created_at: Optional[date] = None


@dataclass(frozen=True)
class RunResultReferenceRow:
    run_id: str
    input_def_id: Optional[str]
    input_def_name: Optional[str]
    target_model: Optional[str]
    created_at: datetime


@dataclass(frozen=True)
class IssueContextDetailRow:
    id: str
    issue_id: str
    key: str
    value_text: Optional[str]
    value_json: Optional[Dict[str, Any]]
    created_at: datetime


@dataclass(frozen=True)
class IssueDetailRow:
    id: str
    run_id: str
    domain: str
    phase: str
    severity: str
    code: str
    row_index: Optional[int]
    message: Optional[str]
    skip_scope: str
    created_at: datetime
    contexts: List[IssueContextDetailRow]


@dataclass(frozen=True)
class RunResultReferenceDetail:
    run_id: str
    mode: str
    source: str
    input_def_id: Optional[str]
    csv_def_id: Optional[str]
    target_model: Optional[str]
    executed_by: Optional[str]
    invoked_by: Optional[str]
    input_name: Optional[str]
    input_fingerprint: Optional[str]
    tags_json: Optional[Dict[str, Any]]
    started_at: datetime
    finished_at: Optional[datetime]
    duration_ms: Optional[int]
    status: str
    total_rows: int
    parsed_rows: int
    fk_resolved_rows: int
    processed_rows: int
    inserted_rows: int
    updated_rows: int
    skipped_rows: int
    error_rows: int
    info_count: int
    warn_count: int
    error_count: int
    summary_message: Optional[str]
    exception_type: Optional[str]
    exception_message: Optional[str]
    created_at: datetime
    issues: List[IssueDetailRow]
