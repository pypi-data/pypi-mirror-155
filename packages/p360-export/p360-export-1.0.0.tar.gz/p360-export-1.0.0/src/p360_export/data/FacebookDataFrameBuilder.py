from pyspark.sql import DataFrame
from p360_export.data.BaseDataFrameBuilder import BaseDataFrameBuilder
from p360_export.exceptions.data_frame_builder import InvalidFacebookColumnException
from p360_export.extra_data.FacebookData import FacebookData


class FacebookDataFrameBuilder(BaseDataFrameBuilder):
    @property
    def export_destination(self):
        return "facebook"

    def build(self, df: DataFrame, query: str, table_identifier: str, config: dict) -> DataFrame:
        column_mapping = self.get_column_mapping(config)

        df.createOrReplaceTempView(table_identifier)

        result_df = self._spark.sql(query)

        for new_name, old_name in column_mapping.items():
            mapped_name = FacebookData.column_map.get(new_name.lower())
            if not mapped_name:
                raise InvalidFacebookColumnException(f"Column {new_name} is not accepted by Facebook API.")
            result_df = result_df.withColumnRenamed(old_name, mapped_name)

        return result_df
