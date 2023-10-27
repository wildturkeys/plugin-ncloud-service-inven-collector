import logging
from typing import Iterator, List, Dict
from typing import Optional, Type

import ncloud_vserver
from ncloud_vserver.api.v2_api import V2Api
from ncloud_vserver.rest import ApiException

from spaceone.inventory.connector.ncloud_server_connector.connector import ServerConnector
from spaceone.inventory.connector.ncloud_server_connector.schema.data import NCloudServerVPC, \
    NCloudAccessControlRuleVPC, ServerVPC, NCloudAccessControlVPC, NCloudNetworkInterfaceVPC
from spaceone.inventory.connector.ncloud_server_connector.schema.data import Server, NCloudServer, NCloudBlockVPC, \
     AccessControlRule, Disk, NetworkInterface, NCloudServerImageProduct
from spaceone.inventory.connector.ncloud_server_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_server_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import API_TYPE_VPC

_LOGGER = logging.getLogger(__name__)


class ServerVPCConnector(ServerConnector):
    cloud_service_group = 'Compute'
    cloud_service_type = 'Server'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_vserver
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_type = API_TYPE_VPC

        self._access_control_rules_dict = {}
        self._server_images_dict = {}

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        for region in self.regions:

            region_code = region.get('region_code')

            self._access_control_rules_dict \
                = dict(self._access_control_rules_dict,
                       **self._sort_access_control_group_rules_group_by_acg_no(region_code=region_code))

            for image_product in self._list_image_product(region_code=region_code):
                self._server_images_dict[image_product.product_code] = image_product.product_name

        for region in self.regions:
            resources.extend(
                self._convert_cloud_service_response(self.list_server_instances(NCloudServerVPC,
                                                                                ServerVPC,
                                                                                region_code=region.get(
                                                                                    'region_code'))))

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

            for server_instance in response_dict.get("server_instance_list"):

                server = response_server_cls(self._create_model_obj(ncloud_server_cls, server_instance))
                server.region_code = server_instance.get("region_code")

                if server_instance.get("server_image_product_code"):
                    server.server_image_name = \
                        self._server_images_dict.get(server_instance.get("server_image_product_code"))

                self._set_default_server_info(server)

                if server_instance.get('zone_code'):
                    server.zone_code = server_instance.get('zone_code')
                    server.compute['az'] = server_instance.get('zone_code')

                if hasattr(server, "server_instance_no"):
                    server.disks = self._find_objs_by_key_value(_block_storages,
                                                                'server_instance_no', server.server_instance_no)

                    server.nics = self._find_objs_by_key_value(_network_interfaces,
                                                               'server_instance_no', server.server_instance_no)

                    for nic in server.nics:
                        if nic.get("is_default"):
                            server.private_ip = nic.get("ip")
                            server.primary_ip_address = server.private_ip
                            continue

                    server.security_groups = []

                    for nic in server.nics:
                        if nic and nic.get("access_control_group_no_list"):
                            access_control_group_no_list = nic.get("access_control_group_no_list")
                            for acg_no in access_control_group_no_list:
                                if self._access_control_rules_dict.get(acg_no):
                                    server.security_groups.extend(
                                        self.__convert_access_control_rules(acg_no,
                                                                            self._access_control_rules_dict))

                yield server

    def _list_image_product(self, **kwargs) -> List[Type[NCloudServerImageProduct]]:

        return self._list_ncloud_resources(self.api_client_v2.get_server_image_product_list,
                                           self._ncloud_cls.GetServerImageProductListRequest,
                                           "product_list",
                                           NCloudServerImageProduct,
                                           **kwargs)

    def _list_block_storage_instance(self, **kwargs) -> List[Type[NCloudBlockVPC]]:

        return self._list_ncloud_resources(self.api_client_v2.get_block_storage_instance_list,
                                           self._ncloud_cls.GetBlockStorageInstanceListRequest,
                                           "block_storage_instance_list",
                                           NCloudBlockVPC,
                                           **kwargs)

    def _list_access_control_group(self, **kwargs) -> List[NCloudAccessControlVPC]:

        return self._list_ncloud_resources(self.api_client_v2.get_access_control_group_list,
                                           self._ncloud_cls.GetAccessControlGroupListRequest,
                                           "access_control_group_list",
                                           NCloudAccessControlVPC,
                                           **kwargs)

    def _list_access_control_rule(self, access_control_group_no: str, **kwargs) -> List[NCloudAccessControlRuleVPC]:
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

    def _sort_access_control_group_rules_group_by_acg_no(self, **kwargs) -> Dict:

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

    def __convert_access_control_rules(self, acg_no: str,
                                       access_control_rules: Dict) -> List[AccessControlRule]:
        """
        access_control_group_name = StringType(serialize_when_none=False)
        access_control_group_no = StringType(serialize_when_none=False)
        access_control_rule_description = StringType(serialize_when_none=False)
        port = StringType(serialize_when_none=False)
        flow = StringType(serialize_when_none=False)
        protocol = StringType(serialize_when_none=False)
        ip = StringType(serialize_when_none=False)
        """

        if not access_control_rules.get(acg_no):
            return []

        rtn_list = []

        for access_control_rule in access_control_rules.get(acg_no):

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

            rtn_list.append(AccessControlRule(dic))

        return rtn_list

    def _convert_disk(self, block_disks: List[NCloudBlockVPC]) -> List[Disk]:
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
                "is_encrypted_volume": block_disk.is_encrypted_volume
            }

            if block_disk.block_storage_disk_detail_type and block_disk.block_storage_disk_detail_type.get("code_name"):
                dic["block_storage_disk_type"] = block_disk.block_storage_disk_detail_type.get("code_name")

            if block_disk.block_storage_type and block_disk.block_storage_type.get("code"):
                dic["block_storage_type"] = block_disk.block_storage_type.get("code")

            rtn_list.append(Disk(dic))

        return rtn_list

    def _convert_network_interfaces(self, network_interfaces: List[NCloudNetworkInterfaceVPC]) \
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
                "ip": network_interface.ip,
                "network_interface_status_name": network_interface.network_interface_status.get("code"),
                "is_default": network_interface.is_default,
                "network_interface_description": network_interface.network_interface_description,
                "server_instance_no": network_interface.instance_no,
                "device_name": network_interface.device_name,
                "access_control_group_no_list": network_interface.access_control_group_no_list
            }

            rtn_list.append(NetworkInterface(dic))

        return rtn_list
