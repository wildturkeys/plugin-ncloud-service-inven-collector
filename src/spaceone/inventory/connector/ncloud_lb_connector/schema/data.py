import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType, DateTimeType

_LOGGER = logging.getLogger(__name__)


class NCloudServerHealthCheckStatus(Model):
    l7_health_check_path = StringType(serialize_when_none=False)
    load_balancer_port = IntType(serialize_when_none=False)
    protocol_type = DictType(StringType, serialize_when_none=False)
    proxy_protocol_use_yn = StringType(serialize_when_none=False)
    server_port = IntType(serialize_when_none=False)
    server_status = BooleanType(serialize_when_none=False)


class NCloudLBRule(Model):
    certificate_name = StringType(serialize_when_none=False)
    l7_health_check_path = StringType(serialize_when_none=False)
    load_balancer_port = IntType(serialize_when_none=False)
    protocol_type = DictType(StringType, serialize_when_none=False)
    proxy_protocol_use_yn = StringType(serialize_when_none=False)
    server_port = IntType(serialize_when_none=False)


class NCloudLB(Model):
    certificate_name = StringType(serialize_when_none=False)
    connection_timeout = IntType(serialize_when_none=False)
    domain_name = StringType(serialize_when_none=False)
    internet_line_type = StringType(serialize_when_none=False)
    is_http_keep_alive = BooleanType(serialize_when_none=False)

    load_balancer_description = StringType(serialize_when_none=False)
    load_balancer_instance_no = StringType(serialize_when_none=False)

    load_balancer_instance_status = DictType(StringType, serialize_when_none=False)
    load_balancer_instance_operation = DictType(StringType, serialize_when_none=False)

    load_balancer_algorithm_type = DictType(StringType, serialize_when_none=False)
    load_balancer_instance_status_name = StringType(serialize_when_none=False)
    load_balancer_name = StringType(serialize_when_none=False)

    load_balancer_rule_list = ListType(ModelType(NCloudLBRule), serialize_when_none=False)
    network_usage_type = DictType(StringType, serialize_when_none=False)
    virtual_ip = StringType(serialize_when_none=False)
    create_date = DateTimeType()


class NCloudLBVPC(Model):
    load_balancer_name = StringType(serialize_when_none=False)
    load_balancer_description = StringType(serialize_when_none=False)
    load_balancer_domain = StringType(serialize_when_none=False)
    load_balancer_instance_no = StringType(serialize_when_none=False)
    load_balancer_instance_operation = DictType(StringType, serialize_when_none=False)
    load_balancer_instance_status = StringType(serialize_when_none=False)
    load_balancer_instance_status_name = StringType(serialize_when_none=False)
    load_balancer_ip_list = ListType(StringType, serialize_when_none=False)
    load_balancer_listener_no_list = ListType(StringType, serialize_when_none=False)
    load_balancer_network_type = DictType(StringType, serialize_when_none=False)
    load_balancer_type = DictType(StringType, serialize_when_none=False)
    region_code = StringType(serialize_when_none=False)
    subnet_no_list = ListType(StringType, serialize_when_none=False)
    throughput_type = DictType(StringType, serialize_when_none=False)
    vpc_no = ListType(StringType, serialize_when_none=False)
    create_date = DateTimeType()


class NCloudLBListenerVPC(Model):
    load_balancer_instance_no = StringType(serialize_when_none=False)
    load_balancer_listener_no = StringType(serialize_when_none=False)
    load_balancer_rule_no_list = ListType(StringType, serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    protocol_type = DictType(StringType, serialize_when_none=False)
    ssl_certificate_no = StringType(serialize_when_none=False)
    use_http2 = BooleanType(serialize_when_none=False)


class LBServerInstance(Model):
    server_name = StringType(serialize_when_none=False)
    server_instance_type = DictType(StringType, serialize_when_none=False)
    public_ip = StringType(serialize_when_none=False)
    private_ip = StringType(serialize_when_none=False)
    server_instance_status_name = StringType(serialize_when_none=False)
    server_instance_no = StringType(serialize_when_none=False)
    zone = DictType(StringType, serialize_when_none=False)
    internet_line_type = StringType(serialize_when_none=False)

    l7_health_check_path = StringType(serialize_when_none=False)
    load_balancer_port = IntType(serialize_when_none=False)
    protocol_type = DictType(StringType, serialize_when_none=False)
    proxy_protocol_use_yn = StringType(serialize_when_none=False)
    server_port = IntType(serialize_when_none=False)
    server_status = StringType(serialize_when_none=False)


class LBListener(Model):

    load_balancer_instance_name = StringType(serialize_when_none=False)
    load_balancer_instance_no = StringType(serialize_when_none=False)
    load_balancer_instance_port = StringType(serialize_when_none=False)
    load_balancer_instance_status_name = StringType(serialize_when_none=False)
    protocol_type = StringType(serialize_when_none=False)

    health_check_path = StringType(serialize_when_none=False)

    server_instance_name = StringType(serialize_when_none=False)
    server_instance_no = StringType(serialize_when_none=False)
    server_instance_port = StringType(serialize_when_none=False)
    server_instance_status_name = StringType(serialize_when_none=False)


class LB(Model):
    load_balancer_name = StringType(serialize_when_none=False)
    load_balancer_description = StringType(serialize_when_none=False)
    load_balancer_domain = StringType(serialize_when_none=False)
    load_balancer_instance_no = StringType(serialize_when_none=False)
    load_balancer_instance_operation = DictType(StringType, serialize_when_none=False)
    load_balancer_instance_status_name = StringType(serialize_when_none=False)
    load_balancer_instance_status_code = StringType(serialize_when_none=False)
    load_balancer_ip_list = ListType(StringType, serialize_when_none=False)
    load_balancer_network_type = StringType(serialize_when_none=False)
    load_balancer_type = StringType(serialize_when_none=False)
    region_code = StringType(serialize_when_none=False)
    throughput_type = StringType(serialize_when_none=False)

    load_balancer_listener_list = ListType(ModelType(LBListener), serialize_when_none=False, default=[])
    load_balanced_server_instance_count = IntType(serialize_when_none=False)

    platform_code = StringType(default="classic")
    create_date = DateTimeType()

    @property
    def instance_type(self) -> str:
        if self.network_usage_type:
            return self.network_usage_type.get('code_name', None)
        return None

    @property
    def name(self) -> str:
        return self.load_balancer_name

    def reference(self):
        return {
            "resource_id": self.load_balancer_instance_no,
            "external_link": "https://console.ncloud.com/load-balancer/loadBalancer"
        }


class LBVPC(LB):
    platform_code = StringType(default="vpc")
    vpc_no = ListType(StringType, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.load_balancer_instance_no,
            "external_link": "https://console.ncloud.com/vpc-load-balancer/loadBalancer"
        }
