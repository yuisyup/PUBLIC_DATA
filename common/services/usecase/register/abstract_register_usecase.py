from abc import ABC, abstractmethod
from typing import *

from common.services.domain.register.dto import InputDefSpec, FkResolveSpec


class AbstractRegisterUsecase(ABC):

    def __init__(self, def_spec: InputDefSpec, col_specs: List[FkResolveSpec]):
        """
        初期化

        :param def_spec: INPUT定義マスタDTO
        :param col_specs: INPUT定義カラムマスタDTOリスト
        """
        self._def_spec: InputDefSpec = def_spec
        self._col_specs: List[FkResolveSpec] = col_specs
