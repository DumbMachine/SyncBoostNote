# SyncBoostNote
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)  [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://img.shields.io/badge/Made%20For-Boostnote-brightgreen.svg?style=for-the-badge)](https://github.com/BoostIO/Boostnote) [![forthebadge](https://img.shields.io/badge/STATUS-WIP-blueviolet.svg?style=for-the-badge)](https://github.com/BoostIO/Boostnote) 


### A simple cli to save your notes from Boostnotes directly to a Github repo.

## Features:


## Requirements:
### Before using this cli, make sure you have the following:
- git
  - If not installed visit, [Git](https://git-scm.com/downloads)
- python
  - IF note installed visit, [Python](https://www.python.org/downloads/)
- boostnote (also know where it is installed)
  - If not installed visit, [BoostNote](https://boostnote.io/#download)
## Installation:
- To install from PyPi:
```bash
$ pip install syncboostnote
```
- To install from source:
```bash
$ git clone https://github.com/DumbMachine/SyncBoostNote
$ cd syncboostnote
$ python setup.py install
```
## Usage:
### Default Usage:
This method assumes that the location of ``Boostnote`` local storage is the following:
```bash
/home/$USER/Boostnote
```
If this indeed is the location of the installation, then you don't really have to do anything.
1. Create a Repo on github ( or use an existing one ), where you would like notes to be saved.
2. Go to installation directory:
```bash
$ cd ~/Boostnote
```
3. Initialise a git repository and add the remote to your desired repository.
```bash
$ git init
$ git remote add origin <repo_url>
```
4. Let the cli take control now. Since your already have the correct location for ``Boostnote`` folder, all you have to do now is:
```bash
$ syncboostnote  # This will call the cli
```
This will add all your notes to repo and also generate ``.md`` files for them. ( placed in the */Boostnote/note/syncboostnote ). 
5. To publish the added notes to your github repo
```bash
$ syncboostnote --sync
```
This will upload the folder ``Boostnote`` to github with the following tree:
```bash
$ tree Boostnote
Boosnote
├── boostnote.json
├── history.json
├── notes
|    ├── ....cson
|    ├── ....cson
|    └── syncboostnote
|        ├── ....md
|        ├── ....md
├──── README.md

```
- Directory `boostnote`:
  - boostnote.json ``Created by boostnote``
  - history.json ``Created by SyncBoostnote``
  - Directory `notes`:
    - Raw `.cson` files used by BoostNote.
    - Directory `syncboostnote`:
      - `.md` files used display content on Github.
  - ``README.md`` Created by ``SyncBoostnote``. Will help you keep track 
 
 **README.md** will have links to all your notes on the Github repo.

```bash
(base)  dumbmachine@dumbmachine  ~/Boostnote   master ●  git init  
Initialized empty Git repository in /home/dumbmachine/Boostnote/.git/
(base)  dumbmachine@dumbmachine  ~/Boostnote   master  git remote add origin git@github.com:DumbMachine/temp.git
(base)  ✘ dumbmachine@dumbmachine  ~/Boostnote   master  git remote add origin git@github.com:DumbMachine/SyncBoostNoteExample.git
(base)  dumbmachine@dumbmachine  ~/Boostnote   master  syncboostnote
(base)  dumbmachine@dumbmachine  ~/Boostnote   master  syncboostnote --sync
Adding all the things
[master (root-commit) 9b9bf03] .
 12 files changed, 1302 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 boostnote.json
 create mode 100644 history.json
 create mode 100644 notes/40c68663-6c75-4c85-a219-a60b137ad262.cson
 create mode 100644 notes/ad76eb68-c488-4e9e-bb7e-3a912d1df252.cson
 create mode 100644 notes/bbbcc9eb-2cbc-43ba-b6af-fdbcca305e71.cson
 create mode 100644 notes/cc0c17cb-25bb-45f6-bdf0-fc8b54e88bb2.cson
 create mode 100644 notes/syncboostnote/Day: Tuesday  Date: June 18.md
 create mode 100644 notes/syncboostnote/Dillinger.md
 create mode 100644 notes/syncboostnote/Stolen Content.md
 create mode 100644 notes/syncboostnote/SyncBoostNote.md
Enumerating objects: 16, done.
Counting objects: 100% (16/16), done.
Delta compression using up to 8 threads
Compressing objects: 100% (16/16), done.
Writing objects: 100% (16/16), 12.82 KiB | 2.56 MiB/s, done.
Total 16 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), done.
To github.com:DumbMachine/SyncBoostNoteExample.git
 * [new branch]      master -> master
Everything up-to-date
(base)  dumbmachine@dumbmachine  ~/Boostnote   master  
```
![image](https://user-images.githubusercontent.com/23381512/60123229-9a42a380-97a4-11e9-9da0-e38b4460933d.png)


TODOS:
- [ ] Sorting tags:
  - [ ] Sort the names by tag.
  - [ ] Sort the names by date.
  - [ ] sort the names by name (alphabetically)
- [ ] Delete ``*.md`` file ``*.cson`` has been deleted.
- [ ] Brings in oops.
- [ ] 😢😢😢 Anything other than ``INTERACTIVE`` is executed twice, dunno why pliz halp.
## Thanks to this repo:
- [pycson](https://github.com/avakar/pycson)
  - This helped in saving me alot of time.

