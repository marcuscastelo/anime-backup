#!/usr/bin/python
import os
from os import path

import datetime


# Most likely not changing
SETTINGS_FILENAME = 'settings.cfg'

print('WARNING: this is a personal project, so it 99% will not work on your computer')

# Determine if Windows or Linux
IS_WINDOWS = False
if os.name == 'nt':
    print('INFO: running on windows.')
    IS_WINDOWS = True
else:
    print('INFO: running on Linux')

# Assert single file
if __name__ != "__main__":
    print('ERROR: backup.py is not a module, it must not be imported')
    exit(1)

#################
## ACTUAL CODE ##
#################

CWD = os.getcwd()
settings_filep = path.join(CWD, SETTINGS_FILENAME)

settings = {}

def _generate_settings():
    settings_file = open(settings_filep, 'w+')
    if settings_file.mode != 'w+':
        print('ERROR: failed to generate new',SETTINGS_FILENAME)
        exit(2)
    settings_file.writelines([
        'OLD_FOLDER=old' + ( 'Windows' if IS_WINDOWS else 'Linux' ) + '\n',
        'MAX_AGE=30\n', #days
        'FILE_BASENAME=animes\n',
        'FILE_EXT=.txt\n'
    ])
    settings_file.close()

def load_settings():
    print('> INFO: loading settings...')
    
    if not path.exists(path.join(CWD, SETTINGS_FILENAME)):
        print('WARNING: settings file not found! generating a blank one...')
        _generate_settings()
    settings_file = open(settings_filep, 'r')

    if settings_file.mode != 'r':
        print('ERROR: failed to load',SETTINGS_FILENAME)
        exit(3)

    lines = settings_file.readlines()
    for line in lines:
        prop, value = line.split('=')
        settings[prop] = value
    settings_file.close()
    print('INFO: settings loaded sucessfully')

def gen_bkp_name():
    return settings['FILE_BASENAME'][:-1] + (datetime.datetime.now().replace(microsecond=0).isoformat().replace(':','-').replace('T','-T-')) + settings['FILE_EXT']

def assert_old_folder():
    print('INFO: asserting OLD_FOLDER...')
    if not path.exists(path.join(CWD, settings['OLD_FOLDER'][:-1])):
        print('WARNING: OLD_FOLDER not found, creating it!')
        os.makedirs(settings['OLD_FOLDER'][:-1])
    else:
        print('OK')


def make_bkp():
    load_settings()
    print('> INFO: Starting backup')
    bkp_name = gen_bkp_name()
    print('INFO: generated name:',bkp_name)

    assert_old_folder()

    curr_filep = path.join(CWD, settings['FILE_BASENAME'][:-1] + settings['FILE_EXT'][:-1])
    bkp_filep = path.join(CWD, settings['OLD_FOLDER'][:-1], bkp_name)

    if not path.exists(curr_filep):
        print('ERROR: file to backup doesn\'t exist:',curr_filep)

    print('>> INFO: copying file %s to %s' % (curr_filep, bkp_filep))
    command = 'cp %s %s' % (curr_filep, bkp_filep)
    # print(command)
    os.system('cp %s %s' % (curr_filep, bkp_filep))
    print('Task completed')


make_bkp()