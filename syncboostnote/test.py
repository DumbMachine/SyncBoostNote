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
