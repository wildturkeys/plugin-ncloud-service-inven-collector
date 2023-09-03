import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType, DateTimeType


_LOGGER = logging.getLogger(__name__)


class Server(Model):

    server_name = StringType(serialize_when_none=False)
    server_instance_type = DictType(StringType, serialize_when_none=False)
    private_ip = StringType(serialize_when_none=False)
    memory_size = IntType(serialize_when_none=False)
    cpu_count = IntType(serialize_when_none=False)
    server_image_name = StringType(serialize_when_none=False)
    region_code = StringType(serialize_when_none=False)
    server_instance_status_name = StringType(serialize_when_none=False)
    server_instance_no = StringType(serialize_when_none=False)
    zone_code = StringType(serialize_when_none=False)
    create_date = DateTimeType()
    uptime = DateTimeType()

    def reference(self):
        return {
            "resource_id": self.server_instance_no,
            "external_link": f"https://console.ncloud.com/server/server"
        }

