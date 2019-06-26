from __future__ import print_function

import json
import os
import platform
import sys
import time
from glob import glob

import cson
import subprocess
from .test import git_update

home = os.path.expanduser("~")


def initialize(config):
    '''
    Initialize will do the following:
    - Check for the directories
    - Make directory for storing notes.
    - Create History
    # ! - Initialize the git repo.
    -----------------s-------------------
    called:
        - Is called upon using  --initialize flag of the CLI
    '''
    # print(config['BOOSTNOTE_PATH'])
    BOOSTNOTE_PATH = config['BOOSTNOTE_PATH']
    if config['BOOSTNOTE_PATH'] == 'default':
        BOOSTNOTE_PATH = os.path.join(home, 'Boostnote')
    if boostnote_exists(location=BOOSTNOTE_PATH):
        BOOSTNOTE_NOTES = os.path.join(BOOSTNOTE_PATH, 'notes')
        create_syncnotes_dir(
            location=os.path.join(BOOSTNOTE_NOTES, 'syncboostnote')
        )
        create_history(BOOSTNOTE_PATH)
        ultimate(config)
    else:
        raise NotADirectoryError(
            f"Boostnote not found at the given location. {BOOSTNOTE_PATH}")


def boostnote_exists(location=os.path.join(home, 'Boostnote')):
    if os.path.isdir(location):
        return 1
    else:
        # ! YAML Config
        return 0
        # raise NotADirectoryError("BoostNode Base Directory doesn't exist. Either make sure BoostNote is installed or add PATH to it in syncboostnote.yaml")\


def create_syncnotes_dir(
    location=os.path.join(home, 'Boostnote/notes/syncboostnote')
):
    """
    Create Directory for syncboostnotes1
    """
    current_platform = platform.system().lower()
    if current_platform != 'windows':
        import pwd

    # create the necessary directory structure for storing config details
    # in the syncboostnote directory
    required_dirs = [location]
    for dir in required_dirs:
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
                if (current_platform != 'windows') and os.getenv("SUDO_USER"):
                    # owner of .syncboostnote should be user even when installing
                    # w/sudo
                    pw = pwd.getpwnam(os.getenv("SUDO_USER"))
                    os.chown(dir, pw.pw_uid, pw.pw_gid)
            except OSError:
                print("syncboostnotes lacks permission to "
                      f"access the '{location}/notes/syncboostnotes' directory.")
                raise

        else:
            pass


def create_history(
    location=os.path.join(home, 'Boostnote')
):
    files = {}
    for note in get_notes():
        files[note.split('/')[-1]] = {
            'title': cson.load(open(note, 'r'))['title'],
            'updated': False
        }
    try:
        json.dump(
            files,
            open(os.path.join(location, 'history.json'), 'w+')
        )
    except Exception as e:
        print(
            f"EXiting, got the following error {e}.\nReport the error on Github")


def get_notes(
    location=os.path.join(home, 'Boostnote', 'notes')

):
    notes = glob(os.path.join(location, '*.cson'))
    if notes:
        return notes
    else:
        raise EnvironmentError("Emptry Notes Folder, nothing to work on.")


def ultimate(config):
    '''
    Performs the followings:
    - Creates history.json, if it doesn't exist
    - If it does:
        - reads it.
        - updates the .md files, which require it.
    -----------------------------------------------
    '''
    # print("Searching for BOOSTNOTE_PATH", end='\r')
    # sys.stdout.flush()
    if not os.path.isfile(os.path.join(config['BOOSTNOTE_PATH'], 'history.json')):

        # Create the History json again.
        create_history(config['BOOSTNOTE_PATH'])
    if boostnote_exists(config['BOOSTNOTE_PATH']):

        # Creating History again, as this will track if new files have been added.
        # sys.stdout.flush()
        # print("Creating History.json file", end='\r')

        create_history(config['BOOSTNOTE_PATH'])

        # sys.stdout.flush()
        # print("Creation done!", end='\r')

        history_json = json.load(open(os.path.join(
            config['BOOSTNOTE_PATH'], 'history.json'), 'r'))
        for file in history_json.keys():
            if not history_json[file]['updated']:

                # If not updated, re render the file
                markdown_writer(
                    cson_reader(
                        os.path.join(
                            config['BOOSTNOTE_PATH'], 'notes', file)
                    ),
                    location=os.path.join(
                        config['BOOSTNOTE_PATH'], 'notes', 'syncboostnote'
                    ),
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
            open(os.path.join(config['BOOSTNOTE_PATH'], 'history.json'), 'w+')
        )

    else:
        print("FUCKKK")


def cson_reader(location):
    if os.path.isfile(location):
        data = cson.load(open(location, 'r'))
        return data
    else:
        return 0
        # raise FileNotFoundError(f'The cson file at {location} was not found')


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
    if things:
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


def get_changes(
    location=os.path.join(home, 'Boostnote')
):
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
    os.chdir(location)
    p = subprocess.Popen(
        "git status", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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


def update_changes(
    location=os.path.join(home, 'Boostnote')
):
    # create_history(location)
    changed_files = get_changes()
    history_json = json.load(open(os.path.join(
        location, 'history.json'), 'r'))
    for file in changed_files:
        if '.md' in file:
            # These files have been deleted or changed without telling us 😢😢😢
            # Thus we will re render them

            # 1. get the filename
            history_json = json.load(open(os.path.join(
                location, 'history.json'), 'r'))
            for filename in history_json.keys():
                print(file)
                if history_json[filename]['title'] == file.replace('.md', ''):
                    if file == 'SnycBoostNotes.md':
                        continue

                    # 2. Rendering the missing files.
                    markdown_writer(
                        cson_reader(
                            os.path.join(
                                location, 'notes', filename)
                        ),
                        location=os.path.join(
                            location, 'notes', 'syncboostnote'),
                        options={
                            'style': 'for-the-badge',
                            'option': 2
                        }
                    )
        else:
            history_json[file]['updated'] = False
    git_update(message='shit')
    json.dump(
        history_json,
        open(os.path.join(location, 'history.json'), 'w+')
    )


def create_history(
    location=os.path.join(home, 'Boostnote')
):
    if os.path.isfile(
        os.path.join(location, 'history.json')
    ):
        # FIle already exists, check for changes.
        update_changes()
        print(1)

    else:
        print(3)
        files = {}
        for note in get_notes():
            files[note.split('/')[-1]] = {
                'title': cson.load(open(note, 'r'))['title'],
                'updated': False
            }
        json.dump(
            files,
            open(os.path.join(location, 'history.json'), 'w+')
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
            # https://github.com/DumbMachine/SyncBoostNoteExample/blob/master/notes/syncboostnote/Stolen%20Content.md
            f"- [{data['title']}](https://github.com/DumbMachine/{repo_name()}/blob/master/notes/syncboostnote/{data['title'].replace(' ','%20')}.md)")
        file.write("\n")
    # return data

    awesome = 'https://img.shields.io/badge/made--with--%E2%99%A5--by-ProjectPy-blueviolet.svg'

    file.write(
        f"\n---\n<sub>This README was generated with ❤ by [SyncBoostnote](https://github.com/DumbMachine/SyncBoostNote) </sub>")


def repo_name(
    location=os.path.join(home, 'Boostnote', '.git', 'config')
):
    '''
    Reads .git/config for information on the Github repo name
    '''
    for line in open(location, 'r').readlines():
        if ".git" in line.strip().split('/')[-1]:
            return(line.strip().split('/')[-1].strip(".git"))
