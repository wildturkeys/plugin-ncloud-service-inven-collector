from spaceone.core.manager import BaseManager
from spaceone.inventory.model.compute import Compute
from spaceone.inventory.model.aws import AWS
from spaceone.inventory.model.os import OS
from spaceone.inventory.model.hardware import Hardware
from spaceone.inventory.connector.ncloud_connector import NCloudConnector


class NCloudServerManager(BaseManager):

    def __init__(self, params, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.server_connector: NCloudConnector = NCloudConnector()

    def list_resources(self):
        return []