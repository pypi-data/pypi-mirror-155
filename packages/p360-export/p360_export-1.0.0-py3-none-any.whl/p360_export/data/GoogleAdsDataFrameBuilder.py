from pyspark.sql import DataFrame
from p360_export.data.BaseDataFrameBuilder import BaseDataFrameBuilder


class GoogleAdsDataFrameBuilder(BaseDataFrameBuilder):
    @property
    def export_destination(self):
        return "google_ads"

    def build(self, df: DataFrame, query: str, table_identifier: str, config: dict) -> DataFrame:
        df = super().build(df, query, table_identifier, config)

        column_mapping = self.get_column_mapping(config)

        for new_name, old_name in column_mapping.items():
            df = df.withColumnRenamed(old_name, new_name)
        return df
