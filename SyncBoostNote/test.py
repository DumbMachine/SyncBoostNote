# ! TODO: Add Highligthing shit

import json
import os
import subprocess
import time
from collections import deque
from datetime import datetime
from glob import glob

import cson

from config import git_commands

home = os.path.expanduser("~")
BOOSTNOTE_PATH = os.path.join(home, 'Boostnote')
BOOSTNOTE_NOTES_PATH = os.path.join(home, 'Boostnote/notes')
BOOSTNOTE_SYNCNOTES_PATH = os.path.join(
    home, 'Boostnote/notes/syncboostnote')


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


def get_notes():
    if boostnote_notes_exist():
        notes = glob(os.path.join(BOOSTNOTE_NOTES_PATH, '*.cson'))
        if notes:
            return notes
        else:
            raise EnvironmentError("Emptry Notes Folder, nothing to work on.")
    else:
        raise NotADirectoryError(
            "BoostNode Base Directory doesn't exist. Either make sure BoostNote is installed or add PATH to it in syncboostnote.yaml")


def cson_reader(location):
    if os.path.isfile(location):
        data = cson.load(open(location, 'r'))
        return data
    else:
        raise FileNotFoundError(f'The cson file at {location} was not found')


def customshield(
        label='label',
        message='message',
        style='plastic',
        color='orange',
        mode='markdown',
        name='Custom Shield'):
    '''

    '''
    if mode not in ['markdown', 'md', 'restructuredtext', 'rst']:
        raise NotImplementedError(f'{mode} is not implemented yet.')
    else:
        if mode in ['markdown', 'md']:
            return f"![{name}](https://img.shields.io/badge/{label}-{message}-{color}.svg?style={style})"
        else:
            return f".. image:: https://img.shields.io/badge/{label}-{message}-{color}.svg?style={style} :alt: {name}"


def markdown_writer(things, location, shields=True,
                    options={
                        'style': 'for-the-badge',
                        'option': 2
                    }):
    '''
    Used to write the markdown files
    --------------------------------
    PARAMETERS:
    things: dict, cson_reader(fp):
        The dict{} which contains shit that was read via the cson

    '''

    embels = ['isStarred', 'isTrashed',
              'updatedAt', 'type', 'folder', 'tags']
    shelds = []
    if shields:
        for key in embels:
            x = None
            if things[key]:
                if key == 'isStarred':
                    shelds.append(customshield(
                        key, '⭐', color='black', style=options['style']))

                if key == 'isTrashed':
                    shelds.append(customshield(
                        key, '🗑', color='black', style=options['style']))

                elif key == 'updatedAt':
                    shelds.append(customshield(
                        key, things[key].split(':')[0][:-3].replace('-', '/'), color='green', style=options['style']))

                elif key in ['type', 'folder']:
                    shelds.append(customshield(
                        key, things[key], color='blue', style=options['style']))

                elif key == 'tags':
                    if options['option']:
                        # OPTION 1: {tag| gay} {tag| notgay}
                        for tag in things[key]:
                            shelds.append(
                                customshield(label='tag', message=tag,
                                             color='purple', style=options['style'])
                            )
                    else:
                        # OPTION 2: {tag| gay, notgay}
                        tags = []
                        for tag in things[key]:
                            tags.append(tag)
                        shelds.append(customshield(
                            label='tags', message='_'.join(tags), color='blueviolet', style=options['style']))

        file = open(os.path.join(location,
                                 f"{things['title']}.md"), 'w+')

        for count, shield in enumerate(shelds):
            if count != len(shelds) - 1:
                file.write(shield)
                file.write(' ')
            else:
                file.write(shield)
                file.write('\n')

        try:
            file.write(things['content'])

        except:
            pass
        try:
            file.write(things['snippets'])

        except:
            pass


# for note in get_notes():
#     markdown_writer(
#         cson_reader(note),
#         options={
#             'style': 'for-the-badge',
#             'option': 2
#         }
#     )
# boostnote_exists()
# boostnote_notes_exist()
# cson_reader()
# cson_reader()

def get_changes():
    '''
    uses git status to find the files which have changes.
    ------------------------------------------------------

    Returns:
        list:
            A List containing all the files names which have changed.
    >>> get_changes()
    >>> ['test.py', 'cli.py', 'config.py', 'utils.py']
    '''
    files = []
    os.chdir(BOOSTNOTE_NOTES_PATH)
    p = subprocess.Popen(
        git_commands.status, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        # Putting checks to see if any rendered file is deleted.
        if '.md' in line.decode("utf-8"):
            files.append(
                line.decode(
                    "utf-8").replace('modified:', '').strip().split('/')[-1]
            )
        # Checking if the diff file is .cson
        if '.cson' in line.decode("utf-8"):
            files.append(line.decode(
                "utf-8").replace('modified:', '').strip().split('/')[-1]
            )
    retval = p.wait()
    return files


def update_changes():
    changed_files = get_changes()
    history_json = json.load(open(os.path.join(
        BOOSTNOTE_PATH, 'history.json'), 'r'))
    for file in changed_files:
        if '.md' in file:
            # These files have been deleted or changed without telling us 😢😢😢
            # Thus we will re render them
            # 1. get the filename
            history_json = json.load(open(os.path.join(
                BOOSTNOTE_PATH, 'history.json'), 'r'))
            for filename in history_json.keys():
                if history_json[filename]['title'] == file.replace('.md', ''):
                    # 2. Rendering the missing files.
                    markdown_writer(
                        cson_reader(
                            os.path.join(
                                BOOSTNOTE_PATH, 'notes', filename)
                        ),
                        location=BOOSTNOTE_SYNCNOTES_PATH,
                        options={
                            'style': 'for-the-badge',
                            'option': 2
                        }
                    )
            pass
        else:
            history_json[file]['updated'] = False
    json.dump(
        history_json,
        open(os.path.join(BOOSTNOTE_PATH, 'history.json'), 'w+')
    )


def create_history():
    files = {}
    for note in get_notes():
        files[note.split('/')[-1]] = {
            'title': cson.load(open(note, 'r'))['title'],
            'updated': False
        }
    json.dump(
        files,
        open(os.path.join(BOOSTNOTE_PATH, 'history.json'), 'w+')
    )


def create_readme(config):

    notes = get_notes()
    # data = {}
    file = open(os.path.join(config['BOOSTNOTE_PATH'], 'README.md'), 'w+')
    file.write(
        '''# SnycBoostNotes
# This repo consists of two directories:
```bash
$ tree
.
├── boostnote.json
├── history.json
└── notes
    ├── ....cson
    ├── ....cson
    └── syncboostnote
        ├── ....md
        ├── ....md
```
- Directory `base`:
  - boostnote.json ``Created by boostnote``
  - history.json ``Created by SyncBoostnote``
  - Directory `notes`:
    - Raw `.cson` files used by BoostNote.
    - Directory `syncboostnote`:
      - `.md` files used display content on Github.

# Index:
# This following are the documents:

        '''
    )
    for note in get_notes():
        data = cson_reader(note)
        # data[note.split("/")[-1]] = {
        #     'title': cson_reader(note)['title'],
        #     'createdAt': cson_reader(note)['createdAt'],
        #     'tags': cson_reader(note)['tags'],
        # }
        # ! Generate Github link here
        file.write(
            f"- [{data['title']}](https://github.com/DumbMachine/temp/blob/master/notes/syncboostnote/{data['title'].replace(' ','%20')}.md)")
        file.write("\n")
    # return data

    awesome = 'https://img.shields.io/badge/made--with--%E2%99%A5--by-ProjectPy-blueviolet.svg'

    file.write(
        f"\n---\n<sub>This README was generated with ❤ by [SyncBoostnote](https://github.com/DumbMachine/SyncBoostNote) </sub>")


def ultimate(config):
    '''
    Performs the followings:
    - Creates history.json, if it doesn't exist
    - If it does:
        - reads it.
        - updates the .md files, which require it.
    -----------------------------------------------
    '''
    if not os.path.isfile(os.path.join(config['BOOSTNOTE_PATH'], 'history.json')):
        # Create the History json again.
        create_history()
    if boostnote_exists(config['BOOSTNOTE_PATH']):
        print()
        print('[PASSED] BOOSTNOTE_EXISTS ')
        if boostnote_notes_exist(os.path.join(config['BOOSTNOTE_PATH'], 'notes')):
            print('[PASSED] BOOSTNOTE_NOTES_EXISTS ')
            history_json = json.load(open(os.path.join(
                BOOSTNOTE_PATH, 'history.json'), 'r'))
            for file in history_json.keys():
                print(file, history_json[file]['updated'])
                if not history_json[file]['updated']:
                    # If not updated, re render the file
                    markdown_writer(
                        cson_reader(
                            os.path.join(
                                config['BOOSTNOTE_PATH'], 'notes', file)
                        ),
                        location=BOOSTNOTE_SYNCNOTES_PATH,
                        options={
                            'style': config['SHIELDS_TYPE'],
                            'option': 2
                        }
                    )
                    # Update the file render
                    history_json[file]['updated'] = True

        create_readme(config)
        # Writing the changes of render.
        json.dump(
            history_json,
            open(os.path.join(BOOSTNOTE_PATH, 'history.json'), 'w+')
        )
        print('[PASSED] README_GEN ')

    else:
        print("FUCKKK")


ultimate({
    "BOOSTNOTE_PATH": os.path.join(home, 'Boostnote'),
    "SHIELDS": True,
    "SHIELDS_TYPE": "for-the-badge",
    "FREQUENCY": "hourly",
    "TIME": 1200
})


# def timely_check(config):
#     time_check = config['TIME']
#     frequency = config['FREQUENCY']

#     if frequency == 'onchange':
#         raise NotImplementedError('This THING is not implemented currently')
#     else:
#         if datetime.now().hour == time_check:
#             print("ITS HIGH NOON")
#         else:
#             time.sleep(2)
#             print("Has the time come yet?")


# # timely_check(
# #     {
# #         "BOOSTNOTE_PATH": os.path.join(home, 'Boostnote'),
# #         "SHIELDS": True,
# #         "SHIELDS_TYPE": "for-the-badge",
# #         "FREQUENCY": "hourly",
# #         "TIME": 11
# #     }
# # )


# def watch_file(filename, time_limit=3600, check_interval=60):
#     '''
#     use get changes to see changes
#     '''
#     now = time.time()
#     last_time = now + time_limit

#     while time.time() <= last_time:
#         if os.path.exists(filename):
#             print('yes')
#         else:
#             # Wait for check interval seconds, then check again.
#             time.sleep(check_interval)

#     print('no')


# def create_readme():
#     raise NotImplementedError
