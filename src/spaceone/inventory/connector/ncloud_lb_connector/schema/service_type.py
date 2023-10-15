import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField, \
    SizeField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

instance_total_count_conf = os.path.join(current_dir, 'widget/instance_total_count.yaml')
count_by_type_conf = os.path.join(current_dir, 'widget/count_by_type.yaml')

cst_lb = CloudServiceTypeResource()
cst_lb.name = 'Load Balancer'
cst_lb.provider = 'ncloud'
cst_lb.group = 'Networking'
cst_lb.labels = ['Network']
cst_lb.service_code = 'ncloudLB'
cst_lb.is_primary = True
cst_lb.is_major = True
cst_lb.tags = {
    'spaceone:icon': f'{ASSET_URL}/Networking.svg',
}

cst_lb._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Status', 'data.load_balancer_instance_status_name'),
        TextDyField.data_source('Type', 'data.network_usage_type.code_name'),
        TextDyField.data_source('Domain', 'data.domain_name'),
        TextDyField.data_source('VIP', 'data.virtual_ip'),
        TextDyField.data_source('Algorithm', 'data.load_balancer_algorithm_type.code_name'),
        DateTimeDyField.data_source("Created", "data.create_date")
    ],
    search=[
        SearchField.set(name='Status', key='data.load_balancer_instance_status_name'),
        SearchField.set(name='Type', key='data.network_usage_type.code_name'),
        SearchField.set(name='Domain', key='data.domain_name'),
        SearchField.set(name='VIP', key='data.virtual_ip'),
        SearchField.set(name='Algorithm', key='data.load_balancer_algorithm_type.code_name')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(instance_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_type_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_lb})
]
