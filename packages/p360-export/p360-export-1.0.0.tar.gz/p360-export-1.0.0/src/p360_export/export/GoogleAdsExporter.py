from typing import List, Sequence
from pyspark.sql import DataFrame
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v10.common.types.offline_user_data import UserIdentifier
from p360_export.export.ExporterInterface import ExporterInterface
from p360_export.export.ExporterUtils import ExporterUtils
from p360_export.utils.ColumnHasher import ColumnHasher
from p360_export.utils.SecretGetterInterface import SecretGetterInterface


class GoogleAdsExporter(ExporterInterface):
    def __init__(
        self,
        secret_getter: SecretGetterInterface,
        developer_token_key: str,
        refresh_token_key: str,
        client_id_key: str,
        client_secret_key: str,
        customer_id: str,
    ):
        self.__customer_id = customer_id
        self.__keys = {
            "developer_token_key": developer_token_key,
            "refresh_token_key": refresh_token_key,
            "client_id_key": client_id_key,
            "client_secret_key": client_secret_key,
        }
        self.__secret_getter = secret_getter
        self.__client = None

    @property
    def export_destination(self):
        return "google_ads"

    def _init_client(self):
        credentials = {
            "developer_token": self.__secret_getter.get(key=self.__keys["developer_token_key"]),
            "refresh_token": self.__secret_getter.get(key=self.__keys["refresh_token_key"]),
            "client_id": self.__secret_getter.get(key=self.__keys["client_id_key"]),
            "client_secret": self.__secret_getter.get(key=self.__keys["client_secret_key"]),
            "use_proto_plus": True,
        }
        self.__client = GoogleAdsClient.load_from_dict(credentials)

    def _get_existing_user_lists(self):
        request = self.__client.get_type("SearchGoogleAdsRequest")
        request.customer_id = self.__customer_id
        request.query = "SELECT user_list.id, user_list.name FROM user_list"
        request.page_size = 10000

        ga_service = self.__client.get_service("GoogleAdsService")
        response = ga_service.search(request=request)
        return response.results

    def _create_user_list(self, user_list_name: str):
        user_list_service = self.__client.get_service("UserListService")
        user_list_operation = self.__client.get_type("UserListOperation")

        user_list = user_list_operation.create
        user_list.name = user_list_name
        user_list.crm_based_user_list.upload_key_type = self.__client.enums.CustomerMatchUploadKeyTypeEnum.CONTACT_INFO
        user_list.membership_life_span = 10

        response = user_list_service.mutate_user_lists(customer_id=self.__customer_id, operations=[user_list_operation])
        return response.results[0].resource_name

    def _get_user_list_resource_name(self, user_list_name: str):
        for user_list in self._get_existing_user_lists():
            if user_list.user_list.name == user_list_name:
                return user_list.user_list.resource_name
        user_list_resource_name = self._create_user_list(user_list_name=user_list_name)
        return user_list_resource_name

    def _prepare_user_data_job_operation(self, hashed_emails: Sequence[str]):
        user_ids = self._prepare_user_ids(hashed_emails)

        user_data_job_operation = self.__client.get_type("OfflineUserDataJobOperation")
        user_data_job_operation.remove_all = True
        user_data_job_operation.create.user_identifiers.extend(user_ids)
        return user_data_job_operation

    def _prepare_user_ids(self, hashed_emails: Sequence[str]) -> List[UserIdentifier]:
        user_ids = []
        for hashed_email in hashed_emails:
            user_id = self.__client.get_type("UserIdentifier")
            user_id.hashed_email = hashed_email
            user_ids.append(user_id)

        return user_ids

    def _prepare_user_data_job(self, user_data_service, user_list_resource_name: str) -> str:
        user_data_job = self.__client.get_type("OfflineUserDataJob")
        user_data_job.type_ = self.__client.enums.OfflineUserDataJobTypeEnum.CUSTOMER_MATCH_USER_LIST
        user_data_job.customer_match_user_list_metadata.user_list = user_list_resource_name
        response = user_data_service.create_offline_user_data_job(customer_id=self.__customer_id, job=user_data_job)
        return response.resource_name

    def _add_users_to_user_list(self, user_list_resource_name: str, hashed_emails: Sequence[str]):
        user_data_service = self.__client.get_service("OfflineUserDataJobService")
        user_data_job_resource_name = self._prepare_user_data_job(
            user_data_service=user_data_service, user_list_resource_name=user_list_resource_name
        )

        request = self.__client.get_type("AddOfflineUserDataJobOperationsRequest")
        request.resource_name = user_data_job_resource_name
        request.operations = [self._prepare_user_data_job_operation(hashed_emails)]
        request.enable_partial_failure = False

        user_data_service.add_offline_user_data_job_operations(request=request)
        user_data_service.run_offline_user_data_job(resource_name=user_data_job_resource_name)

    def export(self, df: DataFrame, config: dict):
        ExporterUtils.check_user_variables(self.export_destination, self.__keys)
        self._init_client()
        user_list_name = ExporterUtils.get_custom_name(config)
        hashed_df = ColumnHasher.hash(df=df, columns=df.columns, converter=ColumnHasher.sha256)
        hashed_emails = list(hashed_df.select("email").toPandas()["email"])
        user_list_resource_name = self._get_user_list_resource_name(user_list_name=user_list_name)
        self._add_users_to_user_list(user_list_resource_name, hashed_emails)
