import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType, DateTimeType


_LOGGER = logging.getLogger(__name__)


class NasVolume(Model):

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


    region_code = StringType(serialize_when_none=False)
    zone_code = StringType(serialize_when_none=False)

    create_date = DateTimeType()

    nas_volume_instance_no = StringType(serialize_when_none=False)
    nas_volume_instance_status_name = StringType(serialize_when_none=False)
    nas_volume_instance_description = StringType(serialize_when_none=False)
    mount_information

    mount_information = StringType(serialize_when_none=False)


    @property
    def name(self) -> str:
        return self.volume_name

    def reference(self):
        return {
            "resource_id": self.nas_volume_instance_no,
            "external_link": f"https://console.ncloud.com/nas/volume"
        }

