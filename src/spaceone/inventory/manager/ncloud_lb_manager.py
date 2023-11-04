from spaceone.inventory.manager.ncloud_manager import NCloudManager


class LbConnectorManager(NCloudManager):
    connector_name = 'LbConnector'

class LbVPCConnectorManager(NCloudManager):
    connector_name = 'LbVPCConnector'
