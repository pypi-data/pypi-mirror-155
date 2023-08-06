import argparse
from .app_preparation import start_the_party
from .config import config as conf


def parse_args():
    parser = argparse.ArgumentParser(description="\033[0;36mHoneyCheck detects rogue DHCP servers in your network. | "
                                                "Made with \033[0;31m<3\033[0;36m by @elchicodepython\033[0m")

    parser.prog = "python3 -m honeycheck"

    parser.add_argument("-c", help="Configuration file", required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    config_file = args.c
    conf.read(config_file)
    start_the_party(
        conf, config_file
    )
