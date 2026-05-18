import pandas as pd
from io import TextIOWrapper
from typing import *

from common.exceptions.register_errors import CsvParseError


class CsvReader:

    def read_csv_to_dataframe(
        self, csv_file, delimiter: str, has_header: bool = False
    ) -> pd.DataFrame:
        """
        CSVファイルをDataFrameに変換する。

        :param csv_file: CSVファイル
        :param delimiter: デリミタ
        :type delimiter: str
        :param has_header: ヘッダー有無フラグ
        :type has_header: bool
        :return: CSVから変換したDataFrame
        :rtype: pd.DataFrame
        """

        try:
            # pandasでCSV読み込み
            df_raw: pd.DataFrame = pd.read_csv(
                TextIOWrapper(csv_file, encoding="utf-8"),
                delimiter=delimiter,
                header=0 if has_header else None,
            )
            return df_raw

        except UnicodeDecodeError as e:
            raise CsvParseError(message="文字コードがUTF-8ではありません。") from e

        except pd.errors.EmptyDataError:
            raise CsvParseError(message="CSVが空です。") from e

        except pd.errors.ParserError as e:
            raise CsvParseError(message="CSVの構造が壊れています。") from e

        except ValueError as e:
            raise CsvParseError(message="read_csvの引数設定に問題があります。") from e

        except OSError as e:
            raise CsvParseError(
                message="ファイルストリームが壊れているか閉じています。"
            ) from e

        except Exception as e:
            raise CsvParseError(
                message="その他の予期しないエラーが発生しました。"
            ) from e
