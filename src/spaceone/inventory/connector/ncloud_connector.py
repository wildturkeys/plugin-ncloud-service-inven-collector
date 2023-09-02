import logging

from spaceone.core.connector import BaseConnector
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.schema.resource import CloudServiceResponse, CloudServiceResource
from typing import Any, List

_LOGGER = logging.getLogger(__name__)
DEFAULT_REGION = 'KR-KOREA-1'
DEFAULT_API_RETRIES = 10


class NCloudBaseConnector(BaseConnector):
    _ncloud_cls: Any = None
    _ncloud_api: Any = None
    _ncloud_api_v2: Any = None
    _ncloud_configuration = None

    def __init__(self, *args, **kwargs):

        if self._ncloud_cls and kwargs.get("secret_data") and self._ncloud_configuration:

            secret_data = kwargs.get("secret_data")
            self._ncloud_configuration.access_key = secret_data.get("access_key")
            self._ncloud_configuration.secret_key = secret_data.get("secret_key")

    @property
    def api_client(self):
        return self._ncloud_cls.ApiClient(self._ncloud_configuration)

    @property
    def api_client_v2(self):
        return self._ncloud_api_v2(self.api_client)

    def get_resources(self) -> List[CloudServiceResponse]:
        raise NotImplementedError()


    def collect_data(self):
        return self.get_resources()


    def set_cloud_service_types(self):
        return self.cloud_service_types

    def collect_data_by_region(self, service_name, region_name, collect_resource_info):
        '''
        collect_resource_info = {
            'request_method': self.request_something_like_data,
            'resource': ResourceClass,
            'response_schema': ResponseClass,
            'kwargs': {}
        }
        '''
        resources = []
        additional_data = ['name', 'type', 'size', 'launched_at']

        try:
            for collected_dict in collect_resource_info['request_method'](region_name,
                                                                          **collect_resource_info.get('kwargs', {})):
                data = collected_dict['data']

                if getattr(data, 'resource_type', None) and data.resource_type == 'inventory.ErrorResource':
                    # Error Resource
                    resources.append(data)
                else:

                    resource_dict = {
                        'data': data,
                        'account': collected_dict.get('account'),
                        'instance_size': float(collected_dict.get('instance_size', 0)),
                        'instance_type': collected_dict.get('instance_type', ''),
                        'launched_at': str(collected_dict.get('launched_at', '')),
                        'tags': collected_dict.get('tags', {}),
                        'region_code': region_name
                    }

                    for add_field in additional_data:
                        if add_field in collected_dict:
                            resource_dict.update({add_field: collected_dict[add_field]})

                    resources.append(collect_resource_info['response_schema'](
                        {'resource': collect_resource_info['resource'](resource_dict)}))
        except Exception as e:
            resource_id = ''
            error_resource_response = self.generate_error(region_name, resource_id, e)
            resources.append(error_resource_response)

        return resources


