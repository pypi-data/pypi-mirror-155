from whizbang.config.app_config import AppConfig
from whizbang.domain.handler.handler_base import HandlerBase
from whizbang.domain.manager.az.az_resource_group_manager import AzResourceGroupManager
from whizbang.domain.models.az_resource_base import AzResourceGroup


class ResourceGroupHandler(HandlerBase):
    def __init__(self, app_config: AppConfig, resource_group_manager: AzResourceGroupManager):
        HandlerBase.__init__(self, app_config=app_config)
        self._resource_group_manager = resource_group_manager

    def create_resource_group(self, name: str, location: str):
        resource_group = AzResourceGroup(
            resource_group_name=name,
            location=location
        )

        return self._resource_group_manager.create(resource_group)
    