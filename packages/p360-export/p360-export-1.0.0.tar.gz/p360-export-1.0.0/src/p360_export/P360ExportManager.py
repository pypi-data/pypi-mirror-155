from typing import List

from p360_export.data.DataFrameBuilderInterface import DataFrameBuilderInterface
from p360_export.exceptions.manager import ExportDestinationNotSetException, InvalidExportDestinationException
from p360_export.export.ExporterInterface import ExporterInterface

from p360_export.query.QueryBuilderInterface import QueryBuilderInterface


class P360ExportManager:
    def __init__(
        self,
        query_builders: List[QueryBuilderInterface],
        data_frame_builders: List[DataFrameBuilderInterface],
        exporters: List[ExporterInterface],
    ):
        self._query_builders = query_builders
        self._data_frame_builders = data_frame_builders
        self._exporters = exporters
        self._export_destination = None

    def set_export_destination(self, config):
        self._export_destination = config.get("destination_type")

    @property
    def query_builder(self):
        return self._select_service(self._query_builders)

    @property
    def data_frame_builder(self):
        return self._select_service(self._data_frame_builders)

    @property
    def exporter(self):
        return self._select_service(self._exporters)

    def _select_service(self, services: List):
        if not self._export_destination:
            raise ExportDestinationNotSetException("Export destination is not set.")

        service = next(filter(lambda service: service.export_destination == self._export_destination, services), None)
        if service:
            return service

        raise InvalidExportDestinationException(f"No service with alias {self._export_destination} found.")
