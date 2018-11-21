# -*- coding: utf-8 -*-

import argparse
import sys

import utils as utils
from push_to_prod import copy_db_dev_prod


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c1', '--config1',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    parser.add_argument('-c2', '--config2',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")

    args = parser.parse_args()
    config1 = utils.read_config(args.config1)
    config2 = utils.read_config(args.config2)

    print(config1)
    print(config1['general']['db_uri'])
    print(config2['general']['db_uri'])
    copy_db_dev_prod(config1['general']['db_uri'], config2['general']['db_uri'])


if __name__ == "__main__":
    main(sys.argv[1:])
