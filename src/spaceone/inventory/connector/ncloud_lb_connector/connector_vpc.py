import logging
from typing import Iterable, List
from typing import Type

import ncloud_vloadbalancer
from ncloud_vloadbalancer.rest import ApiException
from ncloud_vloadbalancer.api.v2_api import V2Api


from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_lb_connector.schema.data import NCloudLBVPC, LB_VPC, LBServerInstance
from spaceone.inventory.connector.ncloud_lb_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_lb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import API_TYPE_VPC

_LOGGER = logging.getLogger(__name__)


class LbVPCConnector(NCloudBaseConnector):
    cloud_service_group = 'Networking'
    cloud_service_type = 'Load Balancer'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_vloadbalancer
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_type = API_TYPE_VPC

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        for region in self.regions:
            resources.extend(
                self._convert_cloud_service_response(
                    self.list_load_balancer_instances(region_code=region.get('region_code'))))

        return resources

    def list_load_balancer_instances(self, **kwargs) -> Iterable[LB_VPC]:

        yield from self.__convert_list_load_balancer_instances(self._list_load_balancer_instances(**kwargs))

    def _list_load_balancer_instances(self, **kwargs) -> List[Type[NCloudLBVPC]]:

        return self._list_ncloud_resources(self.api_client_v2.get_load_balancer_instance_list,
                                           self._ncloud_cls.GetLoadBalancerInstanceListRequest,
                                           "load_balancer_instance_list",
                                           NCloudLBVPC,
                                           **kwargs)

    def __convert_list_load_balancer_instances(self, load_balancer_instances: List[NCloudLBVPC], **kwargs) \
            -> List[LB_VPC]:

        rtn_list = []

        for load_balancer_instance in load_balancer_instances:

            lb_vpc_obj = LB_VPC()
            lb_vpc_obj.load_balancer_name = load_balancer_instance.load_balancer_name
            lb_vpc_obj.load_balancer_description = load_balancer_instance.load_balancer_description
            lb_vpc_obj.load_balancer_instance_no = load_balancer_instance.load_balancer_instance_no
            lb_vpc_obj.load_balancer_ip_list = load_balancer_instance.load_balancer_ip_list
            lb_vpc_obj.load_balancer_domain = load_balancer_instance.load_balancer_domain
            lb_vpc_obj.load_balancer_instance_status_name =\
                str(load_balancer_instance.load_balancer_instance_status_name).lower()
            lb_vpc_obj.load_balancer_network_type = load_balancer_instance.load_balancer_network_type.get("code_name")
            lb_vpc_obj.load_balancer_type = load_balancer_instance.load_balancer_type.get("code_name")
            lb_vpc_obj.region_code = load_balancer_instance.region_code
            lb_vpc_obj.create_date = load_balancer_instance.create_date

            rtn_list.append(lb_vpc_obj)

        return rtn_list
