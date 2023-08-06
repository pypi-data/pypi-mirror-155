from abc import abstractmethod

from whizbang.config.app_config import AppConfig
from whizbang.domain.handler.handler_base import IHandler, HandlerBase
from whizbang.domain.manager.az.az_storage_manager import IAzStorageManager
from whizbang.domain.models.firewall_rule_cidr import FirewallRuleCIDR
from whizbang.domain.models.storage.azure_blob import AzureBlob
from whizbang.domain.models.storage.datalake_state import DatalakeState
from whizbang.domain.models.storage.storage_resource import StorageContainer, StorageBlobSource
from whizbang.domain.workflow.datalake.datalake_deploy_workflow import DatalakeDeployWorkflow
from whizbang.util import path_defaults
from whizbang.util.json_helpers import import_local_json


class IStorageHandler(IHandler):
    """"""

    @abstractmethod
    def deploy_datalake_directories(self, solution_name, storage_account_name):
        """"""

    @abstractmethod
    def get_storage_account_key(self, storage_account_name: str) -> str:
        """"""

    @abstractmethod
    def add_network_rules(self, storage_account_name: str, ip_address_range: str, firewall_rule_name: str = None):
        """"""

    @abstractmethod
    def remove_network_rules(self, storage_account_name: str, ip_address_range: str, firewall_rule_name: str = None):
        """"""

    @abstractmethod
    def update_account_networking(self, storage_account_name: str, allow: bool):
        """"""


class StorageHandler(HandlerBase, IStorageHandler):
    def __init__(self, app_config: AppConfig, storage_manager: IAzStorageManager,
                 datalake_deploy_workflow: DatalakeDeployWorkflow):
        HandlerBase.__init__(self, app_config=app_config)
        self.__storage_manager = storage_manager
        self.__datalake_deploy_workflow = datalake_deploy_workflow

    def deploy_datalake_directories(self, solution_name, storage_account_name, recursive: bool = False,
                                    permissions: str="r", path: str = '"/"'):
        """
        :param solution_name: Name of solution for finding config files
        :param storage_account_name: Name of the storage account to deploy to
        :param recursive: Install acls recursively. Needed for the creation of multiple layers of files. This can be much slower
        :param permissions: What permissions the service principal should get
        :param path: The path to start applying the deployment
        :return: None
        """
        datalake_state_path = path_defaults.get_datalake_state_path(app_config=self._app_config,
                                                                    solution_name=solution_name)
        datalake_json = import_local_json(f'{datalake_state_path}/datalake.json')

        for container in datalake_json['containers']:
            storage_container = StorageContainer(container_name=container['container-name'],
                                                 storage_account_name=storage_account_name)
            datalake_state = DatalakeState(storage_container=storage_container,
                                           datalake_json=container,
                                           recursive=recursive,
                                           permissions=permissions,
                                           path=path)
            self.__datalake_deploy_workflow.run(request=datalake_state)

    def get_storage_account_key(self, storage_account_name: str) -> str:
        return self.__storage_manager.get_storage_account_key(storage_account_name)

    def add_network_rules(self, storage_account_name: str, whitelist_addresses: list[str],
                          firewall_rule_name: str = None):
        name = firewall_rule_name or ""
        for ip_address in whitelist_addresses:
            self.__storage_manager.add_network_rule(storage_account_name=storage_account_name,
                                                    firewall_rule_cidr=FirewallRuleCIDR(
                                                        name=name,
                                                        cidr_ip_range=ip_address
                                                    ))

    def remove_network_rules(self, storage_account_name: str, whitelist_addresses: list[str],
                             firewall_rule_name: str = None):
        name = firewall_rule_name or ""
        for ip_address in whitelist_addresses:
            self.__storage_manager.remove_network_rule(storage_account_name=storage_account_name,
                                                       firewall_rule_cidr=FirewallRuleCIDR(
                                                           name=name,
                                                           cidr_ip_range=ip_address
                                                       ))

    def update_account_networking(self, storage_account_name: str, allow: bool):
        return self.__storage_manager.update_account_networking(storage_account_name=storage_account_name,
                                                                allow=allow)

    def download_blob_to_local_path(self, destination_path: str, blob_name: str,
                                    container_name: str, account_name: str):
        storage_blob = StorageBlobSource(name=blob_name, local_path=destination_path,
                                         container_name=container_name, storage_account_name=account_name)
        return self.__storage_manager.download_blob(storage_blob=storage_blob)
