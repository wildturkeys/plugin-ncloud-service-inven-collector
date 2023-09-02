import logging
import ncloud_server
from ncloud_server.api.v2_api import V2Api
from ncloud_server.rest import ApiException
from spaceone.inventory.connector.ncloud_server_connector.schema.data import Server
from spaceone.inventory.connector.ncloud_connector import NCloudBaseConnector
from spaceone.inventory.connector.ncloud_server_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.schema.resource import CloudServiceResponse, CloudServiceResource

_LOGGER = logging.getLogger(__name__)


class ServerConnector(NCloudBaseConnector):
    service_name = 'Server'
    cloud_service_group = 'Instance'
    cloud_service_type = 'Server'
    cloud_service_types = CLOUD_SERVICE_TYPES

    _ncloud_cls = ncloud_server
    _ncloud_api_v2 = V2Api
    _ncloud_configuration = ncloud_server.Configuration()

    def get_resources(self):

        resources = []
        csr = []

        for instance in self.list_instances():
            csr.append(CloudServiceResponse(
                    {'resource': CloudServiceResource(
                        {'data': instance, "cloud_service_group": self.cloud_service_group,
                         "cloud_service_type": self.cloud_service_type}
                        )
                    }
                )
            )

        resources.extend(self.set_cloud_service_types())
        resources.extend(csr)

        return resources

    def list_instances(self):

        instance_list = []

        try:

            response = self.api_client_v2.get_server_instance_list(ncloud_server.GetServerInstanceListRequest())

            if response:
                response = response.to_dict()

            if response.get("server_instance_list"):

                for server_instance in response.get("server_instance_list"):
                    instance_list.append(
                        Server(
                            {
                                "server_name": server_instance.get("server_name"),
                                "server_instance_type": server_instance.get("server_instance_type"),
                                "server_instance_status_name": server_instance.get("server_instance_status_name"),
                                "private_ip": server_instance.get("private_ip"),
                                "memory_size": server_instance.get("memory_size"),
                                "cpu_count": server_instance.get("cpu_count"),
                                "server_image_name": server_instance.get("server_image_name"),
                                "region": server_instance.get("region")
                            }
                        )
                    )

            return instance_list

        except ApiException as e:
            logging.error(e)
            raise
