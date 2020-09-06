#!/usr/bin/env python3
"""
| ------------------------------------------------------------
| fileculator.py
| ------------------------------------------------------------
| This scripts calculates the total size of the 'storage/app'
| directory (user uploaded files) of multiple Laravel apps.
| Define the project root and depth in .env file and run
| the script as a cron job.
|
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import dotenv_values

print('Reading parameters from .env file...')
params = dotenv_values(dotenv_path='.env')


def get_project_root():
    """Determine the project root"""
    try:
        return params['PROJECT_ROOT']
    except KeyError as error:
        print("Error! Project root is not defined. You must set a project root in .env file.")
        sys.exit(1)


def get_project_depth():
    """Determine the project depth, if failed, return the default."""
    try:
        default = 2
        valid_depths = (1, 2)
        depth = int(params['PROJECT_DEPTH'])
        if depth not in valid_depths:
            raise ValueError(
                'Error! Invalid value defined for depth, value must be between 1 and 2.')
        return depth
    except KeyError as error:
        print('PROJECT_DEPTH key is missing, fallback to default: 2')
        return default
    except ValueError as error:
        print(error)
        sys.exit(1)


def is_storage_only():
    """Check if only storage folder is to calculate, True by default"""
    try:
        return True if int(params['STORAGE_ONLY']) == 1 else False
    except KeyError as error:
        print("Key is not defined in .env, fallback to default: True")
        return True
    except ValueError as error:
        print("Key is not defined in .env, fallback to default: True")
        return True


def get_pattern():
    """Get the pattern to search for laravel directories"""
    return '*' * get_project_depth() + '/*storage/app'


def validate_root_directory():
    """Check if the provided root directory is valid."""
    try:
        root = Path(get_project_root())
        if not os.path.exists(root):
            raise IOError('Error! Project directory not found, aborting...')
        return root
    except IOError as error:
        print(str(error))
        sys.exit(1)


def get_walkable_dirs(public_directory):
    """
    Determine which directories in a Project should be included in
    final count, if STORAGE_ONLY key is set to 1, only the size of
    storage directory will be calculated, else the whole project size.
    :param public_directory: Public path of an individual project directory
    """
    return public_directory.glob('**/*') \
        if is_storage_only() \
        else public_directory.parent.parent.glob('**/*')


def sum_size(walkable_dirs):
    """
    Sum the size of files inside specified directory and it's subdirectories.
    :param walkable_dirs: List of dirs and subdirs in an individual project directory
    :return: Total filesize in bytes
    """
    return sum(file.stat().st_size for file in walkable_dirs if file.is_file())


def write_storage_usage(path, total_size):
    """
    Write storage usage info in defined path.
    :param path: The file path to store storage info.
    :param total_size: Total calculated size.
    """
    data = {
        'size': total_size,
        'written_at': str(datetime.now())
    }
    with open(str(path), 'w') as storage_file:
        json.dump(data, storage_file)
    storage_file.close()


def calculate(public_directory):
    """
    Calculate the size of the specified directory.
    :param public_directory: Public path of an individual project directory
    """
    total_size = sum_size(get_walkable_dirs(public_directory))
    print('%s has %s of files' %
          (public_directory, human_readable_size(total_size)))
    # We'll be keeping the storage info inside storage/app, since
    # this file is not and should not be included in any vcs.
    write_storage_usage(public_directory.joinpath('storage.json'), total_size)


def walk():
    """
    Calculate total size of user uploaded files in storage/app directory and
    write the size information in a json file inside the public directory.
    """
    # Validate project directory
    ROOT_DIRECTORY = validate_root_directory()
    
    # The glob for searching
    LARAVEL_PATTERN = get_pattern()
    
    # Search and get the Laravel projects, in this case, we are
    # targeting directories which has /storage/app subdirectory,
    # i.e. where user uploaded files reside.
    print('Searching for directories...\n')
    # Holds list of the public paths of founded individual projects
    repositories = ROOT_DIRECTORY.glob(LARAVEL_PATTERN)
    
    count = 0
    for public_directory in repositories:
        try:
            # Check if it's not a directory, mainly for safekeeping
            if not public_directory.is_dir():
                continue
            calculate(public_directory)
            count += 1
        except IOError as error:
            print(error)
            continue
    print('\nWritten in %d directories.' % count)
    print('\nExecution finished at: ' + str(datetime.now()))


def human_readable_size(nbytes):
    """
    Converts bytes to human readbale form like MB, KB, GB etc.
    Taken from https://bit.ly/2rXUMg9
    """
    suffixes = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def run():
    """
    Shows primary info and initiates the calculation process.
    """
    try:
        if not params:
            raise FileNotFoundError("Error! .env file is not found.")
        
        print("""
        Project Root:           %s
        Project Depth:          %s
        """ % (get_project_root(), get_project_depth()))
        
        walk()
        return
    except FileNotFoundError as error:
        print(error)


if __name__ == "__main__":
    run()
