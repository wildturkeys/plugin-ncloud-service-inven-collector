import logging
import ncloud_vpc
from ncloud_vpc.api.v2_api import V2Api
from ncloud_vpc.rest import ApiException
from typing import Optional, Type
from spaceone.inventory.connector.ncloud_vpc_connector.schema.data import VPC, NcloudVPC
from spaceone.inventory.connector.ncloud_vpc_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_vpc_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse

from typing import Iterator, List

_LOGGER = logging.getLogger(__name__)

class VpcConnector(NCloudBaseConnector):
    cloud_service_group = 'Networking'
    cloud_service_type = 'VPC'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_vpc
    _ncloud_api_v2 = V2Api

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        resources.extend(self.cloud_service_types)
        resources.extend(self._convert_cloud_service_response(self.list_vpc_instances()))


        return resources

    def list_vpc_instances(self) -> Iterator:

        try:

            response = self.api_client_v2.get_vpc_list(
                ncloud_vpc.GetVpcListRequest())

            response_dict = response.to_dict()

            if response_dict.get("vpc_list"):

                for vpc_instance in response_dict.get("vpc_list"):

                    vpc = VPC(self._create_model_obj(NcloudVPC,vpc_instance ))

                    yield vpc

        except ApiException as e:
            logging.error(e)
            raise