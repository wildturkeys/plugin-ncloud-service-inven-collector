import logging
import traceback
from typing import Any, List, Iterable, Type, Callable

import ncloud_server
import ncloud_vserver

from ncloud_server.api.v2_api import V2Api as ClassicV2Api
from ncloud_vserver.api.v2_api import V2Api as VpcV2Api

from spaceone.inventory.conf.cloud_service_conf import API_TYPE, API_TYPE_CLASSIC, API_TYPE_VPC

from schematics import Model
from schematics.types import DateTimeType
from spaceone.core.connector import BaseConnector

from spaceone.inventory.libs.schema.resource import CloudServiceResponse, CloudServiceResource, ReferenceModel

_LOGGER = logging.getLogger(__name__)

DATETIME_KEYS: List[str] = ['uptime', 'create_date']


class NCloudBaseConnector(BaseConnector):
    cloud_service_group = None
    cloud_service_type = None
    cloud_service_types = None
    cloud_service_details = None

    _ncloud_cls: Any = None
    _ncloud_api_v2: Any = None
    _ncloud_configuration = None
    _ncloud_region_configuration = None
    _api_exception_cls = None

    __api_type = API_TYPE_CLASSIC

    _regions = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_region(self, access_key, secret_key):

        if self.__api_type == API_TYPE_CLASSIC:
            self._set_classic_region(access_key, secret_key)

        elif self.__api_type == API_TYPE_VPC:
            self._set_vpc_region(access_key, secret_key)
        else:
            raise

        _LOGGER.info(self._regions)

    @property
    def api_type(self):
        return self.api_type

    @api_type.setter
    def api_type(self, api_type: str):
        if api_type not in API_TYPE:
            raise ValueError("Invalid api type")
        self.__api_type = api_type

    @property
    def regions(self) -> List:
        return self._regions

    @property
    def api_client(self):
        return self._ncloud_cls.ApiClient(self._ncloud_configuration)

    @property
    def api_client_v2(self):
        return self._ncloud_api_v2(self.api_client)

    def _set_configuration(self, access_key: str, secret_key: str):

        self._ncloud_configuration = self._ncloud_cls.Configuration()
        self._ncloud_configuration.access_key = access_key
        self._ncloud_configuration.secret_key = secret_key

        self._set_region(access_key, secret_key)

    def _set_classic_region(self, access_key: str, secret_key: str):

        _ncloud_region_configuration = ncloud_server.Configuration()
        _ncloud_region_configuration.access_key = access_key
        _ncloud_region_configuration.secret_key = secret_key

        client = ncloud_server.ApiClient(_ncloud_region_configuration)

        api = ClassicV2Api(client)
        get_region_list_request = ncloud_server.GetRegionListRequest
        response = api.get_region_list(get_region_list_request).to_dict()
        self._regions = response.get("region_list")

    def _set_vpc_region(self, access_key: str, secret_key: str):

        _ncloud_region_configuration = ncloud_vserver.Configuration()
        _ncloud_region_configuration.access_key = access_key
        _ncloud_region_configuration.secret_key = secret_key

        client = ncloud_vserver.ApiClient(_ncloud_region_configuration)

        api = VpcV2Api(client)
        get_region_list_request = ncloud_vserver.GetRegionListRequest
        response = api.get_region_list(get_region_list_request).to_dict()
        self._regions = response.get("region_list")

    def get_resources(self, **kwargs) -> List[CloudServiceResponse]:
        raise NotImplementedError()

    def collect_data(self) -> List[CloudServiceResponse]:

        access_key = self.secret_data.get("access_key")
        secret_key = self.secret_data.get("secret_key")

        self._set_configuration(access_key, secret_key)

        return self.get_resources()

    def _convert_cloud_service_response(self, objs: List) -> Iterable[CloudServiceResponse]:

        for obj in objs:

            csr_dic = {"data": obj,
                       "cloud_service_group": self.cloud_service_group,
                       "cloud_service_type": self.cloud_service_type}

            if hasattr(obj, "region_code"):
                csr_dic["region_code"] = obj.get("region_code")

            if hasattr(obj, "instance_type"):
                csr_dic["instance_type"] = obj.get("instance_type")

            if hasattr(obj, "instance_size"):
                csr_dic["instance_size"] = obj.get("instance_size")

            if hasattr(obj, "name"):
                csr_dic["name"] = obj.get("name")

            if self.cloud_service_details:
                csr_dic["metadata"] = self.cloud_service_details

            if hasattr(obj, "reference"):
                csr_dic["reference"] = ReferenceModel(obj.reference())

            yield CloudServiceResponse({'resource': CloudServiceResource(csr_dic)})

    @staticmethod
    def _set_obj_key_value(obj: Any, key: str, value: Any) -> None:
        setattr(obj, key, value)

    @staticmethod
    def _find_objs_by_key_value(target_obj_list: List, key, value) -> List:

        obj_list = []

        for obj in target_obj_list:
            if obj.get(key) == value:
                obj_list.append(obj)

        return obj_list

    @staticmethod
    def _create_model_obj(model_cls: Callable[[], Type[Model]], resource: Any, **kwargs) -> Type[Model]:

        model_obj = model_cls()

        ignore_keys = kwargs.get('ignore_keys', [])

        if isinstance(resource, dict):
            resource_dic = resource
        else:
            resource_dic = resource.to_dict()

        for key, value in resource_dic.items():

            if key not in ignore_keys and hasattr(model_obj, key):
                if key in DATETIME_KEYS and value:
                    dt_value = DateTimeType().to_native(value)
                    setattr(model_obj, key, dt_value)
                else:
                    setattr(model_obj, key, value)

        return model_obj

    def _list_ncloud_resources(self, request_api, request_model, response_key: str, response_model, **kwargs) -> List:

        try:

            resources_list = []

            response = request_api(request_model(**kwargs))
            response_dict = response.to_dict()

            if response_dict.get(response_key):

                for value in response_dict.get(response_key):
                    obj = self._create_model_obj(response_model, value)
                    resources_list.append(obj)

            return resources_list

        except self._api_exception_cls as e:
            _LOGGER.error(e)
            raise

        except Exception as e:
            _LOGGER.error(e)
            _LOGGER.error(traceback.format_exc())
            raise

    def _list_ncloud_raw_resources(self, request_api, request_model, response_key: str, **kwargs) -> List:

        try:

            response = request_api(request_model(**kwargs))

            return getattr(response, response_key)

        except self._api_exception_cls as e:
            _LOGGER.error(e)
            raise

        except Exception as e:
            _LOGGER.error(e)
            _LOGGER.error(traceback.format_exc())
            raise

    def _list_ncloud_raw_resources_ex(self, ncloud_cls, v2_api_cls, exception_cls, request_api: str, request_model,
                                      response_key: str,
                                      **kwargs) -> List:

        try:

            configuration = ncloud_cls.Configuration()
            configuration.access_key = self.secret_data.get('access_key')
            configuration.secret_key = self.secret_data.get('secret_key')

            client = ncloud_cls.ApiClient(configuration)

            api = v2_api_cls(client)
            request_api = getattr(api, request_api)
            api_response = request_api(request_model(**kwargs))

            return getattr(api_response, response_key)


        except exception_cls as e:
            _LOGGER.error(e)
            raise

        except Exception as e:
            _LOGGER.error(e)
            _LOGGER.error(traceback.format_exc())
            raise
