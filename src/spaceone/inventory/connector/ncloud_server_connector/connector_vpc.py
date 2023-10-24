import logging

import ncloud_vserver
from ncloud_vserver.api.v2_api import V2Api
from ncloud_vserver.rest import ApiException

from typing import Optional, Type, Iterable

from spaceone.inventory.connector.ncloud_server_connector.connector import ServerConnector
from spaceone.inventory.connector.ncloud_server_connector.schema.data import NCloudServerVPC, \
    NCloudAccessControlRuleVPC, ServerVPC, NCloudAccessControlVPC, NCloudNetworkInterfaceVPC
from spaceone.inventory.connector.ncloud_server_connector.schema.data import Server, NCloudServer, NCloudBlockVPC, \
    NCloudNetworkInterface, NCloudAccessControlRule, AccessControlRule

from spaceone.inventory.connector.ncloud_server_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_server_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import VPC_AVAILABLE_REGION, INSTANCE_STATE_MAP
from typing import Iterator, List

_LOGGER = logging.getLogger(__name__)


class ServerVPCConnector(ServerConnector):
    cloud_service_group = 'Compute'
    cloud_service_type = 'Server'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_vserver
    _ncloud_api_v2 = V2Api

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._access_control_rules_dict = {}

        for region in self.regions:
            if region.get('region_code') in VPC_AVAILABLE_REGION:
                region_code = region.get('region_code')
                self._access_control_rules_dict\
                    = dict(self._access_control_rules_dict,
                           **self._sort_access_control_group_rules_group_by_acg_no(region_code=region_code))

        self._server_images_dict = {}

    def get_resources(self) -> List[Type[CloudServiceResponse]]:
        resources = []

        for region in self.regions:
            if region.get('region_code') in VPC_AVAILABLE_REGION:
                resources.extend(
                    self._convert_cloud_service_response(self.list_server_instances(NCloudServerVPC,
                                                                                    ServerVPC,
                                                                                    region_code=region.get(
                                                                                        'region_code'))))
        return resources

    def _list_access_control_group(self, **kwargs) -> List[NCloudAccessControlVPC]:

        return self._list_ncloud_resources(self.api_client_v2.get_access_control_group_list,
                                           self._ncloud_cls.GetAccessControlGroupListRequest,
                                           "access_control_group_list",
                                           NCloudAccessControlVPC,
                                           **kwargs)

    def _list_access_control_rule(self, access_control_group_no: str,  **kwargs) -> List[NCloudAccessControlRuleVPC]:
        return self._list_ncloud_resources(self.api_client_v2.get_access_control_group_rule_list,
                                           self._ncloud_cls.GetAccessControlGroupRuleListRequest,
                                           "access_control_group_rule_list",
                                           NCloudAccessControlRuleVPC,
                                           access_control_group_no=access_control_group_no, **kwargs)

    def _list_network_interface(self, **kwargs) -> List[NCloudNetworkInterfaceVPC]:

        return self._list_ncloud_resources(self.api_client_v2.get_network_interface_list,
                                           self._ncloud_cls.GetNetworkInterfaceListRequest,
                                           "network_interface_list",
                                           NCloudNetworkInterfaceVPC,
                                           **kwargs)

    def _sort_access_control_group_rules_group_by_acg_no(self, **kwargs):

        rtn_dict = {}

        access_control_groups = self._list_access_control_group(**kwargs)
        for access_control_group in access_control_groups:
            access_control_group_no = access_control_group.access_control_group_no
            access_control_rules = self._list_access_control_rule(access_control_group_no, **kwargs)
            rtn_dict[access_control_group_no] = []
            for access_control_rule in access_control_rules:
                access_control_rule.access_control_group_name = access_control_group.access_control_group_name
                rtn_dict[access_control_group_no].append(access_control_rule)

        return rtn_dict

    def list_server_instances(self, ncloud_server_cls: Type[NCloudServer],
                              response_server_cls: Type[Server], **kwargs) -> Iterator:

        response = self.api_client_v2.get_server_instance_list(
            self._ncloud_cls.GetServerInstanceListRequest(**kwargs))
        response_dict = response.to_dict()

        if response_dict.get("server_instance_list"):

            _block_storages: List[Optional[NCloudBlockVPC]] = self._list_block_storage_instance(**kwargs)
            _network_interfaces: List[Optional[NCloudNetworkInterfaceVPC]] = self._list_network_interface(**kwargs)

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

                if hasattr(server, "server_instance_no"):
                    server.disks = self._find_objs_by_key_value(_block_storages,
                                                                'server_instance_no', server.server_instance_no)

                    server.nics = self._find_objs_by_key_value(_network_interfaces,
                                                               'instance_no', server.server_instance_no)

                    server.security_groups = []

                    for nic in server.nics:
                        if nic and nic.get("access_control_group_no_list"):
                            access_control_group_no_list = nic.get("access_control_group_no_list")
                            for acg_no in access_control_group_no_list:
                                if self._access_control_rules_dict.get(acg_no):
                                    server.security_groups.extend(
                                        self.__convert_access_control_rules(acg_no,
                                                                            self._access_control_rules_dict.get(acg_no)))

                yield server

    def __convert_access_control_rules(self, acg_no: str,
                                       access_control_rules: List[NCloudAccessControlRule]) -> Iterable[AccessControlRule]:
        """
        access_control_group_name = StringType(serialize_when_none=False)
        access_control_group_no = StringType(serialize_when_none=False)
        access_control_rule_description = StringType(serialize_when_none=False)
        port = StringType(serialize_when_none=False)
        flow = StringType(serialize_when_none=False)
        protocol = StringType(serialize_when_none=False)
        ip = StringType(serialize_when_none=False)
        """

        for access_control_rule in access_control_rules:

            dic = {
                "access_control_group_name": access_control_rule.access_control_group_name,
                "access_control_group_no": acg_no,
                "access_control_rule_description": access_control_rule.access_control_rule_description,
                "port": access_control_rule.port_range,
                "ip": access_control_rule.ip_block
            }

            if access_control_rule.protocol_type.get("code_name"):
                dic["protocol"] = access_control_rule.protocol_type.get("code_name")

            if access_control_rule.access_control_group_rule_type.get("code_name"):
                dic["flow"] = access_control_rule.access_control_group_rule_type.get("code_name")

            yield AccessControlRule(dic)
