import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType, DateTimeType

_LOGGER = logging.getLogger(__name__)


class NcloudVPC(Model):
    create_date = DateTimeType()
    ipv4_cidr_block = StringType(serialize_when_none=False)
    region_code = StringType(serialize_when_none=False)
    vpc_name = StringType(serialize_when_none=False)
    vpc_no = StringType(serialize_when_none=False)
    vpc_status = DictType(StringType, serialize_when_none=False)


class VPC(NcloudVPC):

    @property
    def name(self) -> str:
        return self.vpc_name

    def reference(self):
        return {
            "resource_id": self.vpc_no,
            "external_link": f"https://console.ncloud.com/vpc-network/vpc"
        }
