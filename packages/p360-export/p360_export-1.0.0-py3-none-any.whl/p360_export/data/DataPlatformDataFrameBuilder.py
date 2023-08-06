from p360_export.data.BaseDataFrameBuilder import BaseDataFrameBuilder


class DataPlatformDataFrameBuilder(BaseDataFrameBuilder):
    @property
    def export_destination(self):
        return "dataplatform"
