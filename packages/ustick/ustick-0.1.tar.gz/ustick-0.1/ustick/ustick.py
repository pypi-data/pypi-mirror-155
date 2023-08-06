#!/usr/bin/env python3
"""
Usage:
    ustick [options]

Options:
    -a --add <message>   add notes
    -s --show            show notes table
    -f --find <keyword>  find cards by the word
    -d --delete <id>     remove note by id
    --remove-all         remove all notes
"""

from termcolor import colored
from datetime import datetime
from docopt import docopt
from pathlib import Path
from random import randint
import os
import yaml
import sys
import textwrap


NOTE_FILE = str(Path.home()) + "/.notes"
NOTE_ROWS = 4
NOTE_WIDTH = 22


class Note:
    
    def __init__(
                 self,
                 message,
                 timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 ID=randint(1000, 10000)
                ):
        self.Message = message
        self.timestamp = timestamp
        self.ID = ID

    def getNote(self):
        try:
            noteWrapper = textwrap.TextWrapper(width=NOTE_WIDTH)
            wrappedNote = noteWrapper.wrap(text=self.Message)
            assert len(wrappedNote) < NOTE_ROWS
        except AssertionError:
            print('This note is too large!')
            sys.exit(1)

        return {
                 'ID': self.ID,
                 'message': self.Message,
                 'timestamp': self.timestamp
               }


def addSticker(message, noteFile=NOTE_FILE):
    try:
        if not os.path.exists(noteFile):
            os.mknod(noteFile)
        with open(noteFile, 'r+') as inf:
            notes = readNoteFile()
            if notes is None:
                notes = []

            note = Note(message)
            notes.append(note.getNote())
            inf.write(
                     yaml.dump(notes)
                     )
    except Exception as err:
        print("Error adding a note: %s." % err)
        sys.exit(1)


def deleteSticker(ID, noteFile=NOTE_FILE):
    notes = readNoteFile()
    for note in notes:
        if note['ID'] == ID:
            notes.remove(note)
    with open(noteFile, 'w') as inf:
        inf.write(yaml.dump(notes))


def findSticker(keyword):
    notes = readNoteFile()
    targetNotes = []
    for note in notes:
        if keyword in str(note['ID']) or keyword in note['message']:
            targetNotes.append(note)
    if len(targetNotes) > 0:
        showNotes(targetNotes, keyword)
    else:
        print("There isn't such sticker.")
        sys.exit(0)


def removeAll(noteFile=NOTE_FILE):
    answer = None
    while answer not in ("yes", "no"):
        answer = str(
                    input('Are you sure to remove all notes?'+' (yes/no): ')
                    ).lower().strip()
        if answer == 'yes':
            open(noteFile, 'w').close()
        if answer == 'no':
            sys.exit(0)


def showStickers():
    notes = readNoteFile()
    if notes is None:
        print("There aren't any notes.")
        sys.exit(0)
    showNotes(notes)


def showNotes(notes, replStr=None):
    printedNotes = []
    for note in notes:
        printedNotes.append(getPrintedNote(note, replStr))
    while len(printedNotes) >= 3:
        for line in range(NOTE_ROWS+2):
            print(
                  printedNotes[0][line],
                  printedNotes[1][line],
                  printedNotes[2][line]
                 )
        del printedNotes[0:3]
    if len(printedNotes) == 2:
        for line in range(NOTE_ROWS+2):
            print(
                  printedNotes[0][line],
                  printedNotes[1][line]
            )
    elif len(printedNotes) == 1:
        for line in range(NOTE_ROWS+2):
            print(
                  printedNotes[0][line]
                 )


def getPrintedNote(raw_note, replStr=None):
    printedNote = []
    note = Note(
                ID=raw_note["ID"],
                message=raw_note["message"],
                timestamp=raw_note["timestamp"])
    noteWrapper = textwrap.TextWrapper(width=NOTE_WIDTH)
    wrappedNote = noteWrapper.wrap(text=note.Message)
    if len(wrappedNote) < NOTE_ROWS:
        for i in range(NOTE_ROWS-len(wrappedNote)):
            wrappedNote.append(NOTE_WIDTH*' ')
    printedNote.append('/=' + '#' + str(note.ID) + str((NOTE_WIDTH-6)*'=') + '\\')
    for line in wrappedNote:
        if len(line) <= NOTE_WIDTH:
            line = line + ' '*(NOTE_WIDTH - len(line))
            if replStr is not None:
                line = line.replace(
                                    replStr,
                                    colored(replStr, 'red')
                                    )
            printedNote.append("|" + line + "|")
    printedNote.append('\\' + str(NOTE_WIDTH*'=') + '/')
    return printedNote


def readNoteFile(noteFile=NOTE_FILE):
    with open(noteFile, 'r') as inf:
        try:
            notes = yaml.safe_load(inf)

            if notes is None:
                return None

        except Exception as err:
            print("Error reading file with notes: %s." % err) 
            sys.exit(1)
    return notes
    

def printLine(line):
    print('|' + line + '|')


def main():
    arguments = docopt(__doc__, version="ustick.py v0.1")
    show = arguments['--show']
    add = arguments['--add']
    delete = arguments['--delete']
    find = arguments['--find']
    remove = arguments['--remove-all']
    try:
        if add is not None:
            addSticker(add)
        elif delete is not None:
            deleteSticker(int(delete))
        elif find is not None:
            findSticker(find)
        elif remove:
            removeAll()
        elif show is not False:
            showStickers()
        else:
            showStickers()
    except AttributeError:
        print('There is no stickers')
    except FileNotFoundError:
        print("Note file doesn't exist.")
    except Exception as err:
        print('Error working with stickers: %s.' % err)


if __name__ == '__main__':
    main()
