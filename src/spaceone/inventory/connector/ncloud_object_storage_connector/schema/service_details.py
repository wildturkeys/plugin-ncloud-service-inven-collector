from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceMeta


details = ItemDynamicLayout.set_fields('Details', fields=[
    DateTimeDyField.data_source("Created", "data.CreationDate"),
])

SERVICE_DETAILS = CloudServiceMeta.set_layouts([details])
