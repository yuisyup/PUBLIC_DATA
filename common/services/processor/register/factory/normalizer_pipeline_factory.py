from typing import *

from common.exceptions.app_error import NormalizerRegistryError
from common.services.processor.register.normalizer.normalizer_pipeline import (
    NormalizerPipeline,
)
from common.services.infra.persistance.repositories.input_normalizer_step_definition_repository import (
    InputNormalizerStepDefinitionRepository,
)
from common.services.processor.register.factory.normilizer_step_registry import (
    NormalizerStepRegistry,
)
from common.issue.models import Issue


class NormalizerPipelineFactory:
    def __init__(
        self,
        repo: InputNormalizerStepDefinitionRepository,
        step_registry: NormalizerStepRegistry,
    ):
        self._repo = repo
        self._step_registry = step_registry

    def build(self, input_id: str, issues: List[Issue]) -> NormalizerPipeline:
        defs = self._repo.list_enabled_by_input_id(input_id=input_id)

        processors = []
        for d in defs:
            try:
                cls = self._step_registry.resolve(d.normalizer_step_key)
            except NormalizerRegistryError:
                issues.append(
                    Issue.error(
                        phase="REGISTER.NORMALIZE",
                        code="REGISTER.NORMALIZE_KEY_NOT_FOUND",
                        message="前処理定義のキーがRegistryに存在しません。",
                        context={
                            "input_id": input_id,
                            "normalizer_step_key": d.normalizer_step_key,
                            "seq": d.seq,
                        },
                        skip_scope="ALL",
                    )
                )
                # ここは好み：FATALにして止めてもいい。今回はERRORで止める前提に合わせる。
                continue

            # params_json の適用は後回しでOK（必要になったらここで d.params_json を渡す）
            processors.append(cls())

        return NormalizerPipeline(processors=processors)
