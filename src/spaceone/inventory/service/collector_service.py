import json
import time
import logging
import concurrent.futures

from spaceone.core.service import *
from spaceone.inventory.manager.collector_manager import CollectorManager
from spaceone.inventory.model.resource import CloudServiceTypeResourceResponse, ServerResourceResponse, \
    RegionResourceResponse, ErrorResourceResponse
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.collector_manager: CollectorManager = self.locator.get_manager('CollectorManager')

    @transaction
    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES,
            'supported_schedules': SUPPORTED_SCHEDULES
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """ verify options capability
        Args:
            params
              - options
              - secret_data: may be empty dictionary

        Returns:

        Raises:
             ERROR_VERIFY_FAILED:
        """
        manager = self.locator.get_manager('CollectorManager')
        secret_data = params['secret_data']
        active = manager.verify(secret_data)

        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def collect(self, params):
        """ Get quick list of resources
        Args:
            params:
                - options
                - secret_data
                - filter

        Returns: list of resources
        """

        start_time = time.time()
        # To Do
        resource_regions = []

        for cloud_service_type in self.collector_manager.list_cloud_service_types():
            yield CloudServiceTypeResourceResponse({'resource': cloud_service_type})

        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_CONCURRENT) as executor:

            future_executors: list = [executor.submit(self.collector_manager.list_resources, **params)]

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    yield result

        for resource_region in resource_regions:
            yield RegionResourceResponse({'resource': resource_region})

        _LOGGER.debug(f'[collect] TOTAL FINISHED {time.time() - start_time} Sec')


    @staticmethod
    def _check_query(query):
        """
        Args:
            query (dict): example
                  {
                      'instance_id': ['i-123', 'i-2222', ...]
                      'instance_type': 'm4.xlarge',
                      'region_name': ['aaaa']
                  }
        If there is region_name in query, this indicates searching only these regions
        """

        instance_ids = []
        filters = []
        region_name = []
        for key, value in query.items():
            if key == 'instance_id' and isinstance(value, list):
                instance_ids = value
            elif key == 'region_name' and isinstance(value, list):
                region_name.extend(value)
            else:
                if not isinstance(value, list):
                    value = [value]

                if len(value):
                    filters.append({'Name': key, 'Values': value})

        return filters, instance_ids, region_name
