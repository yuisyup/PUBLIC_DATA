from typing import Protocol
import pandas as pd

class NormalizerStepsProtocol(Protocol):
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        ...
