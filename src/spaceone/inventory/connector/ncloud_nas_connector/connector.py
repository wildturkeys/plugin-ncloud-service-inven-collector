import logging
import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException
from spaceone.inventory.connector.ncloud_nas_connector.schema.data import NasVolume
from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_nas_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse, CloudServiceResource
from typing import Iterator, List

_LOGGER = logging.getLogger(__name__)


class NasConnector(NCloudBaseConnector):

    cloud_service_group = 'Storage'
    cloud_service_type = 'Nas'
    cloud_service_types = CLOUD_SERVICE_TYPES

    _ncloud_cls = ncloud_server
    _ncloud_api_v2 = V2Api

    def get_resources(self) -> List[CloudServiceResponse]:

        resources = []
        resources.extend(self.cloud_service_types)
        resources.extend(self._convert_cloud_service_response(self.list_instances()))

        return resources

    def list_instances(self) -> Iterator:

        try:

            response = self.api_client_v2.get_nas_volume_instance_list(ncloud_server.GetNasVolumeInstanceListRequest())
            response_dict = response.to_dict()

            if response_dict.get("nas_volume_instance_list"):

                for nas_volume_instance in response_dict.get("nas_volume_instance_list"):
                    region_code = nas_volume_instance.get("region").get("region_code")

                    # 고쳐야 함
                    nas_volume = NasVolume(self._create_model_obj(NasVolume, nas_volume_instance))
                    nas_volume.region_code = region_code

                    yield nas_volume


        except ApiException as e:
            logging.error(e)
            raise