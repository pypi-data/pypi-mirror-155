from abc import ABC, abstractmethod
from typing import List, Optional


class ControlConfiguration:
    def __init__(self, config_section: dict, prefix: str):
        self.__config_section = config_section
        self.__prefix = prefix

    def get_req(self, requirement: str) -> Optional[str]:
        return self.__config_section.get(self.__prefix + "_" + requirement)


class ControlConfigurationReq:
    def __init__(self, requirements: List[str]):
        self.__requirements = requirements

    def check_requirements(self, conf: ControlConfiguration) -> bool:
        """Check that all the required configuration parameters for the
        are satisfied.
        """
        for requirement in self.__requirements:
            if not conf.get_req(requirement):
                return False

        return True

    def check_dependencies(self, conf: ControlConfiguration) -> bool:
        """Check system dependencies or any other special check made by the module"""
        return True


class BaseControl(ABC):
    def __init__(self):
        self._conf = None

    def set_conf(self, config: ControlConfiguration) -> None:
        self._conf = config

    @abstractmethod
    def get_conf_req(self) -> ControlConfigurationReq:
        pass

    @abstractmethod
    def apply_actions(self, **kwargs):
        """Execute control programmed actions.
        This method is implemented by each custom control. See 'script.py'
        Example: send a message to rabbitmq, exec a script,...
        """
        pass
