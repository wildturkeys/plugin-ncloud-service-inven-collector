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

    def verify(self, secret_data):
        """ Check connection
        """
        ncloud_connector: NCloudConnector = self.locator.get_connector('NCloudConnector')
        ncloud_connector.set_connect(secret_data)
        r = ncloud_connector.verify(secret_data)
        # ACTIVE/UNKNOWN
        return r

    def list_regions(self, secret_data, region_name):
        ncloud_connector: NCloudConnector = self.locator.get_connector('NCloudConnector')
        ncloud_connector.set_client(secret_data, region_name)

        return ncloud_connector.list_regions()

    @property
    def managers(self):
        return []

    def set_managers(self, ncloud_connector: NCloudConnector):
        return []

    def list_resources(self, params):

        total_err_resources = []

        ncloud_connector: NCloudConnector = self.locator.get_connector('NCloudConnector')
        ncloud_connector.managers(**params)

        try:

            for manager in self.managers:
                yield manager.list_resources(params)

        except Exception as e:
            _LOGGER.error(f'{e}')

            if type(e) is dict:
                error_resource_response = ErrorResourceResponse({'message': json.dumps(e)})
            else:
                error_resource_response = ErrorResourceResponse({'message': str(e)})

            total_err_resources.append(error_resource_response)
            return total_err_resources


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


