from spaceone.core.manager import BaseManager
from spaceone.inventory.connector.ncloud_connector import NCloudConnector
import ncloud_server


class NCloudServerManager(BaseManager):

    def __init__(self, params, **kwargs):
        super().__init__(**kwargs)

        self.params = params

        if kwargs.get('connector'):
            self.server_connector: NCloudConnector = kwargs.get('connector')

    def list_resources(self):

        get_server_instance_list_request = ncloud_server.GetServerInstanceListRequest()

        return self.server_connector.get_server_instance_list(get_server_instance_list_request)

