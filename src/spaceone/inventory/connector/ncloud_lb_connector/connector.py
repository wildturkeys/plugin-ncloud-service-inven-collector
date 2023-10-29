import logging
from typing import Iterable, List
from typing import Type

import ncloud_loadbalancer
from ncloud_loadbalancer.api.v2_api import V2Api
from ncloud_loadbalancer.rest import ApiException

from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_lb_connector.schema.data import NCloudLB, LB, LBListener
from spaceone.inventory.connector.ncloud_lb_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_lb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse

_LOGGER = logging.getLogger(__name__)


class LbConnector(NCloudBaseConnector):
    cloud_service_group = 'Networking'
    cloud_service_type = 'Load Balancer'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_loadbalancer
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.load_balanced_server_instance_dict = {}

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        resources.extend(self.cloud_service_types)

        for region in self.regions:
            resources.extend(
                self._convert_cloud_service_response(
                    self.list_load_balancer_instances(region_no=region.get('region_no'))))

        return resources

    def list_load_balancer_instances(self, **kwargs) -> Iterable[LB]:

        yield from self._list_load_balancer_instances(**kwargs)

    def _list_load_balancer_instances(self, **kwargs) -> List[Type[LB]]:

        response = self.api_client_v2.get_load_balancer_instance_list(
            ncloud_loadbalancer.GetLoadBalancerInstanceListRequest(**kwargs))

        rtn_list: LB = []
        response_dict = response.to_dict()

        if response_dict.get("load_balancer_instance_list"):
            for load_balancer_instance in response_dict.get("load_balancer_instance_list"):
                rtn_list.append(self.__convert_load_balancer_instance(
                    self._create_model_obj(NCloudLB, load_balancer_instance),
                    load_balanced_server_instance_list=load_balancer_instance.get(
                        "load_balanced_server_instance_list")))

        return rtn_list

    """
    
    def list_load_balancer_instances(self, **kwargs) -> Iterator:

        try:

            response = self.api_client_v2.get_load_balancer_instance_list(
                ncloud_loadbalancer.GetLoadBalancerInstanceListRequest(**kwargs))

            response_dict = response.to_dict()

            if response_dict.get("load_balancer_instance_list"):

                for load_balancer_instance in response_dict.get("load_balancer_instance_list"):

                    load_balancer = LB(self._create_model_obj(NCloudLB, load_balancer_instance))

                    if load_balancer_instance.get("load_balanced_server_instance_list"):
                        load_balancer.load_balanced_server_instance_list = self._list_load_balancer_instance(
                            load_balancer_instance.get("load_balanced_server_instance_list"))
                        load_balancer.load_balanced_server_instance_count = len(load_balancer.load_balanced_server_instance_list)

                    if kwargs.get("region_no"):
                        for region in self.regions:
                            if region.get("region_no") == kwargs.get("region_no"):
                                load_balancer.region_code = region.get("region_code")

                    yield load_balancer

        except ApiException as e:
            logging.error(e)
            raise
    
    def _list_load_balancer_instance(self, load_balancer_instance_list) -> List[LBServerInstance]:

        rtn_list = []

        for load_balancer_instance in load_balancer_instance_list:

            server_instance = load_balancer_instance.get("server_instance")
            server_health_check_status_list = load_balancer_instance.get("server_health_check_status_list", [])

            server_instance_obj = {}

            for server_health_check_status in server_health_check_status_list:
                server_instance_obj["protocol_type"] = server_health_check_status.get("protocol_type")
                server_instance_obj["load_balancer_port"] = server_health_check_status.get("load_balancer_port")
                server_instance_obj["server_port"] = server_health_check_status.get("server_port")
                server_instance_obj["l7_health_check_path"] = server_health_check_status.get("l7_health_check_path")
                server_instance_obj["proxy_protocol_use_yn"] = server_health_check_status.get("proxy_protocol_use_yn")
                server_instance_obj["server_status"] = str(server_health_check_status.get("server_status", "")).lower()
                server_instance_obj["server_name"] = server_instance.get("server_name")
                server_instance_obj["server_instance_type"] = server_instance.get("server_instance_type")
                server_instance_obj["public_ip"] = server_instance.get("public_ip")
                server_instance_obj["private_ip"] = server_instance.get("private_ip")
                server_instance_obj["server_instance_status_name"] = server_instance.get("server_instance_status_name")
                server_instance_obj["server_instance_no"] = server_instance.get("server_instance_no")
                server_instance_obj["zone"] = server_instance.get("zone")
                server_instance_obj["internet_line_type"] = server_instance.get("internet_line_type")

                rtn_list.append(LBServerInstance(server_instance_obj))

        return rtn_list
        """

    def __convert_load_balancer_instance(self, load_balancer_instance: NCloudLB, **kwargs) -> LB:

        lb_obj = LB()
        lb_obj.load_balancer_name = load_balancer_instance.load_balancer_name
        lb_obj.load_balancer_description = load_balancer_instance.load_balancer_description
        lb_obj.load_balancer_instance_no = load_balancer_instance.load_balancer_instance_no

        if load_balancer_instance.get('virtual_ip'):
            lb_obj.load_balancer_ip_list = str(load_balancer_instance.virtual_ip).split(",")

        lb_obj.load_balancer_domain = load_balancer_instance.domain_name
        lb_obj.load_balancer_instance_status_name = load_balancer_instance.load_balancer_instance_status_name
        lb_obj.load_balancer_network_type = load_balancer_instance.network_usage_type.get("code_name")
        lb_obj.create_date = load_balancer_instance.create_date

        if load_balancer_instance.get("region"):
            lb_obj.region_code = load_balancer_instance.get("region").get("region_code")
        if 'load_balanced_server_instance_list' in kwargs:
            lb_obj.load_balancer_listener_list = self.__convert_list_load_balancer_listener(
                kwargs.get('load_balanced_server_instance_list'),
                lb_obj.load_balancer_name,
                lb_obj.load_balancer_instance_no
            )

        return lb_obj

    def __convert_list_load_balancer_listener(self, load_balanced_server_instance_list: list,
                                              load_balancer_instance_name: str,
                                              load_balancer_instance_no: str) -> List[LBListener]:

        rtn_list = []

        for load_balanced_server_instance in load_balanced_server_instance_list:

            server_instance = load_balanced_server_instance.get("server_instance")
            server_health_check_status_list = load_balanced_server_instance.get("server_health_check_status_list", [])

            for server_health_check_status in server_health_check_status_list:
                lb_listener_obj = LBListener()

                lb_listener_obj.load_balancer_instance_name = load_balancer_instance_name
                lb_listener_obj.load_balancer_instance_no = load_balancer_instance_no
                lb_listener_obj.load_balancer_instance_port = str(server_health_check_status.get("load_balancer_port"))
                lb_listener_obj.protocol_type = server_health_check_status.get("protocol_type").get("code_name")
                lb_listener_obj.load_balancer_instance_status_name = str(
                    server_health_check_status.get("server_status")).lower()

                lb_listener_obj.health_check_path = server_health_check_status.get("l7_health_check_path")

                lb_listener_obj.server_instance_name = server_instance.get("server_name")
                lb_listener_obj.server_instance_no = server_instance.get("server_instance_no")
                lb_listener_obj.server_instance_port = str(server_health_check_status.get("server_port"))
                lb_listener_obj.server_instance_status_name = server_instance.get("server_instance_status_name")

                rtn_list.append(lb_listener_obj)

        return rtn_list
