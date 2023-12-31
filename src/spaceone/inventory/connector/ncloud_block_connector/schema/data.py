import logging

from schematics import Model
from schematics.types import StringType, IntType, DictType, DateTimeType, BooleanType

_LOGGER = logging.getLogger(__name__)


class NCloudBlock(Model):
    block_storage_name = StringType(serialize_when_none=False)
    block_storage_instance_description = StringType(serialize_when_none=False)
    block_storage_type = DictType(StringType, serialize_when_none=False)
    block_storage_instance_no = StringType(serialize_when_none=False)
    block_storage_size = IntType(serialize_when_none=False)
    device_name = StringType(serialize_when_none=False)
    block_storage_instance_status_name = StringType(serialize_when_none=False)
    server_instance_no = StringType(serialize_when_none=False)
    server_name = StringType(serialize_when_none=False)
    zone = DictType(StringType, serialize_when_none=False)
    create_date = DateTimeType()
    disk_detail_type = DictType(StringType, serialize_when_none=False)
    max_iops_throughput = IntType(serialize_when_none=False)
    region = DictType(StringType, serialize_when_none=False)


class NCloudBlockVPC(NCloudBlock):
    region_code = StringType(serialize_when_none=False)
    zone_code = StringType(serialize_when_none=False)
    block_storage_disk_type = DictType(StringType, serialize_when_none=False)
    is_encrypted_volume = BooleanType(serialize_when_none=False)
    block_storage_disk_detail_type = DictType(StringType, serialize_when_none=False)


class Block(NCloudBlock):
    region_code = StringType(serialize_when_none=False)
    platform_code = StringType(default="classic")
    block_storage_disk_type = StringType(serialize_when_none=False)
    block_storage_type = StringType(serialize_when_none=False)
    zone_code = StringType(serialize_when_none=False)

    @property
    def instance_type(self) -> str:
        return self.block_storage_type

    @property
    def instance_size(self) -> str:
        return self.block_storage_size

    @property
    def name(self) -> str:
        return self.block_storage_name

    def reference(self):
        return {
            "resource_id": self.block_storage_instance_no,
            "external_link": f"https://console.ncloud.com/server/storage"
        }


class BlockVPC(Block, NCloudBlockVPC):
    platform_code = StringType(default="vpc")
    is_encrypted_volume = StringType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.block_storage_instance_no,
            "external_link": f"https://console.ncloud.com/vpc-compute/storage"
        }
