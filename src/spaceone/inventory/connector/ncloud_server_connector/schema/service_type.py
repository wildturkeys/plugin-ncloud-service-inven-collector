import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField, \
    SizeField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_instance_count = os.path.join(current_dir, 'widget/total_instance_count.yaml')
total_vcpu_count = os.path.join(current_dir, 'widget/total_vcpu_count.yaml')
total_memory_size = os.path.join(current_dir, 'widget/total_memory_size.yaml')

count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')
count_by_project_conf = os.path.join(current_dir, 'widget/count_by_project.yaml')
count_by_type_conf = os.path.join(current_dir, 'widget/count_by_type.yaml')
count_by_core_conf = os.path.join(current_dir, 'widget/count_by_core.yaml')

cst_server = CloudServiceTypeResource()
cst_server.name = 'Server'
cst_server.provider = 'ncloud'
cst_server.group = 'Compute'
cst_server.labels = ['Server']
cst_server.service_code = 'ncloudServer'
cst_server.is_primary = True
cst_server.is_major = True
cst_server.tags = {
    'spaceone:icon': f'{ASSET_URL}/Compute.svg',
}

"""
# 서버 인스턴스 상태명
init
creating
booting
setting up
running
rebooting
hard rebooting
shutting down
hard shutting down
terminating
changingSpec
copying
repairing
"""
cst_server._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Platform', 'data.platform_code', default_badge={
            'indigo.500': ['classic'], 'coral.600': ['vpc']
        }),
        EnumDyField.data_source('Status', 'data.server_instance_status_name',
                                default_state={
                                    'safe': ['running'],
                                    'available': ['init', 'creating', 'booting', 'setting up', 'changingSpec'],
                                    'warning': ['warning', 'rebooting', 'hard rebooting', 'shutting down',
                                                'hard shutting down', 'terminating', 'copying', 'repairing', ],
                                    'disable': ['stopped']}),
        TextDyField.data_source('Public IP', 'data.public_ip'),
        TextDyField.data_source('Private IP', 'data.private_ip'),
        TextDyField.data_source('vCore', 'data.cpu_count'),
        SizeField.data_source('Memory', 'data.memory_size', type="size",
                              options={"source_unit": "BYTES", "display_unit": "GB"}),
        TextDyField.data_source('Instance Type', 'data.server_instance_type.code_name'),
        TextDyField.data_source('Image', 'data.server_image_name'),
        TextDyField.data_source('VPC', 'data.vpc_no', reference={"resource_type": "inventory.CloudService",
                                                                 "reference_key": "reference.resource_id"}),
        TextDyField.data_source('Zone', 'data.zone.zone_code'),
        DateTimeDyField.data_source("Created", "data.create_date")
    ],
    search=[
        SearchField.set(name='Status', key='data.server_instance_status_name'),
        SearchField.set(name='Private IP', key='data.private_ip'),
        SearchField.set(name='vCore', key='data.cpu_count', data_type='integer'),
        SearchField.set(name='Memory', key='data.memory_size', data_type='integer'),
        SearchField.set(name='Instance Type', key='data.server_instance_type.code_name'),
        SearchField.set(name='Image', key='data.server_image_name')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_instance_count)),
        CardWidget.set(**get_data_from_yaml(total_vcpu_count)),
        CardWidget.set(**get_data_from_yaml(total_memory_size)),

        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_type_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_core_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_server})
]
