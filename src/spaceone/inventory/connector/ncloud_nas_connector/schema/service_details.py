from schematics.types import ModelType, PolyModelType, StringType
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, \
    TableDynamicLayout


details = ItemDynamicLayout.set_fields('Details', fields[
    # EnumDyField.data_source('Status','data.nas_volume_instance_status'),

    TextDyField.data_source('nas_volume_instance_status_name','data.nas_volume_instance_status_name'),
    SizeField.data_source('volume_total_size', 'data.volume_total_size',type="size",
                          options={"source_unit": "BYTES", "display_unit": "GB"}),
    SizeField.data_source('volume_size', 'data.volume_size',type="size",
                          options={"source_unit": "BYTES", "display_unit": "GB"}),
    SizeField.data_source('volume_use_size', 'data.volume_use_size',type="size",
                          options={"source_unit": "BYTES", "display_unit": "GB"}),


])
SERVICE_DETAILS = CloudServiceMeta.set_layouts([details])

    # volume_name = StringType(serialize_when_none=False)
    # nas_volume_instance_status = DictType(StringType, serialize_when_none=False)

    # volume_total_size = IntType(serialize_when_none=False)
    # volume_size = IntType(serialize_when_none=False)
    # volume_use_size = IntType(serialize_when_none=False)
    # volume_use_ratio = FloatType(serialize_when_none=False)
    # snapshot_volume_configuration_ratio = FloatType(serialize_when_none=False)
    # snapshot_volume_config_time = IntType(serialize_when_none=False)
    # snapshot_volume_size = IntType(serialize_when_none=False)
    # snapshot_volume_use_size = IntType(serialize_when_none=False)
    # snapshot_volume_use_ratio = FloatType(serialize_when_none=False)
    # is_snapshot_configuration = BooleanType(serialize_when_none=False)
    # is_event_configuration = BooleanType(serialize_when_none=False)
    # is_return_protection = BooleanType(serialize_when_none=False)


    # region_code = StringType(serialize_when_none=False)
    # zone_code = StringType(serialize_when_none=False)

    # create_date = DateTimeType()

    # nas_volume_instance_no = StringType(serialize_when_none=False)
    # nas_volume_instance_status_name = StringType(serialize_when_none=False)
    # nas_volume_instance_description = StringType(serialize_when_none=False)
    # mount_information

    # mount_information = StringType(serialize_when_none=False)