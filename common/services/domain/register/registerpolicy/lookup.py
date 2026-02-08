from __future__ import annotations
from typing import Any, Dict, Iterable

from common.exceptions.register_errors import FailedCreateDuplicationLookupKwargsError

class Lookup:

    @staticmethod
    def build_lookup(
        data: Dict[str, Any],
        lookup_fields: Iterable[str]
    ) -> Dict[str, Any]:
        """
        
        検索条件（lookup）を組み立てる
        
        :param data: 1行分のデータ
        :type data: Dict[str, Any]
        :param lookup_fields: 検索条件となるカラム群
        :type lookup_fields: Iterable[str]
        :return: Dict[検索対象カラム, 検索条件値]
        """
        
        lookup = {}
        for k in lookup_fields:
            if k not in data:
                raise FailedCreateDuplicationLookupKwargsError(
                    context={
                        "lookup_fields": lookup_fields,
                        "data_keys": list(data.keys())
                    }
                )
            lookup[k] = data[k]
        return lookup