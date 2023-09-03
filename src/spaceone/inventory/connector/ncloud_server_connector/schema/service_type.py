import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

instance_total_count_conf = os.path.join(current_dir, 'widget/instance_total_count.yaml')

cst_server = CloudServiceTypeResource()
cst_server.name = 'Server'
cst_server.provider = 'ncloud'
cst_server.group = 'Compute'
cst_server.labels = []
cst_server.service_code = 'ncloudServer'
cst_server.is_primary = True
cst_server.is_major = True
cst_server.tags = {
    'spaceone:icon': f'{ASSET_URL}/Server.svg',
}

cst_server._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.server_name'),
        TextDyField.data_source('Status', 'data.server_instance_status_name'),
        TextDyField.data_source('Private IP', 'data.private_ip'),
        TextDyField.data_source('vCore', 'data.cpu_count'),
        SizeField.data_source('Memory', 'data.memory_size', type="size", options={"source_unit": "BYTES", "display_unit":"GB"}),
        TextDyField.data_source('Instance Type', 'data.server_instance_type.code_name'),
        TextDyField.data_source('Image', 'data.server_image_name'),
        DateTimeDyField.data_source("Created", "data.create_date")
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
