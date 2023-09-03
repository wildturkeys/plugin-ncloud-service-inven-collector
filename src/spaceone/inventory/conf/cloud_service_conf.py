MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
DEFAULT_REGION = 'KR-KOREA-1'
FILTER_FORMAT = []

CLOUD_SERVICE_GROUP_MAP = {
    'Server': 'ServerConnectorManager'
}

REGION_INFO = {
    'KR': {'name': 'Korea',
           'tags': {'latitude': '126.734086', 'longitude': '127.269311', 'continent': 'east asia'}}
}