import logging
import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException
from spaceone.inventory.connector.ncloud_server_connector.schema.data import Server
from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_server_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse, CloudServiceResource
from typing import Iterator, List

_LOGGER = logging.getLogger(__name__)


class ServerConnector(NCloudBaseConnector):

    cloud_service_group = 'Compute'
    cloud_service_type = 'Server'
    cloud_service_types = CLOUD_SERVICE_TYPES

    _ncloud_cls = ncloud_server
    _ncloud_api_v2 = V2Api

    def get_resources(self) -> List[CloudServiceResponse]:

        resources = []
        resources.extend(self.cloud_service_types)
        resources.extend(self._convert_cloud_service_response(self.list_instances()))

        return resources

    def list_instances(self) -> Iterator:

        try:

            response = self.api_client_v2.get_server_instance_list(ncloud_server.GetServerInstanceListRequest())
            response_dict = response.to_dict()

            if response_dict.get("server_instance_list"):

                for server_instance in response_dict.get("server_instance_list"):
                    region_code = server_instance.get("region").get("region_code")

                    server = Server(self._create_model_obj(Server, server_instance))
                    server.region_code = region_code

                    yield server


        except ApiException as e:
            logging.error(e)
            raise
