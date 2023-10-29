from spaceone.inventory.libs.schema.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceMeta

# TAB
details = ItemDynamicLayout.set_fields('Details', fields=[
    EnumDyField.data_source('Platform', 'data.platform_code', default_badge={
        'indigo.500': ['classic'], 'coral.600': ['vpc']
    }),
    EnumDyField.data_source('Type', 'data.load_balancer_network_type',
                            default_badge={'indigo.500': ['Public'],
                                           'coral.600': ['Private']}
                            ),
    TextDyField.data_source('Domain', 'data.load_balancer_domain'),
    EnumDyField.data_source('Status', 'data.load_balancer_instance_status_name',
                            default_state={
                                'safe': ['used', 'using', 'created', "running"],
                                'available': ['initialized', 'creating',
                                              'repairing', 'using'],
                                'warning': ['disusing', 'changing', 'terminating'],
                                'disable': ['terminated']}),
    ListDyField.data_source('IPs', 'data.load_balancer_ip_list'),
    DateTimeDyField.data_source("Created", "data.create_date")
])

listeners = TableDynamicLayout.set_fields('Listener', root_path='data.load_balancer_listener_list',
                                          fields=[
                                              EnumDyField.data_source('Protocol', 'protocol_type',
                                                                      default_outline_badge=['http', 'https',
                                                                                             'udp', 'tcp',
                                                                                             'icmp']),
                                              TextDyField.data_source('LB Port', 'load_balancer_instance_port'),
                                              TextDyField.data_source('Server Port', 'server_instance_port'),
                                              EnumDyField.data_source('LB Status',
                                                                      'load_balancer_instance_status_name',
                                                                      default_badge={'indigo.500': ['true', 'up'],
                                                                                     'coral.600': ['false', 'down']}
                                                                      ),
                                              TextDyField.data_source('L7 Health Check Path', 'health_check_path'),
                                              TextDyField.data_source('Server ID', 'server_instance_no', reference={
                                                  "resource_type": "inventory.CloudService",
                                                  "reference_key": "reference.resource_id"}),
                                              TextDyField.data_source('Server Name', 'server_instance_name'),
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
    EnumDyField.data_source('Protocol', 'protocol_type.code_name',
                            default_outline_badge=['http', 'https',
                                                   'udp', 'tcp',
                                                   'icmp']
                            ),
    TextDyField.data_source('Proxy Protocol', 'proxy_protocol_use_yn'),
    TextDyField.data_source('Port', 'server_port'),
])

SERVICE_DETAILS = CloudServiceMeta.set_layouts([details, listeners])
