from schematics.types import ModelType, PolyModelType, StringType
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, \
    TableDynamicLayout


details = ItemDynamicLayout.set_fields('Details',fields=[
    TextDyField.data_source("No", "data.vpc_no"),
    TextDyField.data_source("Name", "data.vpc_name"),
    EnumDyField.data_source("Status","data.vpc_status.code.code",
                            default_state ={
                                'safe' : ['RUN'],
                                    'available':['CREATING','INIT'],
                                    'disable':['TERMTING' ]
                            }),
    DateTimeDyField.data_source("Created", "data.create_date"),
    TextDyField.data_source("region_code","data.region_code"),
    TextDyField.data_source("Ipv4 Cidr Block", "data.ipv4_cidr_block")

])

subnet = TableDynamicLayout.set_fields('Subnet', root_path='data.subnet',
                                       fields=[
                                           TextDyField.data_source('No', 'subnet_no'),
                                           TextDyField.data_source('Name', 'subnet_name'),
                                           # EnumDyField.data_source('Type', 'subnet_type.code_name',
                                           #                         default_badge={'indigo.500': ['Public'],
                                           #                                        'coral.600': ['Private']}
                                           #                         ),
                                           # EnumDyField.data_source('Type', 'usage_type.code_name',
                                           #                         default_outline_badge={'Normal','LoadBalancer', 'BareMetal', 'NatGateway'}),
                                           # EnumDyField.data_source('Subnet Status','subnet_status.code',
                                           #                         default_state={
                                           #                          'safe' : ['RUN'],
                                           #                          'available':['CREATING','INIT'],
                                           #                          'disable':['TERMTING' ] }),
                                           # DateTimeDyField.data_source("Created", "create_date"),


                                       ])

# 'vpc_status': {'code': 'RUN', 'code_name': 'run'}}
SERVICE_DETAILS = CloudServiceMeta.set_layouts([details, subnet])



