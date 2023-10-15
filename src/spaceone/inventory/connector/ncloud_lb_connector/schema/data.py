import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType, DateTimeType, \
    PolyModelType

_LOGGER = logging.getLogger(__name__)


class NCloudACG(Model):
    access_control_group_configuration_no = StringType(serialize_when_none=False)
    access_control_group_description = StringType(serialize_when_none=False)
    access_control_group_name = StringType(serialize_when_none=False)
    create_date = DateTimeType(serialize_when_none=False)
    is_default = BooleanType(serialize_when_none=False)


class NCloudServer(Model):
    server_name = StringType(serialize_when_none=False)
    server_instance_type = DictType(StringType, serialize_when_none=False)
    public_ip = StringType(serialize_when_none=False)
    private_ip = StringType(serialize_when_none=False)
    memory_size = IntType(serialize_when_none=False)
    cpu_count = IntType(serialize_when_none=False)
    server_image_name = StringType(serialize_when_none=False)
    region_code = StringType(serialize_when_none=False)
    server_instance_status_name = StringType(serialize_when_none=False)
    server_instance_no = StringType(serialize_when_none=False)
    zone = DictType(StringType, serialize_when_none=False)
    login_key_name = StringType(serialize_when_none=False)
    port_forwarding_external_port = StringType(serialize_when_none=False)
    port_forwarding_internal_port = StringType(serialize_when_none=False)
    port_forwarding_public_ip = StringType(serialize_when_none=False)
    base_block_storage_disk_detail_type = DictType(StringType, serialize_when_none=False)
    base_block_storage_disk_type = DictType(StringType, serialize_when_none=False)
    base_block_storage_size = IntType(serialize_when_none=False)
    block_device_partition_list = ListType(StringType, serialize_when_none=False)
    instance_tag_list = ListType(StringType, serialize_when_none=False)
    is_fee_charging_monitoring = BooleanType(serialize_when_none=False)
    is_protect_server_termination = BooleanType(serialize_when_none=False)
    platform_type = DictType(StringType, serialize_when_none=False)
    create_date = DateTimeType()
    uptime = DateTimeType()
    server_image_product_code = StringType(serialize_when_none=False)
    internet_line_type = StringType(serialize_when_none=False)
    server_product_code = StringType(serialize_when_none=False)
    server_instance_operation = DictType(StringType, serialize_when_none=False)
    server_instance_status = DictType(StringType, serialize_when_none=False)
    access_control_group_list = ListType(ModelType(NCloudACG), serialize_when_none=False)
    server_description = StringType(serialize_when_none=False)
    base_block_stroage_disk_detail_type = DictType(StringType, serialize_when_none=False)
    user_data = StringType(serialize_when_none=False)
    region = DictType(StringType, serialize_when_none=False)


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


class NCloudLBServerInstance(Model):
    server_instance = ModelType(NCloudServer, serialize_when_none=False)
    server_health_check_status_list = ListType(ModelType(NCloudServerHealthCheckStatus), serialize_when_none=False)


class NCloudLB(Model):
    certificate_name = StringType(serialize_when_none=False)
    connection_timeout = IntType(serialize_when_none=False)
    domain_name = StringType(serialize_when_none=False)
    internet_line_type = StringType(serialize_when_none=False)
    is_http_keep_alive = BooleanType(serialize_when_none=False)

    load_balanced_server_instance_list = ListType(ModelType(NCloudLBServerInstance), serialize_when_none=False)

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
    region_code = StringType(serialize_when_none=False)
    create_date = DateTimeType()


class LB(NCloudLB):

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
            "external_link": f"https://console.ncloud.com/load-balancer/loadBalancer"
        }
