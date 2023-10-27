import os

from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_field import SearchField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_instance_count_conf = os.path.join(current_dir, 'widget/total_instance_count.yaml')
total_subnet_count_conf = os.path.join(current_dir,'widget/total_subnet_count.yaml')

count_by_project_conf = os.path.join(current_dir, 'widget/count_by_project.yaml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yaml')


cst_vpc = CloudServiceTypeResource()
cst_vpc.name = 'VPC'
cst_vpc.provider = 'ncloud'
cst_vpc.group = 'Networking'
cst_vpc.labels = ['Network']
cst_vpc.service_code = 'ncloudVPC'
cst_vpc.is_primary = True
cst_vpc.is_major = True
cst_vpc.tags = {
    'spaceone:icon': f'{ASSET_URL}/Networking.svg',
}

cst_vpc._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Status', 'data.vpc_status.code',
                                default_state={
                                    'safe': ['RUN'],
                                    'available': ['CREATING', 'INIT'],
                                    'disable': ['TERMTING']}),
        DateTimeDyField.data_source('Create', 'data.create_date'),

    ],
    search=[
        SearchField.set(name='Status', key='data.vpc_status.code'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_instance_count_conf)),
        # CardWidget.set(**get_data_from_yaml(total_subnet_count_conf)),

        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf))

    ]

)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_vpc})
]
