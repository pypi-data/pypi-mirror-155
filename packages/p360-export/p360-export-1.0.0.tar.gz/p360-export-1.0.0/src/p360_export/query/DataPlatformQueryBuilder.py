from p360_export.query.ListBasedQueryBuilder import ListBasedQueryBuilder


class DataPlatformQueryBuilder(ListBasedQueryBuilder):
    @property
    def export_destination(self):
        return "dataplatform"
