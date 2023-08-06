from typing import Dict
from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession

from p360_export.data.DataFrameBuilderInterface import DataFrameBuilderInterface
from p360_export.exceptions.data_frame_builder import EmptyColumnMappingException


class BaseDataFrameBuilder(DataFrameBuilderInterface):
    def __init__(self, spark: SparkSession):
        self._spark = spark

    @staticmethod
    def get_column_mapping(config: dict) -> Dict[str, str]:
        column_mapping = config.get("params", {}).get("mapping", {})
        if not column_mapping:
            raise EmptyColumnMappingException("No column mapping specified. The params.mapping value in the configuration file is empty.")
        return column_mapping

    def build(self, df: DataFrame, query: str, table_identifier: str, config: dict) -> DataFrame:
        df.createOrReplaceTempView(table_identifier)

        return self._spark.sql(query)
