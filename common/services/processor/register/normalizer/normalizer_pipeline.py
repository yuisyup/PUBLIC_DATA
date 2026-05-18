import pandas as pd
from typing import List
from common.services.processor.register.normalizer.steps.normalizer_steps_protocol import (
    NormalizerStepsProtocol,
)


class NormalizerPipeline:
    def __init__(self, processors: List[NormalizerStepsProtocol]):
        self._processors = processors

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        for p in self._processors:
            df = p.process(df)
        return df
