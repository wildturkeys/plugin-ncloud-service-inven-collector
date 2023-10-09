import logging
import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException
from spaceone.inventory.connector.ncloud_server_connector.schema.data import Server, NCloudServer
from spaceone.inventory.connector.ncloud_server_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_server_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse

from typing import Iterator, List

_LOGGER = logging.getLogger(__name__)

INSTANCE_STATE_MAP = {
    "init": "RUNNING",
    "creating": "RUNNING",
    "booting": "RUNNING",
    "setting up": "RUNNING",
    "running": "RUNNING",
    "rebooting": "RUNNING",
    "hard rebooting": "RUNNING",
    "shutting down": "STOPPING",
    "hard shutting down": "STOPPING",
    "terminating": "SHUTTING-DOWN",
    "changingSpec": "PENDING",
    "copying": "PENDING",
    "repairing": "PENDING",
    "stopped": "STOPPED"
}


class ServerConnector(NCloudBaseConnector):
    cloud_service_group = 'Compute'
    cloud_service_type = 'Server'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_server
    _ncloud_api_v2 = V2Api

    def get_resources(self) -> List[CloudServiceResponse]:

        resources = []

        resources.extend(self.cloud_service_types)

        for region in self.regions:
            resources.extend(
                self._convert_cloud_service_response(self.list_instances(region_no=region.get('region_no'))))

        return resources

    def list_instances(self, **kwargs) -> Iterator:

        try:

            response = self.api_client_v2.get_server_instance_list(ncloud_server.GetServerInstanceListRequest(**kwargs))
            response_dict = response.to_dict()

            if response_dict.get("server_instance_list"):

                for server_instance in response_dict.get("server_instance_list"):

                    server = Server(self._create_model_obj(NCloudServer, server_instance))

                    region = server_instance.get("region")

                    if region.get("region_code"):
                        server.region_code = region.get("region_code")

                    server.hardware = {
                        'core': server.cpu_count,
                        'memory': round(server.memory_size / 1024 / 1024 / 1024)
                    }

                    server.compute = {
                        'az': server.zone.get('zone_code'),
                        'instance_state': INSTANCE_STATE_MAP.get(server.server_instance_status_name),
                        'instance_id': server.server_instance_no
                    }

                    server.os = {
                        'os_distro': server.platform_type.get('code_name'),
                    }

                    server.primary_ip_address = server.private_ip

                    yield server


        except ApiException as e:
            logging.error(e)
            raise
