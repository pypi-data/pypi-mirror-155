from p360_export.query.MappingBasedQueryBuilder import MappingBasedQueryBuilder


class SFMCPersonaQueryBuilder(MappingBasedQueryBuilder):
    @property
    def export_destination(self):
        return "sfmc_persona"
