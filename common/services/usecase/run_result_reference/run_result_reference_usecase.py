from typing import List, Optional

from common.services.domain.run_result_reference.dto import (
    RunResultReferenceCriteria,
    RunResultReferenceDetail,
    RunResultReferenceRow,
)
from common.services.infra.persistance.repositories.run_result_reference.run_result_reference_repository import (
    RunResultReferenceRepository,
)


class RunResultReferenceUsecase:
    def __init__(self, repository: RunResultReferenceRepository = None):
        self.repository = repository or RunResultReferenceRepository()

    def search(
        self, criteria: RunResultReferenceCriteria
    ) -> List[RunResultReferenceRow]:
        return self.repository.search(criteria)

    def get_detail(self, run_id: str) -> Optional[RunResultReferenceDetail]:
        return self.repository.get_detail(run_id)
