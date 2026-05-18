# common/views/register/base.py
from __future__ import annotations

from django.views import View

from common.forms.form_factory import FormFactory


class BaseView(View):
    """
    基底Viewクラス

    クラス変数:
        - template_name: テンプレート名（デフォルトは "common/list.html"）
        - feature_key: 画面/機能キー (子で上書き)
    """

    template_name: str = "common/list.html"
    feature_key: str = ""  # 子で上書き

    def get_form_class(self):
        """
        feature_keyに対応するFormクラスを取得する。

        :param self: 説明
        """
        return FormFactory.get_form_class(self.feature_key)
