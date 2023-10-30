from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceMeta


details = ItemDynamicLayout.set_fields('Details', fields=[
    TextDyField.data_source('Name','data.cloud_db_service_name'),

    TextDyField.data_source('Kind', 'data.db_kind_code',
                            default_outline_badge=['MYSQL', 'MSSQL',
                                                   'REDIS']),
    TextDyField.data_source('No', 'data.cloud_db_instance_no'),
    EnumDyField.data_source('Status', 'data.cloud_db_instance_status_name', default_state={
        'safe': ['created', 'running'],  # 확인필요
        'disable': ['terminated']
    }),
    TextDyField.data_source('Zone','data.zone.zone_name'),
    TextDyField.data_source('Region','data.region.region_name'),
    DateTimeDyField.data_source("Created", "data.create_date"),

    EnumDyField.data_source('Storage Type','data.data_storage_type.code_name',
                            default_badge={
                                'indigo.500': ['SSD'], 'coral.600': ['HDD']
                            }),
    TextDyField.data_source('Cpu Count','data.cpu_count'),
    TextDyField.data_source('Engine Version','data.engine_version')


    ])

SERVICE_DETAILS = CloudServiceMeta.set_layouts([details])
