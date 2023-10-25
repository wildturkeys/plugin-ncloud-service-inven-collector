import logging
import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException

from typing import Optional, Type, Iterable
from spaceone.inventory.connector.ncloud_server_connector.schema.data import Server, NCloudServer, NCloudBlock, \
    NCloudNetworkInterface, NCloudAccessControlGroup, NCloudAccessControlRule, NCloudAccessControlGroupServerInstance, \
    AccessControlRule, Disk, NetworkInterface

from spaceone.inventory.connector.ncloud_server_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_server_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import INSTANCE_STATE_MAP

from typing import Iterator, List

_LOGGER = logging.getLogger(__name__)


class ServerConnector(NCloudBaseConnector):
    cloud_service_group = 'Compute'
    cloud_service_type = 'Server'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_server
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._access_control_rules_dict = {}

    def _set_default_server_info(self, server: Server):

        server.hardware = {
            'core': server.cpu_count,
            'memory': round(server.memory_size / 1024 / 1024 / 1024)
        }

        server.compute = {
            'az': None,
            'instance_state': INSTANCE_STATE_MAP.get(server.server_instance_status_name),
            'instance_id': server.server_instance_no
        }

        server.os = {'os_distro': server.platform_type.get('code_name')}
        server.primary_ip_address = server.private_ip

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

        response = self.api_client_v2.get_server_instance_list(
            self._ncloud_cls.GetServerInstanceListRequest(**kwargs))
        response_dict = response.to_dict()

        if response_dict.get("server_instance_list"):

            _block_storages: List[Optional[Disk]] = self._convert_disk(self._list_block_storage_instance(**kwargs))
            _network_interfaces: List[Optional[NetworkInterface]] = \
                self._convert_network_interfaces(self._list_network_interface(**kwargs))

            _instance_access_control_rules = self._sort_access_control_group_rule_group_by_instance_no()

            for server_instance in response_dict.get("server_instance_list"):

                server = response_server_cls(self._create_model_obj(ncloud_server_cls, server_instance))
                region = server_instance.get("region")

                if region and region.get("region_code"):
                    server.region_code = region.get("region_code")
                elif server_instance.get("region_code"):
                    server.region_code = server_instance.get("region_code")

                self._set_default_server_info(server)

                if server_instance.get("zone") and server_instance.get("zone").get('zone_code'):
                    server.zone_code = server_instance.get("zone").get('zone_code')
                    server.compute['az'] = server_instance.get("zone").get('zone_code')

                if hasattr(server, "server_instance_no"):
                    server.disks = self._find_objs_by_key_value(_block_storages,
                                                                'server_instance_no', server.server_instance_no)
                    server.nics = self._find_objs_by_key_value(_network_interfaces,
                                                               'server_instance_no', server.server_instance_no)

                    if _instance_access_control_rules and \
                            _instance_access_control_rules.get(server.server_instance_no):
                        server.security_groups = []

                        server.security_groups.extend(self._convert_access_control_rules(
                            _instance_access_control_rules.get(server.server_instance_no)))

                yield server

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

    def _convert_access_control_rules(self, access_control_rules: List[NCloudAccessControlRule]) \
            -> List[AccessControlRule]:
        """
        access_control_group_name = StringType(serialize_when_none=False)
        access_control_group_no = StringType(serialize_when_none=False)
        access_control_rule_description = StringType(serialize_when_none=False)
        port = StringType(serialize_when_none=False)
        flow = StringType(serialize_when_none=False)
        protocol = StringType(serialize_when_none=False)
        ip = StringType(serialize_when_none=False)
        """
        rtn_list = []

        for access_control_rule in access_control_rules:

            dic = {
                "access_control_group_name": access_control_rule.access_control_group_name,
                "access_control_group_no": access_control_rule.access_control_rule_configuration_no,
                "access_control_rule_description": access_control_rule.access_control_rule_description,
                "port": access_control_rule.destination_port,
                "ip": access_control_rule.source_ip
            }

            if access_control_rule.protocol_type.get("code_name"):
                dic["protocol"] = access_control_rule.protocol_type.get("code_name")

            dic["flow"] = "Inbound"

            rtn_list.append(AccessControlRule(dic))

        return rtn_list

    def _convert_disk(self, block_disks: List[NCloudBlock]) -> List[Disk]:
        """
        block_storage_name = StringType(serialize_when_none=False)
        block_storage_size = IntType(serialize_when_none=False)
        block_storage_instance_status_name = StringType(serialize_when_none=False)
        block_storage_disk_type = StringType(serialize_when_none=False)
        block_storage_instance_no = StringType(serialize_when_none=False)
        server_instance_no = StringType(serialize_when_none=False)
        device_name = StringType(serialize_when_none=False)
        max_iops_throughput = IntType(serialize_when_none=False)
        is_encrypted_volume = BooleanType(serialize_when_none=False)
        """
        rtn_list = []

        for block_disk in block_disks:

            dic = {
                "block_storage_name": block_disk.block_storage_name,
                "block_storage_size": block_disk.block_storage_size,
                "block_storage_instance_status_name": block_disk.block_storage_instance_status_name,
                "block_storage_instance_no": block_disk.block_storage_instance_no,
                "server_instance_no": block_disk.server_instance_no,
                "device_name": block_disk.device_name,
                "max_iops_throughput": block_disk.max_iops_throughput,
            }

            if block_disk.disk_detail_type and block_disk.disk_detail_type.get("code_name"):
                dic["block_storage_disk_type"] = block_disk.disk_detail_type.get("code_name")

            if block_disk.block_storage_type and block_disk.block_storage_type.get("code"):
                dic["block_storage_type"] = block_disk.block_storage_type.get("code")

            rtn_list.append(Disk(dic))

        return rtn_list

    def _convert_network_interfaces(self, network_interfaces: List[NCloudNetworkInterface]) \
            -> List[NetworkInterface]:
        """
        network_interface_name = StringType(serialize_when_none=False)
        ip = StringType(serialize_when_none=False)
        network_interface_status_name = StringType(serialize_when_none=False)
        device_name = StringType(serialize_when_none=False)
        is_default = BooleanType(serialize_when_none=False)
        network_interface_description = StringType(serialize_when_none=False)
        server_instance_no = StringType(serialize_when_none=False)
        """
        rtn_list = []

        for network_interface in network_interfaces:

            dic = {
                "network_interface_name": network_interface.network_interface_name,
                "ip": network_interface.network_interface_ip,
                "network_interface_status_name": network_interface.status_code,
                "is_default": False,
                "network_interface_description": network_interface.network_interface_description,
                "server_instance_no": network_interface.server_instance_no
            }

            rtn_list.append(NetworkInterface(dic))

        return rtn_list
