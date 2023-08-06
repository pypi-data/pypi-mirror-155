from os import system

from ..dhcp_watchmen import DHCPWatchmen
from .base_control import BaseControl, ControlConfigurationReq


class Script(BaseControl):
    def apply_actions(self, watchmen: DHCPWatchmen, **kwargs):
        """
        Call the script defined in [prefix]_script_path with
        servers and whitelist as parameters
        separated by -:  server1 server2 server3 whitelist0
        """
        servers = watchmen.dhcp_servers
        whitelist = watchmen.whitelist
        whitelisted = ""
        if len(whitelist) > 0:
            whitelisted = whitelist[0]

        script_path = self._conf.get_req("script_path")

        servers = [f"{server.ip},{server.hw}" for server in servers.values()]
        system(script_path + " " + " ".join(servers) + "-" + whitelisted)

    def get_conf_req(self) -> ControlConfigurationReq:
        return ControlConfigurationReq(["script_path"])
