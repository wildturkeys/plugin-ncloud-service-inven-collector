import logging

from schematics import Model
from schematics.types import StringType, IntType, DictType, DateTimeType, BooleanType

_LOGGER = logging.getLogger(__name__)


# # zone	Zone	Zone	[optional]
# zone_no	str	존(Zone)번호	[optional]
# zone_code	str	존(Zone)코드	[optional]
# zone_name	str	존(Zone)명	[optional]
# zone_description	str	존(Zone)설명	[optional]
# region_no	str	리전(Region)번호	[optional]

# region	Region	리전	[optional]
# region_no	str		[optional]
# region_code	str		[optional]
# region_name	str		[optional]

class NcloudCloudDB(Model):
    cloud_db_instance_no = StringType(serialize_when_none=False)
    cloud_db_service_name = StringType(serialize_when_none=False)
    db_kind_code = StringType(serialize_when_none=False)
    engine_version= StringType(serialize_when_none=False)
    cpu_count = IntType(serialize_when_none=False)
    memory_size = IntType(serialize_when_none=False)
    data_storage_type= DictType(StringType, serialize_when_none=False)
    license_code =StringType(serialize_when_none=False)
    cloud_db_port = IntType(serialize_when_none=False)
    is_ha = BooleanType(serialize_when_none=False)
    backup_time=StringType(serialize_when_none=False) #확인 필요
    backup_file_retention_period = IntType(serialize_when_none=False)
    cloud_db_instance_status_name =StringType(serialize_when_none=False)
    collation =StringType(serialize_when_none=False)
    reboot_schedule_time =StringType(serialize_when_none=False)
    create_date = DateTimeType()
    cloud_db_image_product_code	=StringType(serialize_when_none=False)
    cloud_db_product_code	=StringType(serialize_when_none=False)
    is_cloud_db_config_need_reboot=BooleanType(serialize_when_none=False)
    is_cloud_db_need_reboot	=BooleanType(serialize_when_none=False)
    # zone	Zone	Zone	[optional]

    # region	Region	리전	[optional]

    # cloud_db_config_list	list[CloudDBConfig]		[optional]
    # cloud_db_config_group_list	list[CloudDBConfigGroup]		[optional]
    # access_control_group_list	list[AccessControlGroup]		[optional]
    # cloud_db_server_instance_list	list[CloudDBServerInstance]		[optional]


class CloudDB(NcloudCloudDB):

    @property
    def name(self) -> str:
        return self.cloud_db_service_name

    def reference(self):
        return {
            "resource_id": self.cloud_db_instance_no,
            "external_link": f"https://console.ncloud.com/cloudMysql/server"
        }