from typing import *

from common.exceptions.app_error import PreprocessRegistryError
from common.services.domain.register.preprocess.preprocess_pipeline import PreprocessPipeline
from common.services.infra.persistance.repositories.input_preprocess_definition_repository import (
    InputPreprocessDefinitionRepository
)
from common.services.infra.preprocess_registry import PreprocessRegistry
from common.issue.models import Issue


class PreprocessPipelineFactory:
    def __init__(
        self,
        repo: InputPreprocessDefinitionRepository,
        registry: PreprocessRegistry,
    ):
        self._repo = repo
        self._registry = registry

    def build(self, input_id: str, issues: List[Issue]) -> PreprocessPipeline:
        defs = self._repo.list_enabled_by_input_id(input_id=input_id)

        processors = []
        for d in defs:
            try:
                cls = self._registry.resolve(d.preprocess_key)
            except PreprocessRegistryError:
                issues.append(Issue.error(
                    phase="REGISTER.PREPROCESS",
                    code="REGISTER.PREPROCESS_KEY_NOT_FOUND",
                    message="前処理定義のキーがRegistryに存在しません。",
                    context={"input_id": input_id, "preprocess_key": d.preprocess_key, "seq": d.seq},
                    skip_scope="ALL"
                    )
                )
                # ここは好み：FATALにして止めてもいい。今回はERRORで止める前提に合わせる。
                continue

            # params_json の適用は後回しでOK（必要になったらここで d.params_json を渡す）
            processors.append(cls())

        return PreprocessPipeline(processors=processors)
