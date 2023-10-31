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
# total_cpu_count_conf = os.path.join(current_dir, 'widget/total_cpu_count.yaml')

count_by_region_conf = os.path.join(current_dir,'widget/count_by_region.yaml')
count_by_project_conf = os.path.join(current_dir,'widget/count_by_project.yaml')
# count_by_storage_type_conf = os.path.join(current_dir,'widget/count_by_storage_type.yaml')


cst_cloud_db = CloudServiceTypeResource()
cst_cloud_db.name = 'CloudDB'
cst_cloud_db.provider = 'ncloud'
cst_cloud_db.group = 'Database'
cst_cloud_db.labels = ['Database']
cst_cloud_db.service_code = 'ncloudCloudDB'
cst_cloud_db.is_primary = True
cst_cloud_db.is_major = True
cst_cloud_db.tags = {
    'spaceone:icon': f'{ASSET_URL}/Database.svg',
}


cst_cloud_db._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Platform', 'data.platform_code', default_badge={
            'indigo.500': ['classic'], 'coral.600': ['vpc']
        }),

        TextDyField.data_source('Kind', 'data.db_kind_code',
                                default_outline_badge=['MYSQL', 'MSSQL',
                                                       'REDIS']),
        TextDyField.data_source('Cloud DB ID', 'data.cloud_db_instance_no'),
        TextDyField.data_source('Status','data.cloud_db_instance_status_name', default_state={
            'safe': ['created', 'running'], #확인필요
            'disable': ['terminated']
        }),
        DateTimeDyField.data_source("Created", "data.create_date"),
        TextDyField.data_source('Zone', 'data.zone.zone_name'),

    ],
    search=[

    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_instance_count_conf)),
        # CardWidget.set(**get_data_from_yaml(total_cpu_count_conf)),

        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf)),
        # ChartWidget.set(**get_data_from_yaml(count_by_storage_type_conf))
    ]



)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_cloud_db})
]