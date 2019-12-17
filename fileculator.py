#! /usr/bin/python3
#
# ------------------------------------------------
# fileculator.py
# ------------------------------------------------
# Calculates the total size of a user defined directory and stores the data
# in a json file. It created to calculate total size of user uploaded files
# in CGIT digital ocean server. It targets all Laravel projects and puts
# the calculated file size as a json file in storage/app directory. You
# should run the file as a cron job.
#
# Author: Sowren Sen
# Email: sowrensen@gmail.com

import os
from pathlib import Path
from hurry.filesize import size, alternative
from datetime import datetime
import json


def calculate_size(project_root, project_depth):
    """
    Calculate total size of user uploaded files in Laravel projects and
    write the size information in a json file inside apps public directory.
    """
    # Get the absolute path
    ROOT_DIRECTORY = Path.joinpath(Path.home(), project_root)
    
    # The glob for searching
    TARGET_LARAVEL_DIRECTORY = '*' * int(project_depth) + '/*storage/app'
    
    # Search and get the Laravel projects, in this case, we are
    # targeting directories which has /storage/app subdirectory,
    # i.e. where user uploaded files reside.
    PUBLIC_PATH = ROOT_DIRECTORY.glob(TARGET_LARAVEL_DIRECTORY)
    for public_directory in PUBLIC_PATH:
        # Check if it's not a directory, mainly for safekeeping
        if not public_directory.is_dir():
            continue
        # Calculate the total size of /storage/app directory
        total_size = 0
        total_size = sum(
            file.stat().st_size for file in public_directory.glob('**/*') if file.is_file())  # Total file size in bytes
        print('%s has %s of files' % (public_directory, size(total_size, system=alternative)))
        # Json file path, we'll be keeping it inside storage/app, since
        # this file is not and should not be included in any vcs.
        path = public_directory.joinpath('storage.json')
        # Prepare the data as a dictionary
        data = {
            'size': total_size,
            'written_on': str(datetime.now())
        }
        # Try to write the data into the file, else throw error and continue
        try:
            with open(str(path), 'w') as storage_file:
                json.dump(data, storage_file)
            storage_file.close()
        except IOError as error:
            print(error)
            continue


def run():
    """
    Initializes environment variables and runs main program.
    """
    try:
        valid_depths = (1, 2)
        print('Reading variables...')
        project_root = os.environ['PROJECT_ROOT']
        project_depth = os.environ['PROJECT_DEPTH']
        if int(project_depth) not in valid_depths:
            raise ValueError('Error! Invalid value defined for depth, value must be between 1 and 2.')
        calculate_size(project_root, project_depth)
        return
    except ValueError as error:
        print(error)
    except KeyError as error:
        print('Error! Please define necessary keys in .env file.')


run()