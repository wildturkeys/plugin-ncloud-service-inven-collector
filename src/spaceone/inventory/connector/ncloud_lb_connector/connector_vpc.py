import logging
from typing import Iterable, List
from typing import Type

import ncloud_vloadbalancer
import ncloud_vserver
from ncloud_vloadbalancer.model.target_group import TargetGroup
from ncloud_vloadbalancer.model.target import Target
from ncloud_vloadbalancer.model.load_balancer_listener import LoadBalancerListener
from ncloud_vloadbalancer.model.load_balancer_rule import LoadBalancerRule
from ncloud_vserver.model.server_instance import ServerInstance

from ncloud_vloadbalancer.rest import ApiException
from ncloud_vloadbalancer.api.v2_api import V2Api
from ncloud_vserver.api.v2_api import V2Api as VSERVER_V2Api
from ncloud_vserver.rest import ApiException as VSERVER_ApiException

from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_lb_connector.schema.data import NCloudLBVPC, LBVPC, LBListener
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

        self.__target_groups_dict__ = {}
        self.__target_dict__ = {}
        self.__server_instance_dict__ = {}

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []

        for region in self.regions:
            region_code = region.get('region_code')

            self.__set_target_groups(self.__get_target_group_list__(region_code))
            self.__set_server_instances(self.__get_server_instance_list__(region_code))

            resources.extend(
                self._convert_cloud_service_response(
                    self.list_load_balancer_instances(region_code=region_code)))

        return resources

    def list_load_balancer_instances(self, **kwargs) -> Iterable[LBVPC]:

        yield from self.__convert_list_load_balancer_instances(self._list_load_balancer_instances(**kwargs))

    def _list_load_balancer_instances(self, **kwargs) -> List[Type[NCloudLBVPC]]:

        return self._list_ncloud_resources(self.api_client_v2.get_load_balancer_instance_list,
                                           self._ncloud_cls.GetLoadBalancerInstanceListRequest,
                                           "load_balancer_instance_list",
                                           NCloudLBVPC,
                                           **kwargs)

    def __get_lb_listener_List__(self, region_code, load_balancer_instance_no) -> List[LoadBalancerListener]:
        return self._list_ncloud_raw_resources(self.api_client_v2.get_load_balancer_listener_list,
                                               self._ncloud_cls.GetLoadBalancerListenerListRequest,
                                               "load_balancer_listener_list",
                                               region_code=region_code,
                                               load_balancer_instance_no=load_balancer_instance_no)

    def __get_lb_rule_List__(self, region_code, load_balancer_listener_no) -> List[LoadBalancerRule]:
        return self._list_ncloud_raw_resources(self.api_client_v2.get_load_balancer_rule_list,
                                               self._ncloud_cls.GetLoadBalancerRuleListRequest,
                                               "load_balancer_rule_list",
                                               region_code=region_code,
                                               load_balancer_listener_no=load_balancer_listener_no)

    def __get_target_group_list__(self, region_code) -> List[TargetGroup]:
        return self._list_ncloud_raw_resources(self.api_client_v2.get_target_group_list,
                                               self._ncloud_cls.GetTargetGroupListRequest,
                                               "target_group_list",
                                               region_code=region_code)

    def __get_target_list__(self, region_code, target_group_no) -> List[Target]:
        return self._list_ncloud_raw_resources(self.api_client_v2.get_target_list,
                                               self._ncloud_cls.GetTargetListRequest,
                                               "target_list",
                                               region_code=region_code,
                                               target_group_no=target_group_no)

    def __get_server_instance_list__(self, region_code) -> List[ServerInstance]:
        return self._list_ncloud_raw_resources_ex(ncloud_vserver,
                                                  VSERVER_V2Api,
                                                  VSERVER_ApiException,
                                                  'get_server_instance_list',
                                                  ncloud_vserver.GetServerInstanceListRequest,
                                                  "server_instance_list",
                                                  region_code=region_code)

    def __convert_list_load_balancer_instances(self, load_balancer_instances: List[NCloudLBVPC]) -> List[LBVPC]:

        rtn_list = []

        for load_balancer_instance in load_balancer_instances:
            lb_vpc_obj = LBVPC()
            lb_vpc_obj.load_balancer_name = load_balancer_instance.load_balancer_name
            lb_vpc_obj.load_balancer_description = load_balancer_instance.load_balancer_description
            lb_vpc_obj.load_balancer_instance_no = load_balancer_instance.load_balancer_instance_no
            lb_vpc_obj.load_balancer_ip_list = load_balancer_instance.load_balancer_ip_list
            lb_vpc_obj.load_balancer_domain = load_balancer_instance.load_balancer_domain
            lb_vpc_obj.load_balancer_instance_status_name = \
                str(load_balancer_instance.load_balancer_instance_status_name).lower()
            lb_vpc_obj.load_balancer_network_type = load_balancer_instance.load_balancer_network_type.get("code_name")
            lb_vpc_obj.load_balancer_type = load_balancer_instance.load_balancer_type.get("code_name")
            lb_vpc_obj.region_code = load_balancer_instance.region_code
            lb_vpc_obj.create_date = load_balancer_instance.create_date

            lb_vpc_obj.load_balancer_listener_list = \
                self.__convert_list_load_balancer_listener(load_balancer_instance)

            rtn_list.append(lb_vpc_obj)

        return rtn_list

    def __convert_list_load_balancer_listener(self, load_balancer_instance: LBVPC) -> List[LBListener]:

        load_balancer_listener_list = []

        region_code = load_balancer_instance.region_code
        load_balancer_instance_no = load_balancer_instance.load_balancer_instance_no

        lb_listeners = self.__get_lb_listener_List__(region_code, load_balancer_instance_no)

        for lb_listener in lb_listeners:

            load_balancer_listener_no = lb_listener.load_balancer_listener_no
            load_balancer_rule_list = self.__get_lb_rule_List__(region_code, load_balancer_listener_no)
            target_group_no_list = self.__get_target_group_no_list(load_balancer_rule_list)

            for target_group_no in target_group_no_list:

                self.__set_target(target_group_no, self.__get_target_list__(region_code, target_group_no))

                target_group_info = self.__target_groups_dict__.get(target_group_no)
                if target_group_info.get("target_no_list"):
                    target_no_list = target_group_info.get("target_no_list")

                    for target_no in target_no_list:
                        lb_listener_obj = LBListener()

                        lb_listener_obj.load_balancer_instance_name = load_balancer_instance.load_balancer_name
                        lb_listener_obj.load_balancer_instance_no = load_balancer_instance.load_balancer_instance_no
                        lb_listener_obj.load_balancer_instance_port = str(lb_listener.port)
                        lb_listener_obj.protocol_type = str(lb_listener.protocol_type.code).lower()

                        target_key = f"{target_group_no}_{target_no}"

                        lb_listener_obj.load_balancer_instance_status_name = str(
                            self.__target_dict__.get(target_key)).lower()
                        lb_listener_obj.server_instance_no = target_no
                        lb_listener_obj.server_instance_port = str(target_group_info.get("target_group_port"))
                        lb_listener_obj.health_check_path = target_group_info.get("health_check_url_path")

                        if target_no in self.__server_instance_dict__:
                            lb_listener_obj.server_instance_name = \
                                self.__server_instance_dict__[target_no].get("server_name")
                            lb_listener_obj.server_instance_status_name = \
                                self.__server_instance_dict__[target_no].get("server_instance_status_name")

                        load_balancer_listener_list.append(lb_listener_obj)

        return load_balancer_listener_list

    def __get_target_group_no_list(self, load_balancer_rule_list: List[LoadBalancerRule]) -> List[str]:

        target_group_no_list = []

        for load_balancer_rule in load_balancer_rule_list:

            load_balancer_rule_action_list = load_balancer_rule.load_balancer_rule_action_list

            for load_balancer_rule_action in load_balancer_rule_action_list:
                target_group_weight_list = load_balancer_rule_action.target_group_action.target_group_weight_list

                for target_group_weight in target_group_weight_list:
                    target_group_no_list.append(target_group_weight.target_group_no)

        return target_group_no_list

    def __set_target_groups(self, target_groups: List[TargetGroup]):

        for target_group in target_groups:
            self.__target_groups_dict__[target_group.target_group_no] = {

                "algorithm_type": target_group.algorithm_type.code_name,
                "health_check_url_path": target_group.health_check_url_path,
                "health_check_port": target_group.health_check_port,
                "health_check_protocol_type": target_group.health_check_protocol_type.code,
                "target_group_name": target_group.target_group_name,
                "target_group_port": target_group.target_group_port,
                "target_group_protocol_type": target_group.target_group_protocol_type.code_name,
                "target_no_list": target_group.target_no_list,
                "target_type": target_group.target_type.code,
                "vpc_no": target_group.vpc_no
            }

    def __set_server_instances(self, server_instances: List[ServerInstance]):

        for server_instance in server_instances:
            self.__server_instance_dict__[server_instance.server_instance_no] = {
                "server_instance_status_name": server_instance.server_instance_status_name,
                "server_name": server_instance.server_name
            }

    def __set_target(self, target_group: str, targets: List[Target]):

        for target in targets:
            target_key = f"{target_group}_{target.target_no}"
            self.__target_dict__[target_key] = target.health_check_status.code
