from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ApiResponse:
    body: Dict[str, Any]
    status_code: int
