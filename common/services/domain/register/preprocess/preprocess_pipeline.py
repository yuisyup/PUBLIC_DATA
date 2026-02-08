import pandas as pd
from typing import List
from common.services.domain.register.preprocess.preprocessor_protocol import PreprocessorProtocol

class PreprocessPipeline:
    def __init__(self, processors: List[PreprocessorProtocol]):
        self._processors = processors

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        for p in self._processors:
            df = p.process(df)
        return df
