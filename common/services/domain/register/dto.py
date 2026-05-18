from dataclasses import dataclass
from typing import *

from common.services.domain.register.dataframe.resolve_fk.build import Build


@dataclass(frozen=True)
class InputDefRaw:

    input_id: int
    input_name: str
    target_model_name: str
    input_type: str
    delimiter: str
    has_header: bool
    register_policy: str
    insert_duplication_lookup_fields: str
    input_type_usecase_class_path: str
    policy_processor_class_path: str


@dataclass(frozen=True)
class InputDefSpec:

    input_id: int
    input_name: str
    target_model_name: str
    input_type: str
    delimiter: str
    has_header: bool
    register_policy: str
    insert_duplication_lookup_fields: List[str]
    input_type_usecase_class_path: str
    policy_processor_class_path: str

    @classmethod
    def create(cls, inp: InputDefRaw):

        parsed_insert_duplication_lookup_fields = Build.parse_list(
            inp.insert_duplication_lookup_fields
        )

        return cls(
            input_id=inp.input_id,
            input_name=inp.input_name,
            target_model_name=inp.target_model_name,
            input_type=inp.input_type,
            delimiter=inp.delimiter,
            has_header=inp.has_header,
            register_policy=inp.register_policy,
            insert_duplication_lookup_fields=parsed_insert_duplication_lookup_fields,
            input_type_usecase_class_path=inp.input_type_usecase_class_path,
            policy_processor_class_path=inp.policy_processor_class_path,
        )


@dataclass(frozen=True)
class FkResolveSpecInput:
    """
    生定義：MsInputColumnDef相当DTO
    """

    input_id: int
    column_order: int
    input_source_key: str
    model_target_field_name: str
    is_fk_flag: bool
    is_lookup_only: bool
    input_lookup_fields: str
    fk_target_model: str
    fk_target_field: str
    fk_lookup_fields: str
    display_name: str


@dataclass(frozen=True)
class FkResolveSpec:
    """
    FK変換定義DTO
    """

    # 入力定義ID
    input_id: int
    # カラムNo（ログ用）
    column_order: int
    # 表示名（ログ用）
    display_name: str
    # FK変換必要/不要フラグ
    is_fk_flag: bool
    # 検索のみフラグ
    is_lookup_only: bool
    # 元データカラム名
    input_source_key: str

    # DataFrame上で置換対象となる列
    # ＝データ登録を行うModelのカラム名（例: player_id）
    model_target_field_name: str

    # 【FK変換先情報】---------------------------------------------------↓

    # FK変換先Model（app_label.ModelName形式）（例: main.MsTeam）
    fk_target_model: str
    # 取得するカラム名＝変換先カラム名（例: player_id）
    fk_target_field: str
    # -----------------------------------------------------------------↑

    # 【FK変換先Model検索条件（WHERE KEY(例：name) = VALUE(例：taro)）】----------------------------------------↓

    # ＜KEY＞モデル側の「検索キー（検索条件対象カラム）」（例：["name", "birthday"]）
    fk_lookup_fields: List[str]
    # ＜VALUE>入力（DataFrame）側で、「検索条件値」が入っているDataFrameカラム（例：["csv_name", "csv_birthday"]）
    input_lookup_fields: List[str]
    # ------------------------------------------------------------------------------------------------------↑

    @classmethod
    def create(cls, inp: FkResolveSpecInput):

        # パース
        parsed_fk_lookup_fields = Build.parse_list(inp.fk_lookup_fields)
        parsed_input_lookup_fields = Build.parse_list(inp.input_lookup_fields)

        return cls(
            input_id=inp.input_id,
            column_order=inp.column_order,
            display_name=inp.display_name,
            is_fk_flag=inp.is_fk_flag,
            is_lookup_only=inp.is_lookup_only,
            input_source_key=inp.input_source_key,
            model_target_field_name=inp.model_target_field_name,
            fk_target_model=inp.fk_target_model,
            fk_target_field=inp.fk_target_field,
            fk_lookup_fields=parsed_fk_lookup_fields,
            input_lookup_fields=parsed_input_lookup_fields,
        )
