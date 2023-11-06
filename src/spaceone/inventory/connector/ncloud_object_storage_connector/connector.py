import logging
from typing import Iterator, List, Dict
from typing import Optional, Type
import boto3

import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException

from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_object_storage_connector.schema.data import ObjectStorage, NcloudObjectStorage
from spaceone.inventory.connector.ncloud_object_storage_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_object_storage_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import API_TYPE_CLASSIC

_LOGGER = logging.getLogger(__name__)

class ObjectStorageConnector(NCloudBaseConnector):
    cloud_service_group = 'Storage'
    cloud_service_type = 'Object Storage'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_server
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException
    _object_storage_client = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_type = API_TYPE_CLASSIC
        self._object_storage_client = boto3.client(service_name='s3',
                     endpoint_url="https://kr.object.ncloudstorage.com",
                     aws_access_key_id=self.secret_data.get("access_key"),
                     aws_secret_access_key=self.secret_data.get("secret_key")
                     )

    def get_resources(self) -> List[Type[CloudServiceResponse]]:

        resources = []
        resources.extend(self.cloud_service_types)

        for region in ['kr','us']:
            resources.extend(self._convert_cloud_service_response(self.list_instances(
                NcloudObjectStorage,ObjectStorage, region=region)))

        return resources

    def list_instances(self,ncloud_object_storage_cls:Type[NcloudObjectStorage],
                       response_object_storage_cls:Type[ObjectStorage], region, **kwargs) -> List[ObjectStorage]:

        try:
            resources = []

            response = self._object_storage_client.list_buckets()
            if response.get('Buckets'):
                for object_storage_instance in response.get('Buckets', []):
                    object_storage = response_object_storage_cls(self._create_model_obj(
                        ncloud_object_storage_cls, object_storage_instance))

                    # yield object_storage
                    resources.append(object_storage)
            return resources
        except ApiException as e:
            logging.error(e)
            raise