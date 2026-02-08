from typing import Protocol
import pandas as pd

class PreprocessorProtocol(Protocol):
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        ...
