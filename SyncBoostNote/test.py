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


def markdown_writer(things, shields=True):
    embels = ['isStarred', 'isTrashed',
              'updatedAt', 'type', 'folder', 'tags']
    shelds = []
    if shields:
        for key in embels:
            x = None
            # print(things[key])
            # if key in ['isStarred', 'isTrashed']:
            if things[key]:
                if key == 'isStarred':
                    shelds.append(customshield(key, '⭐', color='black'))

                if key == 'isTrashed':
                    shelds.append(customshield(key, '🗑', color='black'))

                elif key == 'updatedAt':
                    shelds.append(customshield(
                        key, things[key].split(':')[0][:-3].replace('-', '/'), color='green'))

                elif key in ['type', 'folder']:
                    shelds.append(customshield(key, things[key], color='blue'))

                elif key == 'tags':
                    # OPTION 1: {tag| gay} {tag| notgay}
                    # for tag in things[key]:
                    #     shelds.append(
                    #         customshield(label='tag', message=tag,
                    #                      color='purple')
                    #     )

                    # OPTION 2: {tag| gay, notgay}
                    tags = []
                    for tag in things[key]:
                        tags.append(tag)
                    shelds.append(customshield(
                        label='tags', message='_'.join(tags), color='blueviolet', style='for-the-badge'))

        file = open(os.path.join(BOOSTNOTE_NOTES_PATH,
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

# markdown_writer(
#     cson_reader(get_notes()[4])
# )


for note in get_notes():
    markdown_writer(
        cson_reader(
            note
        )
    )
# boostnote_exists()
# boostnote_notes_exist()
# cson_reader()
# cson_reader()
