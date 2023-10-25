from schematics.types import ModelType, PolyModelType, StringType
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, \
    SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, \
    TableDynamicLayout

# TAB
details = ItemDynamicLayout.set_fields('Details', fields=[
        EnumDyField.data_source('Platform', 'data.platform_code', default_badge={
            'indigo.500': ['classic'], 'coral.600': ['vpc']
        }),
        TextDyField.data_source('Name', 'data.block_storage_instance_name'),
        SizeField.data_source('Size(GB)', 'data.block_storage_size', options={
            'display_unit': 'GB',
            'source_unit': 'Byte'
        }),
        EnumDyField.data_source('Status', 'data.block_storage_instance_status_name',
                                default_state={
                                    'safe': ['attached'],
                                    'available': ['detached'],
                                    'warning': ['Initialized', 'creating', 'copying', 'terminating', 'repairing',
                                                'detachFailed'],
                                    'disable': ['terminated']}),
        TextDyField.data_source('Volume ID', 'data.block_storage_instance_no'),
        TextDyField.data_source('Volume Type', 'data.block_storage_type.code'),
        EnumDyField.data_source('Disk Type', 'data.disk_detail_type.code',
                                default_badge={'indigo.500': ['SSD'],
                                               'coral.600': ['HDD']}
                                ),
        TextDyField.data_source('MAX IOPS', 'data.max_iops_throughput'),
        TextDyField.data_source('Device', 'data.device_name'),
        TextDyField.data_source('Server ID', 'data.server_instance_no', reference={
            "resource_type": "inventory.CloudService",
            "reference_key": "reference.resource_id"}),
        TextDyField.data_source('Server Name', 'data.server_name'),
        TextDyField.data_source('Zone', 'data.zone.zone_code'),])


SERVICE_DETAILS = CloudServiceMeta.set_layouts([details])
