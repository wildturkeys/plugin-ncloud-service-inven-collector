import logging
import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException

from typing import Optional, Type
from spaceone.inventory.connector.ncloud_server_connector.schema.data import Server, NCloudServer, NCloudBlock, \
    NCloudNetworkInterface, NCloudAccessControlGroup, NCloudAccessControlRule, NCloudAccessControlGroupServerInstance

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._access_control_rules_dict = {}

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        resources.extend(self.cloud_service_types)

        for region in self.regions:
            resources.extend(
                self._convert_cloud_service_response(self.list_server_instances(NCloudServer,
                                                                                Server,
                                                                                region_no=region.get('region_no'))))

        return resources

    def list_server_instances(self, ncloud_server_cls: Type[NCloudServer],
                              response_server_cls: Type[Server], **kwargs) -> Iterator:

        try:

            response = self.api_client_v2.get_server_instance_list(
                self._ncloud_cls.GetServerInstanceListRequest(**kwargs))
            response_dict = response.to_dict()

            if response_dict.get("server_instance_list"):

                _block_storages: List[Optional[NCloudBlock]] = self._list_block_storage_instance(**kwargs)
                _network_interface: List[Optional[NCloudNetworkInterface]] = self._list_network_interface(**kwargs)

                _instance_access_control_rules = self._sort_access_control_group_rule_group_by_instance_no()

                for server_instance in response_dict.get("server_instance_list"):

                    server = response_server_cls(self._create_model_obj(ncloud_server_cls, server_instance))
                    region = server_instance.get("region")

                    if region and region.get("region_code"):
                        server.region_code = region.get("region_code")
                    elif server_instance.get("region_code"):
                        server.region_code = server_instance.get("region_code")

                    server.hardware = {
                        'core': server.cpu_count,
                        'memory': round(server.memory_size / 1024 / 1024 / 1024)
                    }

                    zone_code = None

                    if server.zone and server.zone.get('zone_code'):
                        zone_code = server.zone.get('zone_code')
                    elif server.zone_code:
                        zone_code = server.zone_code

                    server.compute = {
                        'az': zone_code,
                        'instance_state': INSTANCE_STATE_MAP.get(server.server_instance_status_name),
                        'instance_id': server.server_instance_no
                    }

                    server.os = {'os_distro': server.platform_type.get('code_name')}

                    server.primary_ip_address = server.private_ip

                    if hasattr(server, "server_instance_no"):
                        server.disks = self._find_objs_by_key_value(_block_storages,
                                                                    'server_instance_no', server.server_instance_no)
                        server.nics = self._find_objs_by_key_value(_network_interface,
                                                                   'server_instance_no', server.server_instance_no)

                        if _instance_access_control_rules and \
                                _instance_access_control_rules.get(server.server_instance_no):
                            server.security_groups = _instance_access_control_rules.get(server.server_instance_no)

                    yield server

        except ApiException as e:
            logging.error(e)
            raise
        except Exception as e:
            import traceback
            logging.error(traceback.format_exc())
            logging.error(e)
            raise

    def _list_block_storage_instance(self, **kwargs) -> List[Type[NCloudBlock]]:

        return self._list_ncloud_resources(self.api_client_v2.get_block_storage_instance_list,
                                           self._ncloud_cls.GetBlockStorageInstanceListRequest,
                                           "block_storage_instance_list",
                                           NCloudBlock,
                                           **kwargs)

    def _list_network_interface(self, **kwargs) -> List[NCloudNetworkInterface]:

        return self._list_ncloud_resources(self.api_client_v2.get_network_interface_list,
                                           self._ncloud_cls.GetNetworkInterfaceListRequest,
                                           "network_interface_list",
                                           NCloudNetworkInterface,
                                           **kwargs)

    def _list_access_control_group(self) -> List[NCloudAccessControlGroup]:

        return self._list_ncloud_resources(self.api_client_v2.get_access_control_group_list,
                                           self._ncloud_cls.GetAccessControlGroupListRequest,
                                           "access_control_group_list",
                                           NCloudAccessControlGroup)

    def _list_access_control_rule(self, access_control_group_configuration_no: str) -> List[NCloudAccessControlRule]:

        return self._list_ncloud_resources(self.api_client_v2.get_access_control_rule_list,
                                           self._ncloud_cls.GetAccessControlRuleListRequest,
                                           "access_control_rule_list",
                                           NCloudAccessControlRule,
                                           access_control_group_configuration_no=access_control_group_configuration_no)

    def _list_access_control_group_server(self, access_control_group_configuration_no: str) \
            -> List[NCloudAccessControlGroupServerInstance]:

        return self._list_ncloud_resources(self.api_client_v2.get_access_control_group_server_instance_list,
                                           self._ncloud_cls.GetAccessControlGroupServerInstanceListRequest,
                                           "server_instance_list",
                                           NCloudAccessControlGroupServerInstance,
                                           access_control_group_configuration_no=access_control_group_configuration_no)

    def _sort_access_control_group_rule_group_by_instance_no(self):

        _access_control_groups = self._list_access_control_group()

        for access_control_group in _access_control_groups:
            acg_no = access_control_group.access_control_group_configuration_no

            self._access_control_rules_dict[acg_no] = []
            acg_name = access_control_group.access_control_group_name

            access_control_rules = self._list_access_control_rule(
                access_control_group_configuration_no=acg_no)

            for access_control_rule in access_control_rules:
                access_control_rule.access_control_group_name = acg_name
                self._access_control_rules_dict[acg_no].append(access_control_rule)

        return self._get_access_control_group_rule_server_by_server_instance_no()

    def _get_access_control_group_rule_server_by_server_instance_no(self):

        access_control_group_rule_server_dict = {}

        for acg_no in self._access_control_rules_dict.keys():

            access_control_group_servers = self._list_access_control_group_server(
                access_control_group_configuration_no=acg_no)

            for access_control_group_server in access_control_group_servers:

                if access_control_group_server.get("server_instance_no"):

                    server_instance_no = access_control_group_server.get("server_instance_no")
                    access_control_group_rule_server_dict[server_instance_no] = \
                        self._get_access_control_group_rules_by_server_no(access_control_group_server, acg_no)

        return access_control_group_rule_server_dict

    def _get_access_control_group_rules_by_server_no(self, access_control_group_server, acg_no):

        rtn_list = []

        access_control_group_list = access_control_group_server.access_control_group_list

        for access_control_group in access_control_group_list:

            if access_control_group.get("access_control_group_configuration_no") and \
                    acg_no in self._access_control_rules_dict.keys():

                rtn_list.extend(self._access_control_rules_dict[acg_no])

        return rtn_list
