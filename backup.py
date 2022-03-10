#!/usr/bin/python
import os
from os import path
import platform

import datetime
from logger import Logger
LOGGER = Logger()

# Most likely not changing
SETTINGS_FILENAME = 'settings.cfg'

# Determine if Windows or Linux
def get_os():
    return platform.system() or 'UnknownOS'

SETTINGS_FILEPATH = path.join(os.getcwd(), SETTINGS_FILENAME)
settings = {}

def _generate_settings():
    with open(SETTINGS_FILEPATH, 'w+') as settings_file:
        if settings_file.mode != 'w+':
            LOGGER.log_error('Failed to generate new',SETTINGS_FILEPATH)
            exit(2)

        settings_file.writelines([
            f"OLD_FOLDER=old{get_os()}\n",
            f"MAX_AGE=30\n", #days
            f"FILE_BASENAME=anilist\n",
            f"FILE_EXT=.anl\n"
        ])

def load_settings():
    LOGGER.log_info('Loading settings...')
    if not path.exists(path.join(os.getcwd(), SETTINGS_FILEPATH)):
        LOGGER.log_warning('Settings file doesn\'t exist, creating it')
        _generate_settings()

    with open(SETTINGS_FILEPATH, 'r') as settings_file:
        if settings_file.mode != 'r':
            print('ERROR: failed to load',SETTINGS_FILEPATH)
            exit(3)

        lines = settings_file.readlines()
        for line in lines:
            prop, value = line.split('=')
            settings[prop] = value

    LOGGER.log_info('Settings loaded successfully')

def gen_backup_filename() -> str:
    time_postfix = datetime.datetime.now().replace(microsecond=0).isoformat().replace(':','-').replace('T','-T-')
    basename = settings['FILE_BASENAME'][:-1]
    ext = settings['FILE_EXT'][:-1]
    return f'{basename}-{time_postfix}{ext}'

def create_old_folder_if_not_exists():
    LOGGER.log_trace('Checking if old folder exists...')
    if path.exists(path.join(os.getcwd(), settings['OLD_FOLDER'][:-1])):
        LOGGER.log_trace('Old folder already exists, using it')
    else:
        LOGGER.log_trace('Old folder doesn\'t exist, creating it')
        os.makedirs(settings['OLD_FOLDER'][:-1])

def make_bkp(original_filepath: str, backup_filepath: str):
    os.system('cp %s %s' % (original_filepath, backup_filepath))

def main():
    LOGGER.log_info('Loading settings...')
    load_settings()

    cwd = os.getcwd()

    backup_filename = gen_backup_filename()

    create_old_folder_if_not_exists()
    original_filepath =  path.join(cwd, settings['FILE_BASENAME'][:-1] + settings['FILE_EXT'][:-1])
    backup_filepath = path.join(cwd, settings['OLD_FOLDER'][:-1], backup_filename)

    LOGGER.log_info(f'Backing up file {original_filepath} to {backup_filepath}')
    if path.exists(original_filepath):
        make_bkp(original_filepath, backup_filepath)
        LOGGER.log_info('Backup complete')
    else:
        LOGGER.log_error(f'File {original_filepath} doesn\'t exist')
        exit(1)

    LOGGER.log_info('Exiting...')

if __name__ == "__main__":
    main()
    pass