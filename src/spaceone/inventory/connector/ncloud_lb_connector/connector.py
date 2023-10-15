import logging
import ncloud_loadbalancer
from ncloud_loadbalancer.api.v2_api import V2Api
from ncloud_loadbalancer.rest import ApiException
from typing import Optional, Type
from spaceone.inventory.connector.ncloud_lb_connector.schema.data import NCloudLB, LB
from spaceone.inventory.connector.ncloud_lb_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_lb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse

from typing import Iterator, List

_LOGGER = logging.getLogger(__name__)


class LbConnector(NCloudBaseConnector):
    cloud_service_group = 'Networking'
    cloud_service_type = 'Load Balancer'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_loadbalancer
    _ncloud_api_v2 = V2Api

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        resources.extend(self.cloud_service_types)

        for region in self.regions:
            resources.extend(
                self._convert_cloud_service_response(self.list_load_balancer_instances(region_no=region.get('region_no'))))

        return resources

    def list_load_balancer_instances(self, **kwargs) -> Iterator:

        try:

            response = self.api_client_v2.get_load_balancer_instance_list(ncloud_loadbalancer.GetLoadBalancerInstanceListRequest(**kwargs))

            response_dict = response.to_dict()

            if response_dict.get("load_balancer_instance_list"):

                for load_balancer_instance in response_dict.get("load_balancer_instance_list"):

                    load_balancer = LB(self._create_model_obj(NCloudLB, load_balancer_instance))

                    if kwargs.get("region_no"):
                        for region in self.regions:
                            if region.get("region_no") == kwargs.get("region_no"):
                                load_balancer.region_code = region.get("region_code")

                    yield load_balancer

        except ApiException as e:
            logging.error(e)
            raise
