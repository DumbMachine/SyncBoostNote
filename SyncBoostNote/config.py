import yaml
import sys
import os
import readline
import json

home = os.path.expanduser("~")


class git_commands:
    add = "git add -A"
    commit = "git commit -m {}"
    status = "git status"
    push = "git push origin master"


Config = {
    "BOOSTNOTE_PATH": "~/BoostNotes",
    "SHIELDS": True,
    "SHIELDS_TYPE": "for-the-badge",
    "FREQUENCY": "hourly",
    "TIME": 1200
}


def interactive():
    conf = {}
    questions = [
        ['BOOSTNOTE_PATH: ', ' ~/BoostNotes', 'BOOSTNOTE_PATH'],
        ['SHIELDS: ', ' True', 'SHIELDS'],
        ['SHIELDS_TYPE: ', 'for-the-badge', 'SHIELDS_TYPE'],
        # ["hourly", "daily", "weekly", "monthly"]
        ['FREQUENCY: ', 'hourly', 'FREQUENCY'],
        ['TIME: ', '1200', 'TIME'],  # 24 gour format for now

    ]
    for question in questions:
        conf[question[2]] = input_with_prefill(question[0], question[1])
    print(json.dumps(
        conf, indent=2
    ))
    return conf


def config_reader(location):
    config = yaml.load(open(location), Loader=yaml.Loader)
    print(json.dumps(config, indent=2))
    return config


def input_with_prefill(prompt, text):
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result


def create_config(location='.'):
    '''
    Creates a default config for users to see.
    '''
    yaml.dump(
        Config,
        open(os.path.join(location, 'bns.yaml'), 'w+')
    )


create_config()
