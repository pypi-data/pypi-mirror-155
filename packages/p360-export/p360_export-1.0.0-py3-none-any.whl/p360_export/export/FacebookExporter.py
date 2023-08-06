import random
from typing import List
from pyspark.sql import DataFrame
from pandas import DataFrame as pdDataFrame
from p360_export.exceptions.exporter import UnableToReplaceAudience
from p360_export.export.ExporterUtils import ExporterUtils
from p360_export.export.ExporterInterface import ExporterInterface
from p360_export.utils.ColumnHasher import ColumnHasher
from p360_export.utils.SecretGetterInterface import SecretGetterInterface
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.customaudience import CustomAudience

BATCH_SIZE = 10000


class FacebookExporter(ExporterInterface):
    def __init__(self, secret_getter: SecretGetterInterface, access_token_key: str, ad_account_id: str):
        self.__secret_getter = secret_getter
        self.__user_variables = {"access_token_key": access_token_key, "ad_account_id": ad_account_id}
        self.__ad_account = None
        self.__audience_name = None

    @property
    def export_destination(self):
        return "facebook"

    def _second_init(self, config: dict):
        ExporterUtils.check_user_variables(self.export_destination, self.__user_variables)
        self.__ad_account = self._get_ad_account()
        self.__audience_name = ExporterUtils.get_custom_name(config)

    def _get_ad_account(self) -> AdAccount:
        access_token = self.__secret_getter.get(key=self.__user_variables["access_token_key"])
        FacebookAdsApi.init(access_token=access_token)
        return AdAccount(self.__user_variables["ad_account_id"])

    def _create_custom_audience(self) -> CustomAudience:
        params = {"name": self.__audience_name, "subtype": "CUSTOM", "customer_file_source": "USER_PROVIDED_ONLY"}
        return self.__ad_account.create_custom_audience(params=params)

    @staticmethod
    def _check_audience_availability(custom_audience: dict):
        if custom_audience["operation_status"]["code"] != 200:
            raise UnableToReplaceAudience("Unable to replace users, another user replacement is under process")

    def _get_custom_audience(self) -> CustomAudience:
        custom_audiences = self.__ad_account.get_custom_audiences(fields=["name", "operation_status"])
        for custom_audience in custom_audiences:
            if custom_audience["name"] == self.__audience_name:
                self._check_audience_availability(custom_audience=custom_audience)
                return custom_audience
        return self._create_custom_audience()

    @staticmethod
    def _generate_params(df_size, schema) -> dict:
        session_id = random.randint(1, 1000000)
        return {
            "payload": {"schema": schema, "data": []},
            "session": {"session_id": session_id, "batch_seq": 0, "last_batch_flag": False, "estimated_num_total": df_size},
        }

    @staticmethod
    def _update_params(params: dict, batch: List[List[str]], is_last_batch: bool):
        if is_last_batch:
            params["session"]["last_batch_flag"] = True
        params["payload"]["data"] = batch
        params["session"]["batch_seq"] += 1

    def _send_batches(self, df: pdDataFrame, df_size: int, schema: list):
        custom_audience = self._get_custom_audience()
        params = self._generate_params(df_size=df_size, schema=schema)
        for start_idx in range(0, df_size, BATCH_SIZE):
            end_idx = start_idx + BATCH_SIZE
            batch = df[start_idx:end_idx]
            is_last_batch = end_idx >= df_size
            self._update_params(params=params, batch=batch, is_last_batch=is_last_batch)
            custom_audience.create_users_replace(params=params)

    def export(self, df: DataFrame, config: dict):
        self._second_init(config=config)
        schema = df.columns
        df = ColumnHasher.hash(df=df, columns=schema, converter=ColumnHasher.sha256)
        df = df.toPandas().values.tolist()  # pyre-ignore[16]
        self._send_batches(df=df, df_size=len(df), schema=schema)
