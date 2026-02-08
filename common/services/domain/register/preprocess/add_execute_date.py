import pandas as pd
from datetime import date
from common.services.domain.register.preprocess.preprocessor_protocol import PreprocessorProtocol

class AddExecuteDatePreprocessor(PreprocessorProtocol):
    def __init__(self, column_name: str = "execute_date", value: str | None = None):
        self.column_name = column_name
        self.value = value or date.today().isoformat()

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df[self.column_name] = self.value
        return df
