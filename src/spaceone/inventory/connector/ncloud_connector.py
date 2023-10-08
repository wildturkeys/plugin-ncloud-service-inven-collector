import logging

from spaceone.core.connector import BaseConnector
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.schema.resource import CloudServiceResponse, CloudServiceResource, ReferenceModel
from typing import Any, List
from schematics import Model
from schematics.types import DateTimeType

_LOGGER = logging.getLogger(__name__)

DATETIME_KEYS: List[str] = ['uptime','create_date']

class NCloudBaseConnector(BaseConnector):
    _ncloud_cls: Any = None
    _ncloud_api_v2: Any = None
    _ncloud_configuration = None

    def __init__(self, *args, **kwargs):

        self._ncloud_configuration = self._ncloud_cls.Configuration()

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

    def _convert_cloud_service_response(self, objs: List):

        for obj in objs:

            csr_dic = { "data": obj,
                        "cloud_service_group": self.cloud_service_group,
                        "cloud_service_type": self.cloud_service_type }

            if obj.get("region_code"):
                csr_dic["region_code"] = obj.get("region_code")

            if obj.get("name"):
                csr_dic["name"] = obj.get("name")

            if hasattr(obj, "reference"):
                csr_dic["reference"] = ReferenceModel(obj.reference())

            yield CloudServiceResponse({'resource': CloudServiceResource(csr_dic)})

    def _create_model_obj(self, model_cls: Model, resource: Any, **kwargs) -> Model:

        model_obj = model_cls()

        if isinstance(resource, dict):
            resource_dic = resource
        else:
            resource_dic = resource.to_dict()

        for key, value in resource_dic.items():
            if hasattr(model_obj, key):
                if key in DATETIME_KEYS and value:
                    dt_value = DateTimeType().to_native(value)
                    setattr(model_obj, key, dt_value)
                else:
                    setattr(model_obj, key, value)

        return model_obj