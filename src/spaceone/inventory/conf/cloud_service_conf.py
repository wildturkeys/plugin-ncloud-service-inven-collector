MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
DEFAULT_REGION = 'KR-KOREA-1'
FILTER_FORMAT = []
ASSET_URL = "https://chulgyujeon.github.io/images"
CLOUD_SERVICE_GROUP_MAP = {
    'Server': 'ServerConnectorManager'
}

REGION_INFO = {
    'KR': {'name': 'Korea',
           'tags': {'latitude': '37.44910833', 'longitude': '126.9041972', 'continent': 'east asia'}}
}