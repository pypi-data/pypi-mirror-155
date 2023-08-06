from pyspark.sql import DataFrame
from p360_export.P360ExportManager import P360ExportManager
from p360_export.config.ConfigGetterInterface import ConfigGetterInterface


class P360ExportRunner:
    def __init__(self, manager: P360ExportManager, config_getter: ConfigGetterInterface):
        self.manager = manager
        self.config_getter = config_getter

    def export(self, df_background: DataFrame, config_id: str):
        config = self.config_getter.get(config_id=config_id)
        self.manager.set_export_destination(config)
        query, table_identifier = self.manager.query_builder.build(config=config)
        df = self.manager.data_frame_builder.build(df=df_background, query=query, table_identifier=table_identifier, config=config)
        self.manager.exporter.export(df=df, config=config)
