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
DEFAULT_API_RETRIES = 10

SERVICE_CLASSES = {

    "Server": {"cls": ncloud_server,
               "api_cls": Server_V2Api},
    "Loadbalancer": {"cls": ncloud_loadbalancer,
                     "api_cls": Loadbalancer_V2Api}
}


class NCloudConnector(BaseConnector):

    _secret_data: dict = None
    _api_clients: dict = {}

    def __init__(self, *args, **kwargs):
        self._api_clients: None

    @property
    def api_clients(self):
        return self._api_clients

    def verify(self, secret_data, region_name=None):
        self.set_connect(secret_data)
        self.get_api_client('Server')
        return "ACTIVE"

    def set_connect(self, secret_data: dict):
        self._secret_data = secret_data
        self._generate_api_clients()

    def get_api_client(self, service_name: str):

        if self._api_clients:
            return self._api_clients.get(service_name)
        else:
            return None

    def _generate_api_clients(self):

        if not self.secret_data:
            raise

        for service_name, service_cls_info in SERVICE_CLASSES.items():

            service_api_cls = service_cls_info.get('cls_api')
            service_cls = service_cls_info.get('cls')
            configuration = self._get_configuration(service_cls)

            self.api_clients[service_name] = service_api_cls(service_api_cls.ApiClient(configuration))

    def _get_configuration(self, service_cls):

        configuration = service_cls.Configuration()

        # to do : modify key name
        configuration.access_key = self.secret_data.get('aws_access_key_id')
        configuration.secret_key = self.secret_data.get('aws_secret_access_key')

        return configuration

