import logging
from typing import Iterator, List, Dict
from typing import Optional, Type, Iterable

import ncloud_vserver
from ncloud_vserver.api.v2_api import V2Api
from ncloud_vserver.rest import ApiException

from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_block_connector.schema.data import BlockVPC, NCloudBlockVPC
from spaceone.inventory.connector.ncloud_server_connector.schema.data import NCloudServerVPC
from spaceone.inventory.connector.ncloud_block_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_block_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import API_TYPE_VPC

_LOGGER = logging.getLogger(__name__)


class BlockVPCConnector(NCloudBaseConnector):
    cloud_service_group = 'Compute'
    cloud_service_type = 'Volume'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_vserver
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_type = API_TYPE_VPC
        self.server_instance_dict = {}

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        resources.extend(self.cloud_service_types)

        for region in self.regions:

            region_code = region.get('region_code')

            for server_instance in self._list_server_instance(region_code=region_code):
                self.server_instance_dict[server_instance.server_instance_no] = server_instance.server_name

            resources.extend(
                self._convert_cloud_service_response(
                    self.list_block_storage_instance(region_code=region_code)))

        return resources

    def list_block_storage_instance(self, **kwargs) -> Iterable[BlockVPC]:

        yield from self._convert_block_storage(self._list_block_storage_instance(**kwargs))

    def _list_block_storage_instance(self, **kwargs) -> List[Type[NCloudBlockVPC]]:

        return self._list_ncloud_resources(self.api_client_v2.get_block_storage_instance_list,
                                           self._ncloud_cls.GetBlockStorageInstanceListRequest,
                                           "block_storage_instance_list",
                                           NCloudBlockVPC,
                                           **kwargs)

    def _list_server_instance(self, **kwargs) -> List[Type[NCloudBlockVPC]]:

        return self._list_ncloud_resources(self.api_client_v2.get_server_instance_list,
                                           self._ncloud_cls.GetServerInstanceListRequest,
                                           "server_instance_list",
                                           NCloudServerVPC,
                                           **kwargs)

    def _convert_block_storage(self, block_storages: List[NCloudBlockVPC]) -> List[BlockVPC]:
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

        for block_storage in block_storages:

            dic = {
                "block_storage_name": block_storage.block_storage_name,
                "block_storage_size": block_storage.block_storage_size,
                "block_storage_instance_status_name": block_storage.block_storage_instance_status_name,
                "block_storage_instance_no": block_storage.block_storage_instance_no,
                "server_instance_no": block_storage.server_instance_no,
                "device_name": block_storage.device_name,
                "max_iops_throughput": block_storage.max_iops_throughput,
                "region_code": block_storage.region_code,
                "zone_code": block_storage.zone_code,
                "create_date": block_storage.create_date,
                "is_encrypted_volume": str(block_storage.is_encrypted_volume).lower()
            }

            if block_storage.block_storage_disk_detail_type and\
                    block_storage.block_storage_disk_detail_type.get("code_name"):
                dic["block_storage_disk_type"] = block_storage.block_storage_disk_detail_type.get("code_name")

            if block_storage.block_storage_type and block_storage.block_storage_type.get("code"):
                dic["block_storage_type"] = block_storage.block_storage_type.get("code")

            if block_storage.server_instance_no:
                dic["server_name"] = self.server_instance_dict.get(block_storage.server_instance_no)

            rtn_list.append(BlockVPC(dic))

        return rtn_list
