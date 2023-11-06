import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, BooleanType, DictType, DateTimeType, FloatType

_LOGGER = logging.getLogger(__name__)

#[{'Name': 'sojin-bucket', 'CreationDate': datetime.datetime(2023, 11, 6, 5, 46, 18, 834000, tzinfo=tzutc())}]


#
class NcloudObjectStorage(Model):
    Name = StringType(serialize_when_none=False)
    CreationDate = DateTimeType()


class ObjectStorage(NcloudObjectStorage):

    @property
    def name(self) -> str:
        return self.Name

    # def reference(self):
    #     return {
    #         "external_link": f"https://console.ncloud.com/nas/volume"
    #     }