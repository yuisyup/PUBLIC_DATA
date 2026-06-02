from typing import List

from common.services.domain.run_result_reference.dto import (
    RunResultReferenceCriteria,
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
