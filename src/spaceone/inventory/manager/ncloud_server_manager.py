from spaceone.inventory.manager.ncloud_manager import NCloudManager


class ServerConnectorManager(NCloudManager):
    connector_name = 'ServerConnector'


class ServerVPCConnectorManager(NCloudManager):
    connector_name = 'ServerVPCConnector'
