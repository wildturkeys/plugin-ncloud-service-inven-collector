import logging

import ncloud_server
import ncloud_loadbalancer
from ncloud_server.api.v2_api import V2Api as Server_V2Api
from ncloud_loadbalancer.api.v2_api import V2Api as Loadbalancer_V2Api

from spaceone.core.error import *
from spaceone.core import utils
from spaceone.core.connector import BaseConnector
from spaceone.inventory.conf.cloud_service_conf import *
from typing import Any

_LOGGER = logging.getLogger(__name__)
DEFAULT_REGION = 'KR-KOREA-1'

SERVICE_CLASS = {

    "Server": {"cls": ncloud_server,
               "api_cls": Server_V2Api},
    "Loadbalancer": {"cls": ncloud_loadbalancer,
                     "api_cls": Loadbalancer_V2Api}
}

DEFAULT_API_RETRIES = 10


class NCloudConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        self.ncloud_client = None

    def verify(self, secret_data, region_name):
        self.set_connect(secret_data, region_name)
        return "ACTIVE"

    def set_connect(self, secret_data: dict, region_name=DEFAULT_REGION, service_name='Server'):
        self.ncloud_client = self.get_api_client(secret_data, service_name)

    def get_api_client(self, service_name: str, secret_data: dict):

        if service_name in SERVICE_CLASS:

            service = SERVICE_CLASS[service_name]

            service_cls = service.get('cls')
            service_api_cls = service.get('cls_api')

            if service_cls:
                configuration = service_cls.Configuration()
                # to do : modify key name
                configuration.access_key = secret_data['aws_access_key_id']
                configuration.secret_key = secret_data['aws_secret_access_key']

                return service_api_cls(service_api_cls.ApiClient(configuration))
        raise
