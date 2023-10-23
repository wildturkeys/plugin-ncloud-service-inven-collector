import logging

import ncloud_vserver
from ncloud_vserver.api.v2_api import V2Api
from ncloud_vserver.rest import ApiException

from typing import Optional, Type

from spaceone.inventory.connector.ncloud_server_connector.connector import ServerConnector
from spaceone.inventory.connector.ncloud_server_connector.schema.data import NCloudServerVPC, ServerVPC
from spaceone.inventory.connector.ncloud_server_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_server_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import VPC_AVAILABLE_REGION
from typing import Iterator, List

_LOGGER = logging.getLogger(__name__)


class ServerVPCConnector(ServerConnector):
    cloud_service_group = 'Compute'
    cloud_service_type = 'Server'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_vserver
    _ncloud_api_v2 = V2Api

    def get_resources(self) -> List[Type[CloudServiceResponse]]:
        resources = []
        # resources.extend(self.cloud_service_types)

        for region in self.regions:
            if region.get('region_code') in VPC_AVAILABLE_REGION:
                resources.extend(
                    self._convert_cloud_service_response(self.list_server_instances(NCloudServerVPC,
                                                                                    ServerVPC,
                                                                                    region_code=region.get(
                                                                                        'region_code'))))
        return resources

    def _list_access_control_rule(self, access_control_group_configuration_no: str) -> List:

        return []

    def _list_access_control_group_server(self, access_control_group_configuration_no: str) \
            -> List:

        return []

    def _sort_access_control_group_rule_group_by_instance_no(self):
        return []
