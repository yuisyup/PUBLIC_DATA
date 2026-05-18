import traceback
import pandas as pd
from typing import *
from django.db import models, DatabaseError

from common.exceptions.register_errors import CsvParseError
from common.issue.models import Issue
from common.services.usecase.register.abstract_register_usecase import (
    AbstractRegisterUsecase,
)
from common.services.usecase.register.register_usecase_protocol import (
    RegisterUsecaseProtocol,
)
from common.services.processor.register.extractor.csv_to_dataframe_processor import (
    CsvToDataframeProcessor,
)
from common.services.processor.register.loader.enrich.fk_resolve_processor import (
    FkResolveProcessor,
)
from common.services.processor.register.loader.policy_execute.register_processor_protocol import (
    RegisterProcessorProtocol,
)
from common.services.processor.register.normalizer.normalizer_pipeline import (
    NormalizerPipeline,
)
from common.services.processor.register.factory.policy_processor_factory import (
    PolicyProcessorFactory,
    RegisterPolicyNotFoundError,
)
from common.services.processor.register.factory.normalizer_pipeline_factory import (
    NormalizerPipelineFactory,
)
from common.services.processor.register.factory.normilizer_step_registry import (
    NormalizerStepRegistry,
)
from common.services.infra.persistance.django_model_persister import (
    DjangoModelPersister,
)
from common.services.infra.model_registry import ModelRegistry, ModelRegistryError
from common.services.infra.persistance.repositories.input_normalizer_step_definition_repository import (
    InputNormalizerStepDefinitionRepository,
)


class RegisterFromCsvUsecase(RegisterUsecaseProtocol, AbstractRegisterUsecase):

    @override
    def execute(self, input_source: Any) -> List[Issue]:

        # 発生事象リスト（管理用）
        issues: List[Issue] = []

        # 1. CSVからDataFrameを生成
        try:
            df_mapped: pd.DataFrame = CsvToDataframeProcessor().create_dataframe(
                csv_file=input_source,
                input_def_spec=self._def_spec,
                spec_input_list=self._col_specs,
                issues=issues,
            )

        except CsvParseError as e:
            issues.append(e.to_issue())
            return issues

        # すでに仕様エラー有の場合はissuesを返却し処理終了（FATAL ERROR扱い）
        if any(i.skip_scope == "ALL" for i in issues):
            return issues

        # ★ 1.5 前処理
        try:
            pipeline: NormalizerPipeline = NormalizerPipelineFactory(
                repo=InputNormalizerStepDefinitionRepository(),
                step_registry=NormalizerStepRegistry(),
            ).build(input_id=self._def_spec.input_id, issues=issues)

            df_preprocessed = pipeline.apply(df=df_mapped)

        except Exception as e:
            issues.append(
                Issue.error(
                    phase="REGISTER.NORMALIZE",
                    code="REGISTER.UNEXPECTED_ERROR",
                    message="前処理中に予期しないエラーが発生しました。",
                    context={
                        "input_id": self._def_spec.input_id,
                        "error_message": str(e),
                        "trace": traceback.format_exc().splitlines()[-5:],
                    },
                )
            )
            return issues

        # すでに仕様エラー有の場合はissuesを返却し処理終了（FATAL ERROR扱い）
        if any(i.skip_scope == "ALL" for i in issues):
            return issues

        # 2. DataFrameのFKを解決
        try:
            fk_resolver = FkResolveProcessor(ModelRegistry(), DjangoModelPersister())
            df_resolved: pd.DataFrame = fk_resolver.resolve_foreign_keys(
                df=df_preprocessed, fk_specs=self._col_specs, issues=issues
            )

        except Exception as e:
            issue = Issue.error(
                phase="REGISTER.FK_RESOLVE",
                code="REGISTER.UNEXPECTED_ERROR",
                message="FK解決処理中に予期しないエラーが発生しました。",
                context={
                    "input_id": self._def_spec.input_id,
                    "csv_name": self._def_spec.input_name,
                    "error_message": str(e),
                    "trace": traceback.format_exc().splitlines()[-5:],
                },
            )
            issues.append(issue)
            return issues

        # FK解決にてエラー有の場合は処理終了（登録処理を行わない）
        if any(i.severity == "ERROR" for i in issues):
            return issues

        # 登録ポリシークラスを取得
        try:
            register_policy_processor_instance: (
                RegisterProcessorProtocol
            ) = PolicyProcessorFactory().get_register_processor_by_policy(
                policy_processor_class_path=self._def_spec.policy_processor_class_path,
                persister=DjangoModelPersister(),
            )
        except RegisterPolicyNotFoundError as e:
            issues.append(e.to_issue())
            return issues

        # 登録先Modelクラスを取得
        try:

            model_class: models.Model = ModelRegistry().resolve(
                model_label=self._def_spec.target_model_name
            )

        except ModelRegistryError as e:
            issue = Issue.error(
                phase="REGISTER.GET_TARGET_MODEL_CLASS",
                code="REGISTER.MODEL_CLASS_NOT_FOUND",
                message="登録先Modelクラスの生成に失敗しました。",
                context={
                    "input_id": self._def_spec.input_id,
                    "target_model_name": self._def_spec.target_model_name,
                    "error_message": str(e),
                    "trace": traceback.format_exc().splitlines()[-5:],
                },
            )
            issues.append(issue)
            return issues

        try:
            # 登録処理を実行
            register_policy_processor_instance.execute(
                df=df_resolved,
                model_class=model_class,
                issues=issues,
                lookup_fields=self._def_spec.insert_duplication_lookup_fields,
            )
        except DatabaseError as e:
            issue = Issue.error(
                phase="REGISTER.POST_PROCESS",
                code="REGISTER.DB_ERROR",
                message="登録処理中にデータベースエラーが発生しました。",
                context={
                    "input_id": self._def_spec.input_id,
                    "target_model_name": self._def_spec.target_model_name,
                    "error_message": str(e),
                    "trace": traceback.format_exc().splitlines()[-5:],
                },
            )
            issues.append(issue)
            return issues

        except Exception as e:
            issue = Issue.error(
                phase="REGISTER.POST_PROCESS",
                code="REGISTER.UNEXPECTED_ERROR",
                message="登録処理中に予期せぬエラーが発生しました。",
                context={
                    "input_id": self._def_spec.input_id,
                    "target_model_name": self._def_spec.target_model_name,
                    "error_message": str(e),
                    "trace": traceback.format_exc().splitlines()[-5:],
                },
            )
            issues.append(issue)
            return issues

        # 処理成功時（警告行あり時も含む）
        issue = Issue.success(
            domain="REGISTER",
            phase="REGISTER.FINISH",
        )
        issues.append(issue)

        return issues
