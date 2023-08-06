from abc import ABC, abstractmethod
from typing import Tuple


class QueryBuilderInterface(ABC):
    @property
    @abstractmethod
    def export_destination(self):
        pass

    @abstractmethod
    def build(self, config: dict) -> Tuple[str, str]:
        pass

    @abstractmethod
    def _build_select_part(self, config: dict) -> str:
        pass
