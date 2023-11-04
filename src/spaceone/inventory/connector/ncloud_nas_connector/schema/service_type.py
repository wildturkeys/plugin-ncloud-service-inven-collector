import os

from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField, \
    SizeField
from spaceone.inventory.libs.schema.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_instance_count_conf = os.path.join(current_dir, 'widget/total_instance_count.yaml')
total_volume_count_conf = os.path.join(current_dir, 'widget/total_volume_size.yaml')
total_snapshot_size_conf = os.path.join(current_dir, 'widget/total_snapshot_size.yaml')


count_by_volume_size_conf = os.path.join(current_dir, 'widget/count_by_volume_size.yaml')
count_by_project_conf = os.path.join(current_dir,'widget/count_by_project.yaml')
count_by_region_conf = os.path.join(current_dir,'widget/count_by_region.yaml')

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
        EnumDyField.data_source('Status', 'data.nas_volume_instance_status_name', default_state={
            'safe': ['created'],
            'disable': ['terminated']
        }),
        TextDyField.data_source('Instance Type', 'data.nas_volume_instance_status.code_name'),
        SizeField.data_source('Volume Size', 'data.volume_size', type="size",
                              options={"source_unit": "BYTES", "display_unit": "GB"}),
        DateTimeDyField.data_source("Created", "data.create_date")

    ],
    search=[
        SearchField.set(name='Status', key='data.nas_volume_instance_status_name'),
        SearchField.set(name='Instance Type', key='data.nas_volume_instance_status.code_name'),

        SearchField.set(name='Platform', key='data.platform_code'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_instance_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_volume_count_conf)),
        CardWidget.set(**get_data_from_yaml(total_snapshot_size_conf)),

        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_volume_size_conf))

    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_nas_volume})
]
