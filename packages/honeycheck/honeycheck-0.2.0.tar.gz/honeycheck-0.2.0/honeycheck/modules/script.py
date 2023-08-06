from os import system
from .base_control import ControlModule


class Script(ControlModule):

    config_requirements = ["script_path"]

    def __init__(self, iface, prefix):
        super().__init__(iface, prefix, self.config_requirements)

    def apply_actions(self, watchmen, **kwargs):
        """
        Call the script defined in [prefix]_script_path with servers and whitelist as parametters
        separated by -:  server1 server2 server3 whitelist0
        :param kwargs:
        :return:
        """
        servers = watchmen.dhcp_servers
        whitelist = watchmen.whitelist
        whitelisted = ""
        if len(whitelist) > 0:
            whitelisted = whitelist[0]

        script_path = self.get_req("script_path")

        servers = [server.ip + "," + server.hw for server in servers.values()]
        system(script_path + " " + " ".join(servers) + "-" + whitelisted)
