from push_to_prod import copy_db_dev_prod
import utils as utils
import argparse
import sys


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

    print(config1['db_uri'])
    print(config2['db_uri'])
    copy_db_dev_prod(config1['db_uri'], config2['db_uri'])


if __name__ == "__main__":
    main(sys.argv[1:])
