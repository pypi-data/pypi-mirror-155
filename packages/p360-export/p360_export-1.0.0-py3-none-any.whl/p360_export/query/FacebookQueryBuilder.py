from p360_export.query.MappingBasedQueryBuilder import MappingBasedQueryBuilder


class FacebookQueryBuilder(MappingBasedQueryBuilder):
    @property
    def export_destination(self):
        return "facebook"
