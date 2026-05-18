from django.db import transaction
import traceback

from django.db import models, DatabaseError
from django.core.exceptions import ValidationError
from typing import *
import pandas as pd

from common.issue.models import Issue
from common.services.processor.register.loader.policy_execute.register_processor_protocol import (
    RegisterProcessorProtocol,
)
from common.exceptions.register_errors import FailedCreateDuplicationLookupKwargsError
from common.services.domain.register.registerpolicy.lookup import Lookup
from common.services.infra.persistance.django_model_persister import ModelPersister


class UpsertRegisterProcessor(RegisterProcessorProtocol):

    def __init__(self, persister: ModelPersister):
        """
        初期化

        :param persister: ModelPersister（永続化用クラス→Usecaseで指定）
        """
        self._persister = persister

    @override
    @transaction.atomic
    def execute(
        self,
        df: pd.DataFrame,
        model_class: models.Model,
        issues: List[Issue],
        lookup_fields,
    ):

        # 登録したいデータ件数分ループ
        for i, row in df.iterrows():

            # FK解決失敗など、登録不可な行の発生事象（Issue）を取り出す
            error_issues: List[Issue] = [
                issue
                for issue in issues
                if issue.row_index == i and issue.severity == "ERROR"
            ]

            # ERRORの発生がある場合スキップ
            if len(error_issues) > 0:
                continue

            # 辞書化した1行分のデータ
            data: Dict[str, Any] = row.dropna().to_dict()

            try:
                # 検索条件の組立
                lookup: Dict[str, Any] = Lookup.build_lookup(data, lookup_fields)
            except FailedCreateDuplicationLookupKwargsError as e:
                issues.append(e.to_issue(row_index=i + 1))
                continue

            # 重複レコードを検索
            try:
                obj: models.Model | None = self._persister.lookup_first(
                    model_class, **lookup
                )
            except DatabaseError as e:
                raise e

            dupulication_flg: bool = False

            # 重複レコード存在の場合　→　UPDATE
            if obj:
                for k, v in data.items():
                    if k not in lookup_fields:
                        setattr(obj, k, v)

                dupulication_flg = True

            # 重複レコード存在しない場合　→　INSERT
            else:
                obj = model_class(**data)

            try:
                # 登録処理実行（I/O）
                self._persister.create(model_class, data)
            except ValidationError as e:
                issue = Issue.error(
                    phase="REGISTER.POST_PROCESS",
                    code="REGISTER.FAILED_REGISTER_BY_VALIDATION",
                    message="full_clean()によるバリデーションエラーで登録に失敗しました。",
                    context={
                        **{"row_index": i + 1},
                        **data
                        ** {
                            "error_message": str(e),
                            "trace": traceback.format_exc().splitlines()[-5:],
                        },
                    },
                    skip_scope="ROW",
                )
                issues.append(issue)
                continue
            except DatabaseError as e:
                raise e

        # 処理成功時
        if dupulication_flg:
            message = "登録処理が重複更新行ありで完了しました。"
            context = {
                **{"row_index": i + 1},
                **lookup_fields,
            }
        else:
            message = "登録処理が完了しました。"
            context = {
                **{"row_index": i + 1},
            }

        issue = Issue.success(
            domain="REGISTER",
            phase="REGISTER.POST_PROCESS",
            message=message,
            context=context,
        )
        issues.append(issue)

        return
