from schematics.types import ModelType, PolyModelType, StringType
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, \
    TableDynamicLayout


details = ItemDynamicLayout.set_fields('Details', fields= [
    # EnumDyField.data_source('Status','data.nas_volume_instance_status'),
    EnumDyField.data_source('Platform', 'data.platform_code', default_badge={
        'indigo.500': ['classic'], 'coral.600': ['vpc']
    }),
    TextDyField.data_source('Status','data.nas_volume_instance_status_name'),
    TextDyField.data_source('No' ,'data.nas_volume_instance_no'),
    SizeField.data_source('Volume Total Size', 'data.volume_total_size',type="size",
                          options={"source_unit": "BYTES", "display_unit": "GB"}),
    SizeField.data_source('Volume Size', 'data.volume_size',type="size",
                          options={"source_unit": "BYTES", "display_unit": "GB"}),
    SizeField.data_source('Volume Use Size', 'data.volume_use_size',type="size",
                          options={"source_unit": "BYTES", "display_unit": "GB"}),
    TextDyField.data_source('Volume Use Ratio','data.volume_use_ratio'),

    TextDyField.data_source('Region','data.region_code'),
    TextDyField.data_source('Zone','data.zone.zone_code'),

    DateTimeDyField.data_source("Created", "data.create_date"),
    TextDyField.data_source('Mount Information','data.mount_information'),

    TextDyField.data_source('Is Event Configuration', 'data.is_event_configuration'),
    TextDyField.data_source('Is Return Protection', 'data.is_return_protection'),
    TextDyField.data_source('Is Snapshot Configuration', 'data.is_snapshot_configuration'),

])
snapshot = ItemDynamicLayout.set_fields('Snapshot', fields=[
    SizeField.data_source('Snapshot Volume Size', 'data.snapshot_volume_size',
                          options={"source_unit": "BYTES", "display_unit": "GB"}),
    SizeField.data_source('Snapshot Volume Use Size', 'data.snapshot_volume_use_size',
                          options={"source_unit": "BYTES", "display_unit": "GB"}),
    TextDyField.data_source('Snapshot Volume Use Ratio', 'data.snapshot_volume_use_ratio'),
    TextDyField.data_source('Is Snapshot Configuration', 'data.is_snapshot_configuration'),

    TextDyField.data_source('Snapshot Volume Configuration Ratio', 'data.snapshot_volume_configuration_ratio'),
    TextDyField.data_source('Snapshot Volume Config Time', 'data.snapshot_volume_config_time'),

])
# 서버 이름, 존, ip , status
acl_server = TableDynamicLayout.set_fields('ACL Server',  root_path='data.nas_volume_server_instance_list', fields=[
    TextDyField.data_source('Name','server_name'),
    TextDyField.data_source('IP','zone.zone_code'),
    TextDyField.data_source('Zone','private_ip'),
    TextDyField.data_source('Status', 'server_instance_status_name'),
])

SERVICE_DETAILS = CloudServiceMeta.set_layouts([details, snapshot,acl_server])

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