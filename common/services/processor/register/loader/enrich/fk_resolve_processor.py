from typing import *
from pandas.core.frame import DataFrame
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models

from common.exceptions.register_errors import (
    FkResolveDefIncompleteError,
    FkResolveLookupFieldsMismatchError,
    FkResolveFailedCreateLookupKwargsError,
)
from common.issue.models import Issue

from common.services.domain.register.dto import FkResolveSpec
from common.services.domain.register.dataframe.resolve_fk.check_def import CheckDef
from common.services.domain.register.dataframe.resolve_fk.build import Build
from common.services.infra.model_registry import ModelRegistry, ModelRegistryError
from common.services.infra.persistance.django_model_persister import ModelPersister


class FkResolveProcessor:

    def __init__(self, model_registry: ModelRegistry, persister: ModelPersister):
        """
        初期化

        :param model_registry: モデルクラス解決レジストリ
        :param persister: モデル汎用永続化契約クラス
        """
        self._model_registry: ModelRegistry = model_registry
        self._persister: ModelPersister = persister

    def resolve_foreign_keys(
        self, df: DataFrame, fk_specs: List[FkResolveSpec], issues: List[Issue]
    ) -> DataFrame:
        """
        DataFrame内のFK項目を、定義に基づいて主キーIDに変換。<br>
        モデル側の検索キー（lookup_keys）とDFの入力列（input_lookup_fields）の対応付き。

        :param df: Model側のカラム名へ変換済みのDataframe
        :type df: DataFrame
        :param fk_specs: FK変換定義DTOリスト
        :type fk_specs: List[FkResolveSpec]
        :param issues: 発生事象リスト
        :type issues: List[Issue]
        :return: 変換後DataFrame
        :rtype: DataFrame
        """
        df_resolved: DataFrame = df.copy()

        # INPUTデータ定義のカラム数分（＝DataFrame列分）繰り返す
        for i, fk_spec in enumerate(fk_specs):

            # FK変換が必要ない場合スキップ
            if not fk_spec.is_fk_flag:
                continue

            # 定義情報の不備チェック
            try:
                CheckDef.check(fk_spec)

            except (
                FkResolveDefIncompleteError,
                FkResolveLookupFieldsMismatchError,
            ) as e:

                issues.append(e.to_issue())
                continue

            try:
                # FK変換先カラムを持つModelクラスを返す
                target_model: models.Model = self._model_registry.resolve(
                    fk_spec.fk_target_model
                )

            except ModelRegistryError as e:
                issue = Issue.error(
                    phase="REGISTER.FK_RESOLVE",
                    code="REGISTER.MODEL_CLASS_NOT_FOUND",
                    message="入力データ定義が指定するモデルクラスが存在しません。",
                    context={
                        "input_id": fk_spec.input_id,
                        "column_order": fk_spec.column_order,
                        "fk_target_model": fk_spec.fk_target_model,
                    },
                    skip_scope="ALL",
                )
                issues.append(issue)
                # Modelが見つからない場合は処理中断
                continue

            # DataFrameの行数分繰り返す
            for i, row in df_resolved.iterrows():

                # FK変換先カラムを持つModelの検索条件一覧を作成
                row_dict: Dict[Any, Any] = row.to_dict()

                try:
                    lookup_kwargs: Dict[Any, Any] = Build.build_lookup_kwargs(
                        row_dict, fk_spec
                    )

                except FkResolveFailedCreateLookupKwargsError as e:
                    # 検索条件を作成失敗した場合はFK未解決として行スキップ
                    issues.append(e.to_issue())
                    df_resolved.at[i, fk_spec.model_target_field_name] = None
                    continue

                row_context = {
                    "input_id": fk_spec.input_id,
                    "column_order": fk_spec.column_order,
                    "fk_target_model": fk_spec.fk_target_model,
                }

                try:
                    # FK変換先インスタンスを取得
                    fk_model_instance = self._persister.get(
                        target_model, **lookup_kwargs
                    )

                except ObjectDoesNotExist:
                    issue = Issue.error(
                        phase="REGISTER.FK_RESOLVE",
                        code="REGISTER.MODEL_DATA_NOT_FOUND",
                        row_index=i + 1,
                        message="入力データ定義が指定するモデル・検索条件に一致するレコードが存在しません",
                        context=dict(**row_context, **row_dict),
                        skip_scope="ROW",
                    )

                    issues.append(issue)
                    df_resolved.at[i, fk_spec.model_target_field_name] = None
                    continue

                except MultipleObjectsReturned:
                    issue = Issue.error(
                        phase="REGISTER.FK_RESOLVE",
                        code="REGISTER.AMBIGUOUS",
                        row_index=i + 1,
                        message="入力データ定義が指定するモデル・検索条件に合致するデータが複数件存在します。（検索キーまたはデータ不正）",
                        context=dict(**row_context, **row_dict),
                        skip_scope="ROW",
                    )

                    issues.append(issue)
                    df_resolved.at[i, fk_spec.model_target_field_name] = None
                    continue

                # ★FKへの変換実施★
                df_resolved.at[i, fk_spec.model_target_field_name] = getattr(
                    fk_model_instance, fk_spec.fk_target_field
                )

                issue = Issue.success(
                    domain="REGISTER",
                    phase="REGISTER.FK_RESOLVE",
                    row_index=i + 1,
                    context=dict(**row_context, **row_dict),
                )
                issues.append(issue)

        # 不要列をdrop（is_lookup_only列）
        drop_cols = [
            fk_spec.model_target_field_name
            for fk_spec in fk_specs
            if fk_spec.is_lookup_only
            and fk_spec.model_target_field_name in df_resolved.columns
        ]
        df_resolved.drop(columns=drop_cols, inplace=True)

        print("---------FK解決後DataFrame-----------")
        print(df_resolved.head())
        print("-------------------------------------")

        return df_resolved
