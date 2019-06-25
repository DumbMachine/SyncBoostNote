import argparse
import json
import os
import shutil
import site
import sys
import textwrap
import time
# import warnings

import yaml
from colorama import Fore, init

from .config import Config, config_reader, interactive
from .utils import initialize
from .test import sync

home = os.path.expanduser("~")

init(autoreset=True)


def options():
    '''
    Parsing the Arguments here
    '''
    ap = argparse.ArgumentParser(
        prog="syncboostnote",
        usage="%(prog)s [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''SyncBoostNotes
=======================================
- A CLI to Sync your BoostNotes Notes -
=======================================
                                       '''))

    ap.add_argument(
        "-l",
        "--location",
        required=False,
        help="Location of the BoostNotes local storage.",
        default=os.path.join(home, 'Boostnote'))

    ap.add_argument(
        "-ini",
        "--init",
        required=False,
        help="Initialise the CLI",
        default=False)

    ap.add_argument(
        "--sync",
        # dest=False,
        action='store_true'
    )

    ap.add_argument(
        "-cus",
        "--custom",
        required=False,
        help="Location of the config.yaml/config.yml file",
        default=False)

    ap.add_argument(
        "-g",
        "--generate",
        required=False,
        help="Generate config.yaml file for ya",
        default=False)

    ap.add_argument(
        "-i",
        "--interactive",
        required=False,
        help="Get an Interactive prompt to fill the forms.",
        default=False)

    ap.set_defaults(feature=False)
    return vars(ap.parse_args())


def starter(args):
    '''
    Sets the Config for the installation
    '''
    if args['sync']:
        sync()
    elif args['interactive']:
        print('>>> Interactive <<<')
        return interactive()

    elif args['location']:
        # Location is at the default and the user wants default shit.
        initialize({
            "BOOSTNOTE_PATH": args['location'],
            "SHIELDS": True,
            "SHIELDS_TYPE": "for-the-badge",
            "FREQUENCY": "hourly",
            "TIME": 1200
        })

    elif args['config']:
        print(args['generate'])
        conf = yaml.load(
            open(args['generate'], 'r'),
            Loader=yaml.Loader
        )
        initialize(conf)

    else:
        # ! Weird
        raise Exception('Weird')


def run_as_command():
    args = options()
    starter(args)


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
