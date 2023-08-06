#!/usr/bin/env python3
from threading import Thread
import importlib

import logging.handlers
import sys

from .config import config
from .dhcp_watchmen import DHCPWatchmen


LOG_LEVEL = logging.DEBUG


logger = logging.getLogger("elchicodepython.honeycheck")
logger.setLevel(LOG_LEVEL)

ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - HoneyCheck %(message)s"
)
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_control_objects(iface, name):
    """
    :param iface:
    :param name:
    :return: list of objects inherited from honeycheckModule
    :rtype list
    """

    control_objects_str = [co.strip() for co in config[iface][name].split(",")]
    control_objects = []

    for control_object in control_objects_str:
        # Import the control module defined in the configuration
        control_object_module_str = ".".join(control_object.split('.')[:-1])
        control_object_class_str = control_object.split('.')[-1]
        try:
            control_object_module = importlib.import_module(
                control_object_module_str
            )
        except ModuleNotFoundError:
            logger.error(f"Module {control_object_module_str} not found")
            continue

        ControlClass = getattr(
            control_object_module,
            control_object_class_str
        )

        control_object = ControlClass(iface, name)  # Instance of the Control Object

        if control_object.check_dependencies():
            if control_object.check_requirements():
                control_objects.append(control_object)
            else:
                logger.critical(
                    "Requirements "
                    + str(control_object.config_requirements)
                    + " check failed in "
                    + control_object.__class__.__name__
                )
                return []
        else:
            logger.critical(
                "Dependencies check failed in module "
                + control_object.__class__.__name__
            )
            return []

    return control_objects




def start_the_party(config, config_file):

    # If HoneyCHECK is not configured exit
    if len(config.sections()) == 0:
        logger.error(
            "You should provide a valid configuration to honeycheck before using it\n"
            "Read the docs at https://github.com/elchicodepython/HoneyCheck"
        )

        sys.exit(1)


    ifaces = config.sections()

    if len(ifaces) == 0:
        logger.critical(
            "Fail to check the configuration file in " + config_file
        )
        sys.exit(2)

    for iface in ifaces:
        logger.info(iface + ": FOUND IN " + config_file)
        try:
            timeout = int(config[iface]["discover_timeout"])
            logger.info("Stablished timeout = %s seconds" % timeout)
        except KeyError:
            timeout = 10
            logger.info(
                "Stablished timeout = 10 for sending DHCP DISCOVER packets as DEFAULT"
            )

        whitelist = (
            []
            if "whitelist" not in config[iface]
            else [ip.strip() for ip in config[iface]["whitelist"].split(",")]
        )

        fail_objects = (
            []
            if "fail_test" not in config[iface]
            else get_control_objects(iface, "fail_test")
        )
        pass_objects = (
            []
            if "pass_test" not in config[iface]
            else get_control_objects(iface, "pass_test")
        )
        final_objects = (
            []
            if "final_exec" not in config[iface]
            else get_control_objects(iface, "final_exec")
        )

        watchmen = DHCPWatchmen(
            iface, fail_objects, pass_objects, final_objects, whitelist
        )
        Thread(target=watchmen.sniff_dhcp).start()
        Thread(target=watchmen.dhcp_discovery_daemon, args=(timeout,)).start()
