import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

instance_total_count_conf = os.path.join(current_dir, 'widget/instance_total_count.yaml')

cst_server = CloudServiceTypeResource()
cst_server.name = 'Server'
cst_server.provider = 'ncloud'
cst_server.group = 'Instance'
cst_server.labels = []
cst_server.service_code = 'ncloudServer'


cst_server._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.server_name'),
        TextDyField.data_source('Status', 'data.instance_status_name'),
        TextDyField.data_source('Private IP', 'data.private_ip'),
        TextDyField.data_source('vCore', 'data.cpu_count'),
        TextDyField.data_source('Memory', 'data.memory_size'),
        TextDyField.data_source('Image', 'data.server_image_name')
    ],
    search=[
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(instance_total_count_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_server})
]
