from typing import Dict, List, Any
from django.db.models import QuerySet
from common.models import MsInputColumnDef


class ColumnMapper:
    """
    MsInputColumnDef の定義を元に、
    入力データの source key（input_source_key）をモデルの target field に変換するマッピングクラス
    """

    def __init__(self, column_defs: QuerySet[MsInputColumnDef]):
        self.column_defs = column_defs
        self.source_to_target_map = self._generate_source_to_target_map()

    def _generate_source_to_target_map(self) -> Dict[str, str]:
        """
        input_source_key（カンマ区切り対応）を基にマッピング辞書を生成
        """
        mapping = {}
        for col in self.column_defs:
            # "名前,氏名" のように複数キーがある場合にも対応
            aliases = [s.strip() for s in col.input_source_key.split(',')]
            for alias in aliases:
                mapping[alias] = col.model_target_field_name
        return mapping

    def apply(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        単一のレコードに対してキー名をマッピング
        """
        return {
            self.source_to_target_map.get(k, k): v
            for k, v in record.items()
        }

    def apply_batch(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        複数レコードに対して一括変換
        """
        return [self.apply(r) for r in records]
