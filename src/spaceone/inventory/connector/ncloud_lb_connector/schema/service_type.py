import os

from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

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
        EnumDyField.data_source('Platform', 'data.platform_code', default_badge={
            'indigo.500': ['classic'], 'coral.600': ['vpc']
        }),
        EnumDyField.data_source('Type', 'data.load_balancer_network_type',
                                default_badge={'indigo.500': ['Public'],
                                               'coral.600': ['Private']}
                                ),
        TextDyField.data_source('Domain', 'data.load_balancer_domain'),
        EnumDyField.data_source('Status', 'data.load_balancer_instance_status_name',
                                default_state={
                                    'safe': ['used', 'using', 'created', "running"],
                                    'available': ['initialized', 'creating',
                                                  'repairing', 'using'],
                                    'warning': ['disusing', 'changing', 'terminating'],
                                    'disable': ['terminated']}),
        ListDyField.data_source('IPs', 'data.load_balancer_ip_list'),
        DateTimeDyField.data_source("Created", "data.create_date")
    ],
    search=[
        SearchField.set(name='Status', key='data.load_balancer_instance_status_name'),
        SearchField.set(name='Type', key='data.network_usage_type'),
        SearchField.set(name='Domain', key='data.domain_name'),
        SearchField.set(name='IPs', key='data.load_balancer_ip_list'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(instance_total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_type_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_lb})
]
