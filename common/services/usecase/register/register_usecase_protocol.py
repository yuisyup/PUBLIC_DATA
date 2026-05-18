from __future__ import annotations
from typing import *

from common.issue.models import Issue


class RegisterUsecaseProtocol(Protocol):

    def execute(
        self,
        input_source: Any,
    ) -> List[Issue]:
        """
        入力種別に応じてInputデータをDataframeに変換し、<br>
        INPUT定義マスタ内容に従ってDB登録を行う。

        :param input_source: 入力データ
        :return List[Issue]: 発生事象リスト
        """
        ...
