from __future__ import annotations
from typing import *
import pandas as pd
from django.db import models

from common.issue.models import Issue

class RegisterProcessorProtocol(Protocol):

    def execute(
        self, 
        df: pd.DataFrame, 
        model_class: models.Model, 
        issues: List[Issue],
        lookup_fields,    
    ):
        """
        入力種別に応じてInputデータをDataframeに変換し、<br>
        INPUT定義マスタ内容に従ってDB登録を行う。
        
        :param self: 説明
        :param df: FK変換済みDataframe
        :type df: pd.DataFrame
        :param model_class: 登録先Modelインスタンス
        :type model_class: models.Model
        :param issues: 発生事象リスト
        :type issues: List[Issue]
        :param lookup_fields: 重複チェック検索条件
        :raises :raises: ValidationError, DatabaseError
        
        """
        ...