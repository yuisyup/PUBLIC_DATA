from typing import List
from common.models import MsInputNormilizerStepDef


class InputNormalizerStepDefinitionRepository:
    def list_enabled_by_input_id(self, input_id: str) -> List[MsInputNormilizerStepDef]:
        return list(
            MsInputNormilizerStepDef.objects.filter(
                input_id=input_id, is_enabled=True
            ).order_by("seq")
        )
