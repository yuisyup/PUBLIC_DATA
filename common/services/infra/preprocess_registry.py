from typing import *

from common.exceptions.app_error import PreprocessRegistryError
from common.services.domain.register.preprocess.preprocessor_protocol import PreprocessorProtocol
from common.services.domain.register.preprocess.add_execute_date import AddExecuteDatePreprocessor

class PreprocessRegistry:
    """
    preprocess_key -> Preprocessor class の対応表
    
    """
    _map: Dict[str, Type[PreprocessorProtocol]] = {
        
        # 実行日付与
        "ADD_EXECUTE_DATE": AddExecuteDatePreprocessor,
    }

    def resolve(self, key: str) -> Type[PreprocessorProtocol]:
        try:
            return self._map[key]
        except KeyError as e:
            raise PreprocessRegistryError(f"前処理クラスが見つかりません。key: {key}") from e
