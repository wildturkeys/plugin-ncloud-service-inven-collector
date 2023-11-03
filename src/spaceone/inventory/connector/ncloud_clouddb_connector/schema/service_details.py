from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceMeta


details = ItemDynamicLayout.set_fields('Details', fields=[
    TextDyField.data_source('Name','data.cloud_db_service_name'),

    EnumDyField.data_source('Kind', 'data.db_kind_code',
                            default_outline_badge=['MYSQL', 'MSSQL',
                                                   'REDIS']),
    TextDyField.data_source('Cloud DB ID', 'data.cloud_db_instance_no'),
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
db_server = TableDynamicLayout.set_fields('DB Server', root_path='data.cloud_db_server_instance_list', fields=[
    TextDyField.data_source('Name', 'cloud_db_server_name'),
    EnumDyField.data_source('Status', 'cloud_db_server_instance_status_name',
                            default_state={
                                'safe': ['running'],
                                'available': ['init', 'creating', 'booting', 'setting up', 'changingSpec'],
                                'warning': ['warning', 'rebooting', 'hard rebooting', 'shutting down',
                                            'hard shutting down', 'terminating', 'copying', 'repairing', ],
                                'disable': ['stopped']}
                            ),
    EnumDyField.data_source('Server Role','cloud_db_server_role.code_name',
                            default_outline_badge=['Master', 'Standby Master', 'Hidden Master','Stand Alone']),
    DateTimeDyField.data_source('Created','create_date'),
    TextDyField.data_source('Server ID', 'cloud_db_server_instance_no'),
    TextDyField.data_source('Storage Size','data_storage_size'),
    TextDyField.data_source('Used Storage Size', 'used_data_storage_size'),
    DateTimeDyField.data_source('Uptime','uptime'),

])

access_control_group = TableDynamicLayout.set_fields('Access Control Group', root_path='data.access_control_group_list', fields=[
    TextDyField.data_source('Name','access_control_group_name'),
    TextDyField.data_source('Description','access_control_group_description'),
    DateTimeDyField.data_source('Created','create_date'),
    TextDyField.data_source('Is Default','is_default')

    ])

SERVICE_DETAILS = CloudServiceMeta.set_layouts([details, db_server, access_control_group])
