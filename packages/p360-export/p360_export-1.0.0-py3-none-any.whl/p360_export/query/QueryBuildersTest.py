import unittest
from pysparkbundle.test.PySparkTestCase import PySparkTestCase
from p360_export.query.DataPlatformQueryBuilder import DataPlatformQueryBuilder

from p360_export.query.FacebookQueryBuilder import FacebookQueryBuilder
from p360_export.query.GoogleAdsQueryBuilder import GoogleAdsQueryBuilder

CONFIG = {
    "params": {
        "export_columns": ["list_email_col", "list_gen_col", "list_phone_col"],
        "mapping": {"EMAIL": "map_email_col", "GEN": "map_gen_col", "PHONE": "map_phone_col"},
    },
    "personas": [
        {
            "definition_persona": [
                {
                    "attributes": [
                        {"op": "BETWEEN", "id": "persona_1", "value": [0.0, 14.0]},
                        {"op": "BETWEEN", "id": "persona_2", "value": [0.0, 15.0]},
                    ],
                    "op": "AND",
                }
            ],
        }
    ],
}
EXPECTED_CONDITIONS = "(\npersona_1 BETWEEN 0.0 AND 14.0\nAND\npersona_2 BETWEEN 0.0 AND 15.0\n);"


class QueryBuildersTest(PySparkTestCase):
    @staticmethod
    def expected_mapping_based_query(table_id):
        return f"SELECT map_email_col, map_gen_col, map_phone_col FROM {table_id} WHERE\n" + EXPECTED_CONDITIONS

    @staticmethod
    def expected_list_based_query(table_id):
        return f"SELECT list_email_col, list_gen_col, list_phone_col FROM {table_id} WHERE\n" + EXPECTED_CONDITIONS

    def test_data_platform_query_builder(self):
        query_builder = DataPlatformQueryBuilder()
        query, table_id = query_builder.build(CONFIG)
        assert query == self.expected_list_based_query(table_id)

    def test_facebook_query_builder(self):
        query_builder = FacebookQueryBuilder()
        query, table_id = query_builder.build(CONFIG)
        assert query == self.expected_mapping_based_query(table_id)

    def test_google_ads_query_builder(self):
        query_builder = GoogleAdsQueryBuilder()
        query, table_id = query_builder.build(CONFIG)
        assert query == self.expected_mapping_based_query(table_id)


if __name__ == "__main__":
    unittest.main()
