import logging
from typing import Iterator, List, Dict
from typing import Optional, Type

import ncloud_vnas
from ncloud_vnas.api.v2_api import V2Api
from ncloud_vnas.rest import ApiException

from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_nas_connector.connector import NasConnector
from spaceone.inventory.connector.ncloud_nas_connector.schema.data import NCloudNasVolumeVPC, NasVolumeVPC
from spaceone.inventory.connector.ncloud_nas_connector.schema.service_details import SERVICE_DETAILS
from spaceone.inventory.connector.ncloud_nas_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse
# from spaceone.inventory.conf.cloud_service_conf import API_TYPE_VPC


_LOGGER = (logging.getLogger(__name__))


class NasVPCConnector(NasConnector):

    cloud_service_group = 'Storage'
    cloud_service_type = 'Nas'
    cloud_service_types = CLOUD_SERVICE_TYPES
    cloud_service_details = SERVICE_DETAILS

    _ncloud_cls = ncloud_vnas
    _ncloud_api_v2 = V2Api
    _api_exception_cls = ApiException

    def get_resources(self) -> List[CloudServiceResponse]:

        resources = []
        resources.extend(self.cloud_service_types)
        resources.extend(self._convert_cloud_service_response(self.list_instances()))

        return resources

    def list_instances(self) -> Iterator:

        try:

            response = self.api_client_v2.get_nas_volume_instance_list(ncloud_vnas.GetNasVolumeInstanceListRequest())
            response_dict = response.to_dict()

            if response_dict.get("nas_volume_instance_list"):

                for nas_volume_instance in response_dict.get("nas_volume_instance_list"):
                    # region_code = nas_volume_instance.get("region").get("region_code")

                    # 고쳐야 함
                    nas_volume = NasVolumeVPC(self._create_model_obj(NCloudNasVolumeVPC, nas_volume_instance))
                    # nas_volume.region_code = region_code
                    nas_volume.volume_size_gb = round(nas_volume.volume_size / 1024 / 1024 / 1024)
                    nas_volume.snapshot_volume_size_gb = round(nas_volume.snapshot_volume_size / 1024 / 1024 / 1024)



                    yield nas_volume

        except ApiException as e:
            logging.error(e)
            raise

        except Exception as e:
            import traceback
            logging.error(traceback.format_exc())
            logging.error(e)
            raise


    # def get_resources(self) -> List[Type[CloudServiceResponse]]:
    #
    #     resources = []

        # for region in self.regions:

            # region_code = region.get('region_code')

            # self._access_control_rules_dict \
            #     = dict(self._access_control_rules_dict,
            #            **self._sort_access_control_group_rules_group_by_acg_no(region_code=region_code))
            #
            # for image_product in self._list_image_product(region_code=region_code):
            #     self._server_images_dict[image_product.product_code] = image_product.product_name

            # resources.extend(
            #     self._convert_cloud_service_response(self.list_nas_volume_instances(NcloudNasVolume,
            #                                                                     NasVolume,
            #                                                                     region_code =region.get(
            #                                                                         'region_code'))))

        # return resources

    # def list_nas_volume_instances(self, ncloud_nas_volume_cls: Type[NcloudNasVolume],
    #                               response_nas_volume_cls: Type[NasVolume], **kwargs) -> Iterator:
    #
    #     response = self.api_client_v2.get_vnas_instance_list(
    #         self._ncloud_cls.GetNasVolumeInstanceListRequest(**kwargs))
    #     response_dict = response.to_dict()
    #
    #
    #     if response_dict.get("nas_volume_instance_list"):
    #
    #         for nas_volume_instance in response_dict.get("nas_volume_instance_list"):
    #
    #             nas_volume = response_nas_volume_cls(self._create_model_obj(ncloud_nas_volume_cls, nas_volume_instance))
    #             # nas_volume.region_code = nas_volume_instance.get("region_cde")
    #
    #
    #             yield nas_volume
