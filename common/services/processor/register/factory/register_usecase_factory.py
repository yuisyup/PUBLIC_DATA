from typing import *

from common.exceptions.register_errors import DefinitionNotFoundError, ColumnDefinitionNotFoundError, RegisterUsecaseClassNotFoundError
from common.services.usecase.register.register_usecase_protocol import RegisterUsecaseProtocol
from common.services.usecase.register.abstract_register_usecase import AbstractRegisterUsecase
from common.services.domain.register.dto import InputDefRaw, InputDefSpec, FkResolveSpecInput, FkResolveSpec
from common.services.infra.persistance.repositories.input_definition_repository import InputDefinitionRepository
from common.utils.import_utils import ImportUtils

class RegisterUsecaseFactory:

    def get_register_usecase(
        self, 
        input_id: int
    ) -> RegisterUsecaseProtocol:
        """
        データ登録・更新基幹モジュールのユースケースインスタンスを返す。<br>
        入力データIDによって返却されるインスタンスが変わる。
        
        :param input_id: 入力データID
        :return register_usecase: データ登録・更新モジュールインスタンス
        :raise Exceptipnを継承した独自例外: 入力データ定義取得失敗<br>入力データカラム定義取得失敗<br>データ登録更新基幹モジュールのユースケースクラス解決失敗
        """
        
        # データ定義マスタRepository
        repo: InputDefinitionRepository = InputDefinitionRepository()
        
        # 1. 入力データ定義マスタ取得
        input_def_raw: InputDefRaw = repo.get_input_def_as_dto(input_id=input_id)
        if input_def_raw is None:
            raise DefinitionNotFoundError(
                context={"input_id": input_id}
            )
        
        def_spec: InputDefSpec = InputDefSpec.create(inp=input_def_raw)
        
        # 2. 入力データ定義カラムマスタリスト取得
        col_specs_raw: List[FkResolveSpecInput] = repo.lookup_column_defs_as_dto(input_id=input_id)
        if not col_specs_raw:
            raise ColumnDefinitionNotFoundError(
                context={
                    "input_id": input_id,
                    "csv_name": def_spec.input_name
                }
            )
        
        col_specs: List[FkResolveSpec] = []
        for raw in col_specs_raw:
            col_specs.append(FkResolveSpec.create(inp=raw))
        
        # 3. データ登録・更新基幹モジュールのユースケース「クラス」を取得
        try:
            register_usecase: Type[AbstractRegisterUsecase] = ImportUtils.import_class(
                full_path=def_spec.input_type_usecase_class_path)
        except (ImportError, AttributeError) as e:
            raise RegisterUsecaseClassNotFoundError(
                context={
                    "input_id": input_id,
                    "csv_name": def_spec.input_name,
                    "class_path": def_spec.input_type_usecase_class_path,
                    "log": str(e)
                }
            ) from e
        
        # 4. データ登録・更新基幹モジュールのユースケースインスタンスを返却
        return register_usecase(
            def_spec=def_spec, 
            col_specs=col_specs)