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


cst_vpc = CloudServiceTypeResource()
cst_vpc.name = 'VPC'
cst_vpc.provider = 'ncloud'
cst_vpc.group = 'Networking'
cst_vpc.labels = ['Network']
cst_vpc.service_code = 'ncloudVPC'
cst_vpc.is_primary = True
cst_vpc.is_major = True
cst_vpc.tags = {
    'spaceone:icon': f'{ASSET_URL}/Networking.svg',
}

cst_vpc._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name','data.vpc_name'),
        #TextDyField.data_source('No','data.vpc_no'),
        #TextDyField.data_source('Create', 'data.create_date'),
        # TextDyField.data_source('Status','data.vpc_status.code'
                               # default_state={
                                #    'safe':['RUN'],
                                 #   'available':['CREATING','INIT'],
                                  #  'disable':['TERMTING' ]
                                #}
                                # ),
        #TextDyField.data_source('Ipv4 Cidr Block', 'data.ipv4_cidr_block'),
        #TextDyField.data_source('Region','data.region_code')
    ],
    search=[
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(instance_total_count_conf))
    ]

)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_vpc})
]