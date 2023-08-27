__all__ = ['CollectorManager']

import time
import json
import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.connector import EC2Connector
from spaceone.inventory.connector import NCloudConnector
from spaceone.inventory.manager.ec2 import EC2InstanceManager, AutoScalingGroupManager, LoadBalancerManager, \
    DiskManager, NICManager, VPCManager, SecurityGroupManager, CloudWatchManager

from spaceone.inventory.manager.ncloud import NCloudServerManager

from spaceone.inventory.manager.metadata.metadata_manager import MetadataManager
from spaceone.inventory.model.server import Server, ReferenceModel
from spaceone.inventory.model.region import Region
from spaceone.inventory.model.cloudtrail import CloudTrail
from spaceone.inventory.model.cloud_service_type import CloudServiceType
from spaceone.inventory.model.resource import ErrorResourceResponse, ServerResourceResponse
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.utils import convert_tags


_LOGGER = logging.getLogger(__name__)


class CollectorManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def verify(self, secret_data, region_name):
        """ Check connection
        """
        ncloud_connector = self.locator.get_connector('NCloudConnector')
        r = ncloud_connector.verify(secret_data, region_name)
        # ACTIVE/UNKNOWN
        return r

    def list_regions(self, secret_data, region_name):
        ncloud_connector: NCloudConnector = self.locator.get_connector('NCloudConnector')
        ncloud_connector.set_client(secret_data, region_name)

        return ncloud_connector.list_regions()

    def list_instances(self, params):
        servers = []
        errors = []

        ncloud_connector: EC2Connector = self.locator.get_connector('NCloudConnector')
        ncloud_connector.set_client(params['secret_data'], params['region_name'])

        meta_manager: MetadataManager = MetadataManager()
        region_name = params.get("region_name", '')

        server_manager = NCloudServerManager(params, connector=ncloud_connector)

        return servers, errors

    def list_resources(self, params):
        start_time = time.time()
        total_resources = []

        ncloud_connector: EC2Connector = self.locator.get_connector('NCloudConnector')
        ncloud_connector.set_client(params['secret_data'], params['region_name'])

        server_manager = NCloudServerManager(params, connector=ncloud_connector)

        try:
            resources = server_manager.list_instances(params)
            total_resources.extend(resources)

            _LOGGER.debug(f'[list_resources] [{params["region_name"]}] Finished {time.time() - start_time} Seconds')

            return total_resources

        except Exception as e:
            _LOGGER.error(f'[list_resources] [{params["region_name"]}] {e}')

            if type(e) is dict:
                error_resource_response = ErrorResourceResponse({'message': json.dumps(e)})
            else:
                error_resource_response = ErrorResourceResponse({'message': str(e)})

            total_resources.append(error_resource_response)
            return total_resources


    @staticmethod
    def list_cloud_service_types():
        meta_manager: MetadataManager = MetadataManager()

        cloud_service_type = {
            '_metadata': meta_manager.get_cloud_service_type_metadata(),
            'tags': {
                'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-ec2.svg',
            }
        }
        return [CloudServiceType(cloud_service_type, strict=False)]

    @staticmethod
    def get_region_from_result(resource):
        match_region_info = REGION_INFO.get(getattr(resource, 'region_code', None))

        if match_region_info is not None:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': resource.region_code
            })

            return Region(region_info, strict=False)

        return None
