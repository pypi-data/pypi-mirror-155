from p360_export.query.BaseQueryBuilder import BaseQueryBuilder


class ListBasedQueryBuilder(BaseQueryBuilder):
    def _build_select_part(self, config: dict) -> str:
        column_list = config.get("params", {}).get("export_columns")

        if not column_list:
            raise Exception("Cannot export an empty subset of attributes.")

        columns = ", ".join(column_list)

        return f"SELECT {columns} FROM {self._table_identifier}"
