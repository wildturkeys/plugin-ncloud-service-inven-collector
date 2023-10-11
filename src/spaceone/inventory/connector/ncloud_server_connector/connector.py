import logging
import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException
from typing import Optional
from spaceone.inventory.connector.ncloud_server_connector.schema.data import Server, NCloudServer, NCloudBlock, NCloudNetworkInterface
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
                self._convert_cloud_service_response(self.list_server_instances(region_no=region.get('region_no'))))

        return resources

    def list_server_instances(self, **kwargs) -> Iterator:

        try:

            response = self.api_client_v2.get_server_instance_list(ncloud_server.GetServerInstanceListRequest(**kwargs))
            response_dict = response.to_dict()

            if response_dict.get("server_instance_list"):

                _block_storages: List[Optional[NCloudBlock]] = self._list_block_storage_instance()
                _network_interface: List[Optional[NCloudNetworkInterface]] = self._list_block_storage_instance()

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

                    if hasattr(server, "server_instance_no"):
                        server.disks = self._find_objs_by_key_value(_block_storages,
                                                                    'server_instance_no', server.server_instance_no)

                        server.nics = self._find_objs_by_key_value(_network_interface,
                                                                    'server_instance_no', server.server_instance_no)
                    yield server


        except ApiException as e:
            logging.error(e)
            raise



    def _list_block_storage_instance(self, **kwargs) -> List:

        try:

            block_storage_list = []

            response = self.api_client_v2.get_block_storage_instance_list(
                ncloud_server.GetBlockStorageInstanceListRequest(**kwargs)
            )
            response_dict = response.to_dict()

            if response_dict.get("block_storage_instance_list"):

                for block_storage_instance in response_dict.get("block_storage_instance_list"):

                    block_storage = self._create_model_obj(NCloudBlock, block_storage_instance)

                    region = block_storage_instance.get("region")

                    if region.get("region_code"):
                        block_storage.region_code = region.get("region_code")

                    block_storage_list.append(block_storage)

            return block_storage_list

        except ApiException as e:
            logging.error(e)
            raise


    def _list_network_iterface(self, **kwargs) -> List:

        try:

            network_iterface_list = []

            response = self.api_client_v2.get_network_interface_list(
                ncloud_server.GetNetworkInterfaceListRequest(**kwargs)
            )
            response_dict = response.to_dict()

            if response_dict.get("block_storage_instance_list"):

                for network_interface in response_dict.get("network_interface_list"):

                    network_interface_obj = self._create_model_obj(NCloudNetworkInterface, network_interface)

                    network_iterface_list.append(network_interface_obj)

            return network_iterface_list

        except ApiException as e:
            logging.error(e)
            raise
