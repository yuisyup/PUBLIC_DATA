import pandas as pd
from typing import *
import traceback

from common.issue.models import Issue
from common.exceptions.register_errors import CsvParseError
from common.services.domain.register.dto import InputDefSpec, FkResolveSpec
from common.services.domain.register.dataframe.edit.mapping_column import MappingColumn
from common.services.domain.register.dataframe.edit.replace import Replace
from common.services.infra.input.csv_reader import CsvReader

class CsvToDataframeProcessor: 
    
    def create_dataframe(
        self,
        csv_file,
        input_def_spec: InputDefSpec,
        spec_input_list: List[FkResolveSpec],
        issues: List[Issue]
    ) -> pd.DataFrame:
        """
        CSVからDataframeへの変換を行う。<br>
        （Dataframeのカラム名は登録先Modelに準拠した名前に変換済みのもの）
        
        :param csv_file: CSVファイル
        :param input_def_spec: INPUT定義DTO
        :param spec_input_list: INPUT定義カラムDTOリスト
        :return df_mapped: 登録先Modelのカラム変換済みのDataframe
        """
        
        # CSVを読み込んでDataFrame生成
        try: 
            df_raw: pd.DataFrame = CsvReader().read_csv_to_dataframe(
                csv_file,
                input_def_spec.delimiter,
                input_def_spec.has_header)
            
        except CsvParseError as e:
            raise CsvParseError(
                context={
                    "input_id": input_def_spec.input_id,
                    "csv_name": input_def_spec.input_name,
                    "error_message": str(e),
                    "trace": traceback.format_exc().splitlines()[-5:],
                }
            ) from e
        print("---------parse後DataFrame-----------")
        print(df_raw.head())
        print("-------------------------------------")
        
        # FK変換定義から、登録先Model用のカラムマップを生成
        col_dict: Dict[int, str] = MappingColumn.map_def_column(
            specs=spec_input_list)
        
        # Dataframeのカラム名変換を実行
        df_mapped: pd.DataFrame | None = Replace.replace_column_name(
            col_dict=col_dict,
            df_raw=df_raw)
        
        if df_mapped is None:
            context={
                "input_id": input_def_spec.input_id,
                "csv_name": input_def_spec.input_name
            }
            issues.append(
                Issue.error(
                    phase="REGISTER.EDIT_DATAFRAME_COLUMN_NAME",
                    code="REGISTER.UNEXPECTED_ERROR",
                    message="CSVカラム名→DataFrame（登録先Model）カラム名のマッピングに失敗しました(マスタ不備)",
                    context=dict(**context, **col_dict),
                )
            )
            return None
        
        print("---------mapped後DataFrame-----------")
        print(df_mapped.head())
        print("-------------------------------------")
            
        
        return df_mapped
        