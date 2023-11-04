from spaceone.inventory.manager.ncloud_manager import NCloudManager


class BlockConnectorManager(NCloudManager):
    connector_name = 'BlockConnector'


class BlockVPCConnectorManager(NCloudManager):
    connector_name = 'BlockVPCConnector'
