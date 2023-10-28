import logging
from typing import Iterator, List
from typing import Type

import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException

from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_nas_connector.schema.data import NcloudNasVolume, NasVolume, NCloudServer
from spaceone.inventory.connector.ncloud_nas_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_nas_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
from spaceone.inventory.conf.cloud_service_conf import API_TYPE_CLASSIC

_LOGGER = logging.getLogger(__name__)


class NasConnector(NCloudBaseConnector):
    cloud_service_group = 'Storage'
    cloud_service_type = 'Nas'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_server
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_type = API_TYPE_CLASSIC

    def get_resources(self) -> List[CloudServiceResponse]:

        resources = []

        for region in self.regions:

            resources.extend(
                self._convert_cloud_service_response(self.list_nas_volume_instances(NcloudNasVolume,
                                                                                    NasVolume,
                                                                                    region_no=region.get('region_code') ))
            )
        # resources.extend(self._convert_cloud_service_response(self.list_instances()))

        return resources

    def list_nas_volume_instances(self, ncloud_nas_volume_cls:Type[NcloudNasVolume],
                                  response_nas_volume_cls: Type[NasVolume], **kwargs) -> Iterator:

        try:

            response = self.api_client_v2.get_nas_volume_instance_list(
                self._ncloud_cls.GetNasVolumeInstanceListRequest(**kwargs))
            response_dict = response.to_dict()

            if response_dict.get("nas_volume_instance_list"):

                for nas_volume_instance in response_dict.get("nas_volume_instance_list"):
                    region_code = nas_volume_instance.get("region").get("region_code")

                    # 고쳐야 함
                    nas_volume = response_nas_volume_cls(self._create_model_obj(ncloud_nas_volume_cls, nas_volume_instance))
                    nas_volume.region_code = region_code
                    nas_volume.zone_code = nas_volume_instance.get("zone").get("zone_code")
                    nas_volume.volume_size_gb = round(nas_volume.volume_size / 1024 / 1024 / 1024)
                    nas_volume.snapshot_volume_size_gb = round(nas_volume.snapshot_volume_size / 1024 / 1024 / 1024)


                    nas_volume.nas_volume_server_instance_list = self._list_server_instances(
                        nas_volume_instance.get("nas_volume_server_instance_list"))

                    yield nas_volume


        except ApiException as e:
            logging.error(e)
            raise

    def _list_server_instances(self, server_instances, **kwargs) -> List[Type[NCloudServer]]:

        resources_list = []

        for server_instance in server_instances:
            server = NCloudServer(self._create_model_obj(NCloudServer, server_instance))
            resources_list.append(server)

        return resources_list
