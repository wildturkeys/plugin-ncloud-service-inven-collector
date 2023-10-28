from spaceone.inventory.manager.ncloud_manager import NCloudManager


class NasConnectorManager(NCloudManager):
    connector_name = 'NasConnector'


class NasVPCConnectorManager(NCloudManager):
    connector_name = 'NasVPCConnector'
