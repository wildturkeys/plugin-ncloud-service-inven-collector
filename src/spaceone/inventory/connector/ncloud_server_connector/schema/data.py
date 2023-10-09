import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType, DateTimeType

_LOGGER = logging.getLogger(__name__)


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


class Server(NCloudServer):
    hardware = DictType(StringType, serialize_when_none=False)
    compute = DictType(StringType, serialize_when_none=False)
    nics = ListType(DictType(StringType), serialize_when_none=False)
    os = DictType(StringType, serialize_when_none=False)
    primary_ip_address = StringType(serialize_when_none=False)

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
