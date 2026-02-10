import ast
import pandas as pd
from typing import *

from common.exceptions.register_errors import FkResolveFailedCreateLookupKwargsError

if TYPE_CHECKING:
    from common.services.domain.register.dto import FkResolveSpec


class Build:
    
    @staticmethod
    def parse_list(val):
        """
        :param val: パースしたい要素
        :return: パース済み要素
        """
        
        if isinstance(val, str):
            try:
                return ast.literal_eval(val)
            except Exception:
                    return [val]
                
        return val or []
    
    @staticmethod
    def build_lookup_kwargs(
        row: Dict[Any,Any],
        fk_spec: "FkResolveSpec"
    ) -> Dict[Any, Any]:
        """
        FK変換先Modelの検索条件を組み立てる。<br>
        fk_spec.fk_lookup_fields（FK変換先Modelカラム名）＝ fk_spec.input_lookup_fieldsの値（入力データカラムの「値」）
        
        :param row: DataFrameのFK変換を行いたい行（辞書化したもの）
        :type row: Dict[Any, Any]
        :param fk_spec: FK変換定義DTO
        :type fk_spec: FkResolveSpec
        :return: FK変換先Model検索条件辞書
        :rtype: Dict[Any, Any]
        """
        
        lookup_kwargs = {}
        
        # FK変換が必要なカラム数分繰り返す
        for model_key, df_col in zip(fk_spec.fk_lookup_fields, fk_spec.input_lookup_fields):
                    
            # INPUT側カラムの内容
            value = row.get(df_col)
                    
            # 欠損チェック
            if pd.isna(value):
                # 欠損あり：解決不能のため空で返却
                raise FkResolveFailedCreateLookupKwargsError(
                    context={
                        "input_id": fk_spec.input_id,
                        "column_order": fk_spec.column_order,
                        "input_lookup_fields": fk_spec.input_lookup_fields,
                        "fk_lookup_fields": fk_spec.fk_lookup_fields
                    }
                )
                    
            # Model側（検索条件側）の対応しているカラムにINPUT側の「変換前入力値」を挿入
            lookup_kwargs[model_key] = value
            
        return lookup_kwargs