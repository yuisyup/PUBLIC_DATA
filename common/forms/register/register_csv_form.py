# common/forms/register/base.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from django import forms
from django.core.exceptions import ValidationError

from common.forms.register.register_base_form import RegisterBaseForm


class RegisterCsvForm(RegisterBaseForm):
    """
    CSV登録系プロトタイプの共通フォーム基底
    - 機能固有の追加フィールドは継承して足す
    """
    # CSVファイル
    csv_file = forms.FileField(
        label='CSVファイル', 
        required=True,
        error_messages={
            'required': '必須です。'
        }
    )
