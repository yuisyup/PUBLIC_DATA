from typing import List
from common.models import MsInputPreprocessDef

class InputPreprocessDefinitionRepository:
    def list_enabled_by_input_id(self, input_id: str) -> List[MsInputPreprocessDef]:
        return list(
            MsInputPreprocessDef.objects
            .filter(input_id=input_id, is_enabled=True)
            .order_by("seq")
        )
