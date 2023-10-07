import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

instance_total_count_conf = os.path.join(current_dir, 'widget/instance_total_count.yaml')

cst_nas_volume = CloudServiceTypeResource()
cst_nas_volume.name = 'Nas'
cst_nas_volume.provider = 'ncloud'
cst_nas_volume.group = 'Storage'
cst_nas_volume.labels = []
cst_nas_volume.service_code = 'ncloudNas'
cst_nas_volume.is_primary = True
cst_nas_volume.is_major = True
cst_nas_volume.tags = {
    # 바꿔야 함
    'spaceone:icon': f'{ASSET_URL}/Server.svg',
}

# 바꿔야 함
cst_nas_volume._metadata = CloudServiceTypeMeta.set_meta(
    fields=[

        TextDyField.data_source('Name', 'data.volume_name'),
        TextDyField.data_source('Status', 'data.nas_volume_instance_status_name'),
        # TextDyField.data_source('Private IP', 'data.private_ip'),
        # TextDyField.data_source('vCore', 'data.cpu_count'),
        # SizeField.data_source('Memory', 'data.memory_size', type="size", options={"source_unit": "BYTES", "display_unit":"GB"}),
        TextDyField.data_source('Instance Type', 'data.nas_volume_instance_status.code_name'),
        TextDyField.data_source('Total Size', 'data.volume_instance_status.nas_volume_total_size'),

        DateTimeDyField.data_source("Created", "data.create_date")

    ],
    search=[
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(instance_total_count_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_nas_volume})
]



