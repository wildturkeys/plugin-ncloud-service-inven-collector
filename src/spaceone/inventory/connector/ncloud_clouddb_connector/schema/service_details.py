from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceMeta


details = ItemDynamicLayout.set_fields('Details', fields=[
    TextDyField.data_source('Name','data.cloud_db_service_name')

    ])

SERVICE_DETAILS = CloudServiceMeta.set_layouts([details])
