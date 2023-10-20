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

cst_nas_volume = CloudServiceTypeResource()
cst_nas_volume.name = 'Nas'
cst_nas_volume.provider = 'ncloud'
cst_nas_volume.group = 'Storage'
cst_nas_volume.labels = ['Storage']
cst_nas_volume.service_code = 'ncloudNas'
cst_nas_volume.is_primary = True
cst_nas_volume.is_major = True
cst_nas_volume.tags = {
    'spaceone:icon': f'{ASSET_URL}/Storage.svg',
}

cst_nas_volume._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Platform', 'data.platform_code', default_badge={
            'indigo.500': ['classic'], 'coral.600': ['vpc']
        }),
        TextDyField.data_source('Status', 'data.nas_volume_instance_status_name'),
        TextDyField.data_source('Instance Type', 'data.nas_volume_instance_status.code_name'),
        SizeField.data_source('Total Size', 'data.volume_total_size', type="size",
                              options={"source_unit": "BYTES", "display_unit": "GB"}),
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
