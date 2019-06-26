# # ! TODO: Add Highligthing shit

import json
import os
import platform
import subprocess
import time
from collections import deque
from datetime import datetime
from glob import glob

# import cson
home = os.path.expanduser("~")


def sync(
    location=os.path.join(home, 'Boostnote')
):
    os.chdir(location)
    p = subprocess.Popen(
        "git status", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # print(p.stdout.readlines()[1].strip())
    if p.stdout.readlines()[1].decode("utf=8").strip() == 'nothing to commit, working tree clean':
        os.system("git push origin master")
    else:
        print("Adding all the things")
        p = subprocess.Popen(
            "git add -A", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # print("Commiting all the things")
        p1 = subprocess.Popen(
            f"git commit -m '{datetime.now()}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p1.stdout.readlines()[2:]:
            print(line.decode("utf-8"))

        # print("Pushing all the things")
        p2 = subprocess.Popen(
            "git push origin master", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    retval = p.wait()


def boostnote_exists(location=os.path.join(home, 'Boostnote')):
    if os.path.isdir(BOOSTNOTE_PATH):
        return 1
    else:
        # ! YAML Config
        return 0
        # raise NotADirectoryError("BoostNode Base Directory doesn't exist. Either make sure BoostNote is installed or add PATH to it in syncboostnote.yaml")\


def boostnote_notes_exist(location=os.path.join(home, 'notes')):
    if os.path.isdir(BOOSTNOTE_NOTES_PATH):
        return 1
    else:
        # ! YAML Config
        raise NotADirectoryError(
            f"No NOTES were found in the {BOOSTNOTE_NOTES_PATH} directory")


def git_update(message='nothing'):
    os.system('git add -A')
    os.system(f"git commit -m '{message}'")


def timely_check(config):
    time_check = config['TIME']
    frequency = config['FREQUENCY']

    if frequency == 'onchange':
        raise NotImplementedError('This THING is not implemented currently')
    else:
        if datetime.now().hour == time_check:
            print("ITS HIGH NOON")
        else:
            if datetime.now().hour > time_check:
                time.sleep(
                    (datetime.now().hour - time_check) * 360
                )
            elif datetime.now().hour < time_check:
                time.sleep(
                    (datetime.now().hour - time_check + 24) * 360
                )
            # time.sleep(2)
            print("Has the time come yet?")


def time_check(frequency, thyme, config):
    '''
    Waits for the time and performs:
    1. If user mentions time, then sleep time will be time + frequency
    2. If user mention time, then sleep time will be 1200 hrs + frequency
    '''
    thyme = 12
    while(1):

        if frequency == 'onchange':
            while(1):
                if not get_changes():
                    # Wait
                    print(f'Waiting for {"2 seconds"}')
                    time.sleep(2)
                    # time, slep(10 * 60 * 60)
                else:
                    # change occured
                    print("Calling update_changes")
                    update_changes()
                    print("Calling ultimate")
                    ultimate(config)

        if datetime.now().hour == thyme:
            # check updates
            print(gay)
            pass
        else:
            print('shit', datetime.now())
            if frequency == 'hourly':
                time.sleep(1 * 360 / 100)
            elif frequency == 'daily':
                time.sleep(24 * 360 / 100)
            elif frequency == 'weekly':
                time.sleep(24 * 7 * 360 / 100)


# time_check('onchange', '14',
#            {
#                "BOOSTNOTE_PATH": os.path.join(home, 'Boostnote'),
#                "SHIELDS": True,
#                "SHIELDS_TYPE": "for-the-badge",
#                "FREQUENCY": "hourly",
#                "TIME": 11
#            }
#            )
