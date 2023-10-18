import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType, DateTimeType, FloatType

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
    server_image_product_code = StringType(serialize_when_none=False)
    internet_line_type = StringType(serialize_when_none=False)
    server_product_code = StringType(serialize_when_none=False)
    server_instance_operation = DictType(StringType, serialize_when_none=False)
    server_instance_status = DictType(StringType, serialize_when_none=False)
    server_description = StringType(serialize_when_none=False)
    base_block_stroage_disk_detail_type = DictType(StringType, serialize_when_none=False)
    user_data = StringType(serialize_when_none=False)
    region = DictType(StringType, serialize_when_none=False)


class NcloudNasVolume(Model):

    volume_name = StringType(serialize_when_none=False)
    nas_volume_instance_status = DictType(StringType, serialize_when_none=False)

    volume_total_size = IntType(serialize_when_none=False)
    volume_size = IntType(serialize_when_none=False)
    volume_use_size = IntType(serialize_when_none=False)
    volume_use_ratio = FloatType(serialize_when_none=False)
    snapshot_volume_configuration_ratio = FloatType(serialize_when_none=False)
    snapshot_volume_config_time = IntType(serialize_when_none=False)
    snapshot_volume_size = IntType(serialize_when_none=False)
    snapshot_volume_use_size = IntType(serialize_when_none=False)
    snapshot_volume_use_ratio = FloatType(serialize_when_none=False)
    is_snapshot_configuration = BooleanType(serialize_when_none=False)
    is_event_configuration = BooleanType(serialize_when_none=False)
    is_return_protection = BooleanType(serialize_when_none=False)

    zone = DictType(StringType, serialize_when_none=False)
    region_code = StringType(serialize_when_none=False)
    zone_code = StringType(serialize_when_none=False)

    create_date = DateTimeType()

    nas_volume_instance_no = StringType(serialize_when_none=False)
    nas_volume_instance_status_name = StringType(serialize_when_none=False)

    mount_information = StringType(serialize_when_none=False)
    nas_volume_server_instance_list = ListType(ModelType(NCloudServer),serialize_when_none=False )




class NasVolume(NcloudNasVolume):
    nas_volume_server_instance_list = ListType(ModelType(NCloudServer), serialize_when_none=False)

    @property
    def name(self) -> str:
        return self.volume_name

    def reference(self):
        return {
            "resource_id": self.nas_volume_instance_no,
            "external_link": f"https://console.ncloud.com/nas/volume"
        }