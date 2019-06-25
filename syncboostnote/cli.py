import argparse
import json
import os
import shutil
import site
import sys
import textwrap
import time
import warnings

from colorama import Fore, init

from .config import Config, interactive, config_reader
from .test import ultimate

init(autoreset=True)


def options():
    '''
    Parsing the Arguments here
    '''
    ap = argparse.ArgumentParser(
        prog="projectpy",
        usage="%(prog)s [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''SyncBoostNotes
                                       =======================================
                                       - A CLI to Sync your BoostNotes Notes -
                                       =======================================
                                       '''))

    ap.add_argument("-l", "--location", required=True,
                    help="Location of the BoostNotes local storage.")

    ap.add_argument(
        "-c",
        "--config",
        required=False,
        help="Location of the config.yaml/config.yml file",
        default=True)

    ap.add_argument(
        "-col",
        "--color",
        required=False,
        help="Toggle Colors on the print",
        default=True)

    ap.add_argument(
        "-g",
        "--generate",
        required=False,
        help="Generate config.yaml file for ya",
        default=True)

    ap.add_argument(
        "-i",
        "--interactive",
        required=False,
        help="Get an Interactive prompt to fill the forms.",
        default=False)

    return vars(ap.parse_args())


def initialize(args):
    '''
    Sets the Config for the installation
    '''
    if args['interactive']:
        print('>>> Interactive <<<')
        return interactive()

    elif args['config']:
        print('>>> CUSTOM <<<')
        ultimate(config_reader('./config.yaml'))

    else:
        # ! Weird
        raise Exception('Weird')


def main():
    args = options()
    initialize(args)


def run_as_command():
    main()


run_as_command()
# print(
#     '''
# _________________________________
# |                                |
# | Generation was successful      |
# | Below is the generated config: |
# | -------------------------      |
# | $ cd repo_name                 |
# | $ python setup.py install      |
# ------------------------------
# '''
# )
