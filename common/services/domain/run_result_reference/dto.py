from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


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
