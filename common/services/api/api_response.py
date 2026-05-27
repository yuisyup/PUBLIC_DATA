from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ApiResponse:
    """
    【api_handler共通】レスポンス型定義クラス
    """

    # レスポンスボディ
    body: Dict[str, Any]
    # リクエストステータス
    status_code: int
