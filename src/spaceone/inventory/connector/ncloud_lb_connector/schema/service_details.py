from schematics.types import ModelType, PolyModelType, StringType
from spaceone.inventory.libs.schema.resource import CloudServiceMeta, CloudServiceResource, CloudServiceResponse
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, \
    SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, SimpleTableDynamicLayout, \
    TableDynamicLayout

# TAB
details = ItemDynamicLayout.set_fields('Details', fields=[
    TextDyField.data_source('Name', 'data.load_balancer_name'),

    EnumDyField.data_source('Type', 'data.network_usage_type.code_name',
                            default_badge={'indigo.500': ['Public'],
                                           'coral.600': ['Private']}
                            ),
    TextDyField.data_source('Domain', 'data.domain_name'),
    EnumDyField.data_source('Status', 'data.load_balancer_instance_status_name',
                            default_state={
                                'safe': ['used', 'using', 'created'],
                                'available': ['initialized', 'creating',
                                              'repairing', 'using'],
                                'warning': ['disusing', 'changing'],
                                'disable': ['terminated']}),
    TextDyField.data_source('VIP', 'data.virtual_ip'),
    TextDyField.data_source('Algorithm', 'data.load_balancer_algorithm_type.code_name'),
    TextDyField.data_source('Certificate', 'data.certificate_name'),
    TextDyField.data_source('Http Keep Alive', 'data.is_http_keep_alive'),
    DateTimeDyField.data_source("Created", "data.create_date")
])

server_instances = TableDynamicLayout.set_fields('Servers', root_path='data.load_balanced_server_instance_list',
                                                 fields=[
                                                     TextDyField.data_source('L7 Health Check Path',
                                                                             'l7_health_check_path'),
                                                     TextDyField.data_source('LB Port', 'load_balancer_port'),
                                                     TextDyField.data_source('Server Port', 'server_port'),
                                                     EnumDyField.data_source('Protocol', 'protocol_type.code_name',
                                                                             default_outline_badge=['http', 'https',
                                                                                                    'udp', 'tcp',
                                                                                                    'icmp']),
                                                     TextDyField.data_source('Proxy Protocol', 'proxy_protocol_use_yn'),
                                                     EnumDyField.data_source('LB Status', 'server_status',
                                                                             default_badge={'indigo.500': ['true'],
                                                                                            'coral.600': ['false']}
                                                                             ),
                                                     TextDyField.data_source('ID', 'server_instance_no', reference={
                                                         "resource_type": "inventory.CloudService",
                                                         "reference_key": "reference.resource_id"}),
                                                     TextDyField.data_source('Name', 'server_name'),
                                                     EnumDyField.data_source('Server Status',
                                                                             'server_instance_status_name',
                                                                             default_state={
                                                                                 'safe': ['running'],
                                                                                 'available': ['init', 'creating',
                                                                                               'booting', 'setting up',
                                                                                               'changingSpec'],
                                                                                 'warning': ['warning', 'rebooting',
                                                                                             'hard rebooting',
                                                                                             'shutting down',
                                                                                             'hard shutting down',
                                                                                             'terminating', 'copying',
                                                                                             'repairing', ],
                                                                                 'disable': ['stopped']}
                                                                             ),

                                                 ])

rules = TableDynamicLayout.set_fields('Rules', root_path='data.load_balancer_rule_list', fields=[
    TextDyField.data_source('Certificate', 'certificate_name'),
    TextDyField.data_source('L7 Health Check Path', 'l7_health_check_path'),
    TextDyField.data_source('LB Port', 'load_balancer_port'),
    TextDyField.data_source('Protocol', 'protocol_type.code_name'),
    TextDyField.data_source('Proxy Protocol', 'proxy_protocol_use_yn'),
    TextDyField.data_source('Port', 'server_port'),
])

SERVICE_DETAILS = CloudServiceMeta.set_layouts([details, server_instances, rules])
