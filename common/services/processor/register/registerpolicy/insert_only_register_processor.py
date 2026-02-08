from django.db import transaction
import traceback

from django.db import models, DatabaseError
from django.core.exceptions import ValidationError
from typing import *
import pandas as pd

from common.issue.models import Issue
from common.exceptions.register_errors import FailedCreateDuplicationLookupKwargsError
from common.services.domain.register.registerpolicy.lookup import Lookup
from common.services.processor.register.registerpolicy.register_processor_protocol import RegisterProcessorProtocol
from common.services.infra.persistance.django_model_persister import ModelPersister

class InsertOnlyRegisterProcessor(RegisterProcessorProtocol):
    
    def __init__(
        self, 
        persister: ModelPersister):
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
            error_issues: List[Issue]= [issue for issue in issues if issue.row_index == i and issue.severity == "ERROR"]
            
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
            
            try:
                exist_duplicate_record: bool = self._persister.exists_by_lookup(model_class, lookup)
            except DatabaseError as e:
                raise e
                
            # InsertOnlyルール（すでにレコード存在すれば拒否）
            if exist_duplicate_record:
                issue = Issue.warn(
                    phase="REGISTER.POST_PROCESS",
                    code="REGISTER.DUPLICATION",
                    message="重複レコードがあります。",
                    context={
                        **{"row_index": i + 1},
                        **data,
                        **lookup
                    }
                )
                issues.append(issue)
                continue

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
                        **{
                            "error_message": str(e),
                            "trace": traceback.format_exc().splitlines()[-5:],
                        }
                    },
                    skip_scope="ROW"
                )
                issues.append(issue)
                continue
            except DatabaseError as e:
                raise e
            
        # 処理成功時
        issue = Issue.success(
            domain="REGISTER",
            phase="REGISTER.POST_PROCESS",
            message="新規登録しました。",
            context={
                **{"row_index": i + 1},
            },
        )
        issues.append(issue)

        return

