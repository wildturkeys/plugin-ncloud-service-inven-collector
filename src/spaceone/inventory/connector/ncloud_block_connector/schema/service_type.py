import os

from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, EnumDyField, \
    SizeField
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

instance_total_count_conf = os.path.join(current_dir, 'widget/total_instance_count.yaml')
count_by_type_conf = os.path.join(current_dir, 'widget/count_by_type.yaml')

cst_block = CloudServiceTypeResource()
cst_block.name = 'Volume'
cst_block.provider = 'ncloud'
cst_block.group = 'Compute'
cst_block.labels = ['Storage']
cst_block.service_code = 'ncloudVolume'
cst_block.is_primary = True
cst_block.is_major = True
cst_block.tags = {
    'spaceone:icon': f'{ASSET_URL}/Compute.svg',
}
"""
Initialized
creating
detached
copying
terminating
repairing
terminated
detachFailed
"""

cst_block._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Platform', 'data.platform_code', default_badge={
            'indigo.500': ['classic'], 'coral.600': ['vpc']
        }),
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
        TextDyField.data_source('Volume Type', 'data.block_storage_type'),
        EnumDyField.data_source('Disk Type', 'data.block_storage_disk_type',
                                default_badge={'indigo.500': ['SSD'],
                                               'coral.600': ['HDD']}
                                ),
        TextDyField.data_source('MAX IOPS', 'data.max_iops_throughput'),
        TextDyField.data_source('Device', 'data.device_name'),
        TextDyField.data_source('Server ID', 'data.server_instance_no', reference={
            "resource_type": "inventory.CloudService",
            "reference_key": "reference.resource_id"}),
        TextDyField.data_source('Server Name', 'data.server_name'),
        TextDyField.data_source('Zone', 'data.zone_code'),
    ],
    search=[
        SearchField.set(name='Status', key='data.block_storage_instance_status_name'),
        SearchField.set(name='Volume ID', key='data.block_storage_instance_no'),
        SearchField.set(name='Volume Type', key='data.block_storage_type'),
        SearchField.set(name='Disk Type', key='data.block_storage_disk_type'),
        SearchField.set(name='MAX IOPS', key='data.max_iops_throughput'),
        SearchField.set(name='Device', key='data.device_name'),
        SearchField.set(name='Server ID', key='data.server_instance_no'),
        SearchField.set(name='Server Name', key='data.server_name'),
        SearchField.set(name='Zone Name', key='data.zone_code')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(instance_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_type_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_block})
]
