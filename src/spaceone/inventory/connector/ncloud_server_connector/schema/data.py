import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType, DateTimeType

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


class NCloudBlock(Model):
    block_storage_name = StringType(serialize_when_none=False)
    block_storage_instance_description = StringType(serialize_when_none=False)
    block_storage_type = DictType(StringType, serialize_when_none=False)
    block_storage_instance_no = StringType(serialize_when_none=False)
    block_storage_size = IntType(serialize_when_none=False)
    device_name = StringType(serialize_when_none=False)
    region_code = StringType(serialize_when_none=False)
    block_storage_instance_status_name = StringType(serialize_when_none=False)
    server_instance_no = StringType(serialize_when_none=False)
    server_name = StringType(serialize_when_none=False)
    zone = DictType(StringType, serialize_when_none=False)
    create_date = DateTimeType()
    disk_detail_type = DictType(StringType, serialize_when_none=False)
    max_iops_throughput = IntType(serialize_when_none=False)


class NCloudNetworkInterface(Model):
    network_interface_name = StringType(serialize_when_none=False)
    network_interface_description = StringType(serialize_when_none=False)
    network_interface_ip = StringType(serialize_when_none=False)
    network_interface_no = StringType(serialize_when_none=False)
    server_instance_no = StringType(serialize_when_none=False)
    status_code = StringType(serialize_when_none=False)


class NCloudAccessControlGroup(Model):
    access_control_group_name = StringType(serialize_when_none=False)
    access_control_group_description = StringType(serialize_when_none=False)
    access_control_group_configuration_no = StringType(serialize_when_none=False)
    create_date = DateTimeType(serialize_when_none=False)
    is_default_group = StringType(serialize_when_none=False)


class NCloudAccessControlGroupServerInstance(Model):
    server_instance_no = StringType(serialize_when_none=False)
    access_control_group_list = ListType(DictType(StringType), serialize_when_none=False)


class NCloudAccessControlRule(Model):
    access_control_group_name = StringType(serialize_when_none=False)
    access_control_rule_configuration_no = StringType(serialize_when_none=False)
    access_control_rule_description = StringType(serialize_when_none=False)
    destination_port = StringType(serialize_when_none=False)
    protocol_type = DictType(StringType, serialize_when_none=False)
    source_access_control_rule_configuration_no = StringType(serialize_when_none=False)
    source_access_control_rule_name = StringType(serialize_when_none=False)
    source_ip = StringType(serialize_when_none=False)
    flow = StringType(serialize_when_none=False, default="Inbound")


class NCloudNetworkInterfaceVPC(Model):
    access_control_group_no_list = ListType(StringType, serialize_when_none=False)
    delete_on_termination = BooleanType(serialize_when_none=False)
    device_name = StringType(serialize_when_none=False)
    instance_no = StringType(serialize_when_none=False)
    instance_type = DictType(StringType, serialize_when_none=False)
    ip = StringType(serialize_when_none=False)
    is_default = BooleanType(serialize_when_none=False)
    network_interface_name = StringType(serialize_when_none=False)
    network_interface_description = StringType(serialize_when_none=False)
    network_interface_no = StringType(serialize_when_none=False)
    network_interface_status = DictType(StringType, serialize_when_none=False)
    subnet_no = StringType(serialize_when_none=False)


class NCloudBlockVPC(NCloudBlock):
    pass


class NCloudAccessControlVPC(Model):
    access_control_group_name = StringType(serialize_when_none=False)
    access_control_group_description = StringType(serialize_when_none=False)
    access_control_group_no = StringType(serialize_when_none=False)
    access_control_group_status = DictType(StringType, serialize_when_none=False)
    is_default = BooleanType(serialize_when_none=False)
    vpc_no = StringType(serialize_when_none=False)


class NCloudAccessControlRuleVPC(Model):
    access_control_group_name = StringType(serialize_when_none=False)
    access_control_rule_no = StringType(serialize_when_none=False)
    access_control_rule_description = StringType(serialize_when_none=False)
    access_control_group_rule_type = DictType(StringType, serialize_when_none=False)
    access_control_group_sequence = StringType(serialize_when_none=False)
    ip_block = StringType(serialize_when_none=False)
    port_range = StringType(serialize_when_none=False)
    protocol_type = DictType(StringType, serialize_when_none=False)


class Server(NCloudServer):
    hardware = DictType(StringType, serialize_when_none=False)
    compute = DictType(StringType, serialize_when_none=False)
    nics = ListType(ModelType(NCloudNetworkInterface), serialize_when_none=False, default=[])
    os = DictType(StringType, serialize_when_none=False)
    primary_ip_address = StringType(serialize_when_none=False)
    disks = ListType(ModelType(NCloudBlock), serialize_when_none=False, default=[])
    security_groups = ListType(ModelType(NCloudAccessControlRule), serialize_when_none=False, default=[])

    platform_code = StringType(default="classic")
    zone_code = StringType(serialize_when_none=False)

    @property
    def instance_type(self) -> str:
        return self.server_instance_type.get('code_name', None)

    @property
    def name(self) -> str:
        return self.server_name

    def reference(self):
        return {
            "resource_id": self.server_instance_no,
            "external_link": f"https://console.ncloud.com/server/server"
        }


## VPC

class NCloudServerVPC(NCloudServer):
    vpc_no = StringType(serialize_when_none=False)
    subnet_no = StringType(serialize_when_none=False)
    region_code = StringType(serialize_when_none=False)


class ServerVPC(NCloudServerVPC, Server):
    platform_code = StringType(default="vpc")

    def reference(self):
        return {
            "resource_id": self.server_instance_no,
            "external_link": "https://console.ncloud.com/vpc-compute/server"
        }


class AccessControlRule(Model):
    access_control_group_name = StringType(serialize_when_none=False)
    access_control_group_no = StringType(serialize_when_none=False)
    access_control_rule_description = StringType(serialize_when_none=False)
    port = StringType(serialize_when_none=False)
    flow = StringType(serialize_when_none=False)
    protocol = StringType(serialize_when_none=False)
    ip = StringType(serialize_when_none=False)
