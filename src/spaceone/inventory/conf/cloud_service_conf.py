MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
DEFAULT_REGION = 'KR-KOREA-1'
FILTER_FORMAT = []
ASSET_URL = "https://chulgyujeon.github.io/images/icon"
CLOUD_SERVICE_GROUP_MAP = {
    'Server': 'ServerConnectorManager',
    'ServerVPC': 'ServerVPCConnectorManager',
    'Nas': 'NasConnectorManager',
    'LB': 'LbConnectorManager',
    'Block': 'BlockConnectorManager',
    'VPC': 'VpcConnectorManager'
}

VPC_AVAILABLE_REGION = ["KR", "SGN", "JPN"]

"""
{'region_list': [{'region_code': 'KR',
                  'region_name': 'Korea',
                  'region_no': '1'},
                 {'region_code': 'HK',
                  'region_name': 'HongKong',
                  'region_no': '3'},
                 {'region_code': 'SGN',
                  'region_name': 'Singapore(New)',
                  'region_no': '7'},
                 {'region_code': 'JPN',
                  'region_name': 'Japan(New)',
                  'region_no': '8'},
                 {'region_code': 'USWN',
                  'region_name': 'US-West(New)',
                  'region_no': '9'},
                 {'region_code': 'DEN',
                  'region_name': 'Germany(New)',
                  'region_no': '10'}],
"""

REGION_INFO = {
    'KR': {'name': 'Korea',
           'tags': {'latitude': '37.44910833', 'longitude': '126.9041972', 'continent': 'east asia', 'region_no': '1'},
           },
    'HK': {'name': 'HongKong',
           'tags': {'latitude': '22.396427', 'longitude': '114.109497', 'continent': 'east asia', 'region_no': '3'}
           },
    'SGN': {'name': 'Singapore',
            'tags': {'latitude': '1.352083', 'longitude': '103.819839', 'continent': 'south asia', 'region_no': '7'}
            },
    'JPN': {'name': 'Japan',
            'tags': {'latitude': '36.204823', 'longitude': '138.252930', 'continent': 'east asia', 'region_no': '8'}
            },
    'USWN': {'name': 'US-West',
             'tags': {'latitude': '34.052235', 'longitude': '-118.243683', 'continent': 'north america', 'region_no': '9'}
             },
    'DEN': {'name': 'Germany',
            'tags': {'latitude': '50.110924', 'longitude': '8.682127', 'continent': 'europe', 'region_no': '10'}
            }
}
