from schematics.types import ModelType, PolyModelType, StringType
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, \
    TableDynamicLayout

# TAB
details = ItemDynamicLayout.set_fields('Details', fields=[
    TextDyField.data_source('Login Key', 'data.login_key_name'),
    EnumDyField.data_source('Protect Server Termination', 'data.is_protect_server_termination', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Fee Charging Monitoring', 'data.is_fee_charging_monitoring', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    TextDyField.data_source('Base Storage Disk Type', 'data.base_block_storage_disk_detail_type.code_name'),
    SizeField.data_source('Base Storage Disk Size', 'data.base_block_storage_size', type="size",
                          options={"source_unit": "BYTES", "display_unit": "GB"}),
    TextDyField.data_source('Login Key', 'data.base_block_storage_disk_type'),
    TextDyField.data_source('Login Key', 'data.login_key_name'),
])

port_forwarding = ItemDynamicLayout.set_fields('Port Forwarding', fields=[
    TextDyField.data_source('Public IP', 'data.port_forwarding_public_ip'),
    TextDyField.data_source('External Port', 'data.port_forwarding_external_port'),
    TextDyField.data_source('Internal Port', 'data.port_forwarding_internal_port'),
])

SERVICE_DETAILS = CloudServiceMeta.set_layouts([details, port_forwarding])