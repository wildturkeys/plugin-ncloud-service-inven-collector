import logging
from typing import Iterator, List
from typing import Optional, Type

import ncloud_vpc
from ncloud_vpc.api.v2_api import V2Api
from ncloud_vpc.rest import ApiException

from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_vpc_connector.schema.data import VPC, NcloudVPC, NcloudSubnet, NcloudACL, \
    NcloudNatGateway
from spaceone.inventory.connector.ncloud_vpc_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_vpc_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import API_TYPE_VPC


_LOGGER = logging.getLogger(__name__)


class VpcConnector(NCloudBaseConnector):
    cloud_service_group = 'Networking'
    cloud_service_type = 'VPC'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_vpc
    _ncloud_api_v2 = V2Api

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_type = API_TYPE_VPC

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        resources.extend(self.cloud_service_types)
        for region in self.regions:
            resources.extend(self._convert_cloud_service_response(self.list_vpc_instances(
                NcloudVPC, VPC, region_code=region.get('region_code')
            )))

        # resources.extend(self._convert_cloud_service_response(self.list_vpc_instances()))

        return resources

    def list_vpc_instances(self, ncloud_nas_vpc_cls:Type[NcloudVPC],
                           response_vpc_cls: Type[VPC], **kwargs) -> Iterator:

        try:

            response = self.api_client_v2.get_vpc_list(
                self._ncloud_cls.GetVpcListRequest(**kwargs))

            response_dict = response.to_dict()

            if response_dict.get("vpc_list"):
                _subnet_instances: List[Optional[NcloudSubnet]] = self._list_subnet_instance(**kwargs)
                _acl_instances: List[Optional[NcloudACL]] = self._list_acl_instance(**kwargs)
                _nat_gateway_instances: List[Optional[NcloudNatGateway]] = self._list_nat_gateway_instance(**kwargs)

                for vpc_instance in response_dict.get("vpc_list"):

                    vpc = response_vpc_cls(self._create_model_obj(ncloud_nas_vpc_cls, vpc_instance))
                    # vpc.acl = _acl_instances

                    if hasattr(vpc, "vpc_no"):
                        vpc.subnet = self._find_objs_by_key_value(_subnet_instances,
                                                                  'vpc_no',
                                                                  vpc.vpc_no)
                        vpc.acl = self._find_objs_by_key_value(_acl_instances,
                                                               'vpc_no',
                                                               vpc.vpc_no)

                        vpc.nat_gateway = self._find_objs_by_key_value(_nat_gateway_instances, 'vpc_no', vpc.vpc_no)
                    yield vpc

        except ApiException as e:
            logging.error(e)
            raise

    def _list_nat_gateway_instance(self, **kwargs) -> List[Type[NcloudNatGateway]]:
        return self._list_ncloud_resources(self.api_client_v2.get_nat_gateway_instance_list,
                                           self._ncloud_cls.GetNatGatewayInstanceListRequest,
                                           "nat_gateway_instance_list", NcloudNatGateway, **kwargs)

    def _list_subnet_instance(self, **kwargs) -> List[Type[NcloudSubnet]]:
        return self._list_ncloud_resources(self.api_client_v2.get_subnet_list,
                                           self._ncloud_cls.GetSubnetListRequest,
                                           "subnet_list", NcloudSubnet, **kwargs)

    def _list_acl_instance(self, **kwargs) -> List[Type[NcloudACL]]:
        return self._list_ncloud_resources(self.api_client_v2.get_network_acl_list,
                                           self._ncloud_cls.GetNetworkAclListRequest,
                                           "network_acl_list", NcloudACL, **kwargs)
