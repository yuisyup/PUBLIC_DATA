from typing import *
import pandas as pd

class Replace:
    
    @staticmethod
    def replace_column_name(
        col_dict: Dict[int, str],
        df_raw: pd.DataFrame
    )-> pd.DataFrame | None:
        """
        入力データのDataFrameカラム名から、Modelに対応したカラム名に変更したDataFrameを返す。<br>
        （input_source_key → model_target_field_name）
        
        :param col_dict: 変換したいカラム名辞書（列数、model_target_field_name）
        :param df_raw: DataFrame（生データ）
        :return df_mapped: DataFrame（カラム名変換後）　※変換失敗時はNone
        """
        
        try:
            df_mapped = df_raw.rename(columns=col_dict)
        except Exception as e:
            return None
        
        return df_mapped