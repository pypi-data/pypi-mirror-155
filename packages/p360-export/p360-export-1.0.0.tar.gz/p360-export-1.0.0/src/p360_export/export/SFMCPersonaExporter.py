import paramiko
import os

from FuelSDK.rest import ET_Constructor
from FuelSDK import ET_Client, ET_DataExtension, ET_Post, ET_Get
from pyspark.sql import DataFrame
from p360_export.exceptions.exporter import UnableToCreateDataExtension, UnableToCreateImportDefinition
from p360_export.export.ExporterUtils import ExporterUtils
from p360_export.export.ExporterInterface import ExporterInterface
from p360_export.utils.SecretGetterInterface import SecretGetterInterface


class SFMCPersonaExporter(ExporterInterface):
    def __init__(
        self,
        secret_getter: SecretGetterInterface,
        client_secret_key: str,
        ftp_password_key: str,
        client_id: str,
        ftp_username: str,
        tenant_url: str,
        account_id: str,
        file_location: str,
    ):
        self.__secret_getter = secret_getter
        self.__variables = {
            "client_secret_key": client_secret_key,
            "ftp_password_key": ftp_password_key,
            "tenant_url": tenant_url,
            "client_id": client_id,
            "ftp_username": ftp_username,
            "file_location": file_location,
            "account_id": account_id,
        }
        self.__client = None
        self.__audience_name = None

    @property
    def export_destination(self):
        return "sfmc_persona"

    @property
    def csv_path(self):
        return f"/dbfs/tmp/{self.__audience_name}.csv"

    @staticmethod
    def check_response(response: ET_Constructor, exporter_exception):
        if response.results[0]["StatusCode"] == "Error":
            raise exporter_exception(str(response.results))

    def _configure_export(self, config: dict):
        ExporterUtils.check_user_variables(self.export_destination, self.__variables)
        client_config = {
            "clientid": self.__variables["client_id"],
            "clientsecret": self.__secret_getter.get(key=self.__variables["client_secret_key"]),
            "authenticationurl": f"https://{self.__variables['tenant_url']}.auth.marketingcloudapis.com/",
            "useOAuth2Authentication": "True",
            "accountId": self.__variables["account_id"],
            "scope": "data_extensions_read data_extensions_write automations_write automations_read",
            "applicationType": "server",
        }
        self.__client = ET_Client(params=client_config)
        self.__audience_name = ExporterUtils.get_custom_name(config)

    def _upload_csv(self):
        host = f"{self.__variables['tenant_url']}.ftp.marketingcloudops.com"
        username = self.__variables["ftp_username"]
        password = self.__secret_getter.get(key=self.__variables["ftp_password_key"])

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        sftp = ssh.open_sftp()
        sftp.put(self.csv_path, f"/Import/{self.__audience_name}.csv")
        sftp.close()
        os.remove(self.csv_path)

    def _create_data_extension(self) -> str:
        data_extension = ET_DataExtension()
        data_extension.auth_stub = self.__client
        data_extension.props = {"Name": self.__audience_name}
        data_extension.columns = [{"Name": "email", "FieldType": "Text", "IsPrimaryKey": "true", "MaxLength": "100", "IsRequired": "true"}]

        response = data_extension.post()
        self.check_response(response=response, exporter_exception=UnableToCreateDataExtension)

        return response.results[0]["NewObjectID"]

    def _get_data_extension_id(self) -> str:
        data_extension = ET_DataExtension()
        data_extension.auth_stub = self.__client
        data_extension.props = ["ObjectID"]
        data_extension.search_filter = {"Property": "Name", "SimpleOperator": "equals", "Value": self.__audience_name}

        response = data_extension.get()
        if response.results:
            return response.results[0]["ObjectID"]

        return self._create_data_extension()

    def _create_import_definition(self, data_extension_id: str) -> str:
        props = {
            "Name": self.__audience_name,
            "DestinationObject": {"ObjectID": data_extension_id},
            "RetrieveFileTransferLocation": {"CustomerKey": self.__variables["file_location"]},
            "AllowErrors": True,
            "UpdateType": "Overwrite",
            "FileSpec": f"{self.__audience_name}.csv",
            "FileType": "CSV",
            "FieldMappingType": "InferFromColumnHeadings",
        }

        response = ET_Post(auth_stub=self.__client, obj_type="ImportDefinition", props=props)
        self.check_response(response=response, exporter_exception=UnableToCreateImportDefinition)

        return response.results[0]["NewObjectID"]

    def _get_import_definition_id(self, data_extension_id: str) -> str:
        props = ["ObjectID"]
        search_filter = {"Property": "Name", "SimpleOperator": "equals", "Value": self.__audience_name}

        response = ET_Get(auth_stub=self.__client, obj_type="ImportDefinition", props=props, search_filter=search_filter)
        if response.results:
            return response.results[0]["ObjectID"]

        return self._create_import_definition(data_extension_id=data_extension_id)

    def _run_import_definition(self, import_definition_id: str):
        request = self.__client.soap_client.factory.create("PerformRequestMsg")
        definition = self.__client.soap_client.factory.create("ImportDefinition")
        definition.ObjectID = import_definition_id
        request.Definitions.Definition = definition
        request.Action = "start"
        self.__client.soap_client.service.Perform(None, request)

    def export(self, df: DataFrame, config: dict):
        self._configure_export(config=config)
        df.toPandas().to_csv(self.csv_path)  # pyre-ignore[16]
        self._upload_csv()
        data_extension_id = self._get_data_extension_id()
        import_definition_id = self._get_import_definition_id(data_extension_id=data_extension_id)
        self._run_import_definition(import_definition_id=import_definition_id)
