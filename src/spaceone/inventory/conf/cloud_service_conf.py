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
    'KR-KOREA-1': {'name': 'KR East (N. Virginia)',
                  'tags': {'latitude': '39.028760', 'longitude': '-77.458263', 'continent': 'north_america'}}
}