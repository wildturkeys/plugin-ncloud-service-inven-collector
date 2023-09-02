import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType


_LOGGER = logging.getLogger(__name__)


class Server(Model):
    server_name = StringType(serialize_when_none=False)
    server_instance_type = DictType(StringType, serialize_when_none=False)
    server_instance_status_name = StringType(serialize_when_none=False)
    private_ip = StringType(serialize_when_none=False)
    memory_size = IntType(serialize_when_none=False)
    cpu_count = IntType(serialize_when_none=False)
    server_image_name = StringType(serialize_when_none=False)
    region = DictType(StringType, serialize_when_none=False)

