from abc import ABC, abstractmethod
from pyspark.sql import DataFrame


class DataFrameBuilderInterface(ABC):
    @property
    @abstractmethod
    def export_destination(self):
        pass

    @abstractmethod
    def build(self, df: DataFrame, query: str, table_identifier: str, config: dict) -> DataFrame:
        pass
