from p360_export.query.MappingBasedQueryBuilder import MappingBasedQueryBuilder


class GoogleAdsQueryBuilder(MappingBasedQueryBuilder):
    @property
    def export_destination(self):
        return "google_ads"
