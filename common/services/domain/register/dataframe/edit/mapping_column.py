from typing import *

from common.services.domain.register.dto import FkResolveSpec


class MappingColumn:

    @staticmethod
    def map_def_column(specs: List[FkResolveSpec]) -> Dict[int, str]:
        """
        FK解決定義リストから、DataFrameのカラムNo,カラム名辞書を一覧で返す

        :param specs: FK変換定義リスト
        :return col_dict: カラムNo,カラム名（model_target_field_name）辞書
        """
        col_dict = {i: spec.model_target_field_name for i, spec in enumerate(specs)}

        return col_dict
