from typing import *

from common.exceptions.register_errors import (
    FkResolveDefIncompleteError,
    FkResolveLookupFieldsMismatchError,
)
from common.services.domain.register.dto import FkResolveSpec


class CheckDef:

    @staticmethod
    def check(spec: FkResolveSpec):
        """
        入力データカラム定義の内容をチェックします。

        :param spec: 入力データカラム定義
        :type spec: FkResolveSpec
        :return: （発生事象コード=IssueCode, エラーメッセージ）
        :rtype: Tuple[str, str]
        """

        # データ正常にそろってなければエラー(フラグ以外チェック)
        if not (
            spec.input_id
            and spec.column_order
            and spec.model_target_field_name
            and spec.fk_target_model
            and spec.fk_target_field
            and spec.fk_lookup_fields
            and spec.input_lookup_fields
        ):

            raise FkResolveDefIncompleteError(
                context={"input_id": spec.input_id, "column_order": spec.column_order}
            )

        # FK変換に使用する入力側、Model側のカラム個数不一致はデータ不整合のためエラー
        if len(spec.fk_lookup_fields) != len(spec.input_lookup_fields):
            raise FkResolveLookupFieldsMismatchError(
                context={
                    "input_id": spec.input_id,
                    "column_order": spec.column_order,
                    "fk_lookup_fields": spec.fk_lookup_fields,
                    "input_lookup_fields": spec.input_lookup_fields,
                }
            )

        return
