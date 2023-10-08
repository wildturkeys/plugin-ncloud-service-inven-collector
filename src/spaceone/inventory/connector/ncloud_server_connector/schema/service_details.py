from schematics.types import ModelType, PolyModelType, StringType
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, \
    TableDynamicLayout

# TAB
port_forwarding = ItemDynamicLayout.set_fields('Port Forwarding', fields=[
    TextDyField.data_source('Public IP', 'data.port_forwarding_public_ip'),
    TextDyField.data_source('External Port', 'data.port_forwarding_external_port'),
    TextDyField.data_source('Internal Port', 'data.port_forwarding_internal_port'),
])

SERVICE_DETAILS = CloudServiceMeta.set_layouts([port_forwarding])