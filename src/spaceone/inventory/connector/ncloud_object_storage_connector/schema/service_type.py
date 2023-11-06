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
count_by_project_conf = os.path.join(current_dir,'widget/count_by_project.yaml')


cst_object_storage = CloudServiceTypeResource()
cst_object_storage.name = 'Object Storage'
cst_object_storage.provider = 'ncloud'
cst_object_storage.group = 'Storage'
cst_object_storage.labels = ['Storage']
cst_object_storage.service_code = 'ncloudObjectStorage'
cst_object_storage.is_primary = True
cst_object_storage.is_major = True
cst_object_storage.tags = {
    'spaceone:icon': f'{ASSET_URL}/Storage.svg',
}

cst_object_storage._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        DateTimeDyField.data_source('Created','data.CreationDate')

],
    search=[

    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_instance_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf)),

    ]

)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_object_storage})
]
