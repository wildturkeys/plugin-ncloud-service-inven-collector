import logging
from typing import Iterator, List
from typing import Type

import ncloud_clouddb
from ncloud_clouddb.api.v2_api import V2Api
from ncloud_clouddb.rest import ApiException

from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_clouddb_connector.schema.data import NcloudCloudDB, CloudDB
from spaceone.inventory.connector.ncloud_clouddb_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_clouddb_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import API_TYPE_CLASSIC


_LOGGER = logging.getLogger(__name__)


class CloudDBConnector(NCloudBaseConnector):
    cloud_service_group = 'Database'
    cloud_service_type = 'CloudDB'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_clouddb
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_type = API_TYPE_CLASSIC


    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []
        resources.extend(self.cloud_service_types)

        for region in self.regions:
            resources.extend(
                self._convert_cloud_service_response(self.list_cloud_db_instances(NcloudCloudDB,
                                                                                  CloudDB,
                                                                                  db_kind_code='MYSQL')))

        return resources

    def list_cloud_db_instances(self, ncloud_cloud_db_cls:Type[NcloudCloudDB],
                                response_cloud_db_cls: Type[CloudDB], **kwargs) -> Iterator:

        response = self.api_client_v2.get_cloud_db_instance_list(
            self._ncloud_cls.GetCloudDBInstanceListRequest(**kwargs)
        )
        response_dict = response.to_dict()

        if response_dict.get("cloud_db_instance_list"):

            for cloud_db_instance in response_dict.get("cloud_db_instance_list"):
                region_code = cloud_db_instance.get("region").get("region_code")
                cloud_db = response_cloud_db_cls(self._create_model_obj(ncloud_cloud_db_cls, cloud_db_instance))
                cloud_db.region_code = region_code
                yield cloud_db

