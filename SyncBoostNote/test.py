# ! TODO: Add Highligthing shit

import os
import json
from glob import glob
import cson

home = os.path.expanduser("~")
BOOSTNOTE_PATH = os.path.join(home, 'Boostnote')
BOOSTNOTE_NOTES_PATH = os.path.join(home, 'Boostnote/notes')


def boostnote_exists():
    if os.path.isdir(BOOSTNOTE_PATH):
        return 1
    else:
        # ! YAML Config
        return 0
        # raise NotADirectoryError("BoostNode Base Directory doesn't exist. Either make sure BoostNote is installed or add PATH to it in syncboostnote.yaml")\


def boostnote_notes_exist():
    if os.path.isdir(BOOSTNOTE_NOTES_PATH):
        return 1
    else:
        # ! YAML Config
        raise NotADirectoryError(
            f"No NOTES were found in the {BOOSTNOTE_NOTES_PATH} directory")


def get_notes():
    if boostnote_notes_exist():
        notes = glob(os.path.join(BOOSTNOTE_NOTES_PATH, '*.cson'))
        if notes:
            return notes
        else:
            raise EnvironmentError("Emptry Notes Folder, nothing to work on.")
    else:
        raise NotADirectoryError("BoostNode Base Directory doesn't exist. Either make sure BoostNote is installed or add PATH to it in syncboostnote.yaml")\



def cson_reader(location):
    if os.path.isfile(location):
        data = cson.load(open(location, 'r'))
        return data
    else:
        raise FileNotFoundError(f'The cson file at {location} was not found')


def markdown_writer(name, content):
    open(os.path.join(BOOSTNOTE_NOTES_PATH, f'{name}.md'), 'w+').write(content)


def customShield(label='label', message='message', color='orange', mode='markdown', name='Custom Shield'):
    '''
    isStarred: false
    isTrashed: true
    createdAt: "2019-06-20T11:15:56.974Z"
updatedAt: "2019-06-20T19:44:18.224Z"
type: "MARKDOWN_NOTE"
folder: "4bfaf976594ec1b5be18"
title: "   "
tags: []
    '''
    if mode not in ['markdown', 'md', 'restructuredtext', 'rst']:
        raise NotImplementedError(f'{mode} is not implemented yet.')
    else:
        if mode in ['markdown', 'md']:
            return f"![Custom Shield](https://img.shields.io/badge/{label}-{message}-{color}.svg)"
        else:
            return f".. image:: https://img.shields.io/badge/{label}-{message}-{color}.svg   :alt: Custom Shield"


    # boostnote_exists()
    # boostnote_notes_exist()
    # cson_reader()
    # cson_reader()
cson_reader(get_notes()[4])
markdown_writer(
    cson_reader(get_notes()[4])
)
