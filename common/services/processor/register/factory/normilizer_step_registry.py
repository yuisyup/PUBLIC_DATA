from typing import *

from common.exceptions.app_error import NormalizerRegistryError
from common.services.processor.register.normalizer.steps.normalizer_steps_protocol import (
    NormalizerStepsProtocol,
)
from common.services.processor.register.normalizer.steps.add_execute_date import (
    AddExecuteDate,
)


class NormalizerStepRegistry:
    """
    preprocess_key -> Preprocessor class の対応表

    """

    _map: Dict[str, Type[NormalizerStepsProtocol]] = {
        # 実行日付与
        "ADD_EXECUTE_DATE": AddExecuteDate,
    }

    def resolve(self, key: str) -> Type[NormalizerStepsProtocol]:
        try:
            return self._map[key]
        except KeyError as e:
            raise NormalizerRegistryError(
                f"前処理クラスが見つかりません。key: {key}"
            ) from e
