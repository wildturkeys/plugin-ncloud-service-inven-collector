import os

from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField, \
    SizeField
from spaceone.inventory.libs.schema.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))


cst_cloud_db = CloudServiceTypeResource()
cst_cloud_db.name = 'CloudDB'
cst_cloud_db.provider = 'ncloud'
cst_cloud_db.group = 'Database'
cst_cloud_db.labels = ['Database']
cst_cloud_db.service_code = 'ncloudCloudDB'
cst_cloud_db.is_primary = True
cst_cloud_db.is_major = True
cst_cloud_db.tags = {
    'spaceone:icon': f'{ASSET_URL}/Storage.svg',
}


cst_cloud_db._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('No', 'data.cloud_db_instance_no')

    ],
    search=[

    ],
    widget=[

    ]



)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_cloud_db})
]