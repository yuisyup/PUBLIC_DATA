# common/forms/register/base.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from django import forms


class RegisterBaseForm(forms.Form):
    """
    登録系プロトタイプの共通フォーム基底
    - 機能固有の追加フィールドは継承して足す
    """
    # 入力データ定義選択肢
    input_data_choices = forms.ChoiceField(
        label='入力データ定義', 
        required=True,
        error_messages={
            'required': '必須です。'
        }
    )
