import logging
from typing import Iterable, List
from typing import Type

import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException

from spaceone.inventory.connector.ncloud_block_connector.schema.data import Block, NCloudBlock
from spaceone.inventory.connector.ncloud_block_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_block_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.libs.schema.resource import CloudServiceResponse

_LOGGER = logging.getLogger(__name__)


class BlockConnector(NCloudBaseConnector):
    cloud_service_group = 'Compute'
    cloud_service_type = 'Volume'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_server
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        resources.extend(self.cloud_service_types)

        for region in self.regions:
            resources.extend(
                self._convert_cloud_service_response(
                    self.list_block_storage_instance(region_no=region.get('region_no'))))

        return resources

    def list_block_storage_instance(self, **kwargs) -> Iterable[Block]:

        try:

            response = self.api_client_v2.get_block_storage_instance_list(
                ncloud_server.GetBlockStorageInstanceListRequest(**kwargs))
            response_dict = response.to_dict()

            if response_dict.get("block_storage_instance_list"):

                for block_storage_instance in response_dict.get("block_storage_instance_list"):

                    block = Block(self._create_model_obj(NCloudBlock, block_storage_instance))
                    region = block.get("region")

                    if region.get("region_code"):
                        block.region_code = region.get("region_code")

                    yield block

        except ApiException as e:
            logging.error(e)
            raise
