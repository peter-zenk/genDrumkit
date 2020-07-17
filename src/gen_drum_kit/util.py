'''
Created on Jun 19, 2020

@author: peter

global utility functions
'''

from pathlib import Path


def decomment(csvfile):
    """ remove comments from CSV file """
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw:
            yield row


def mkdir(path):
    """ short cut """
    Path(path).mkdir(parents=True, exist_ok=True)


def dir_exists(path):
    """ short cut """
    return(Path(path).is_dir())


def file_exists(path):
    """ short cut """
    return(Path(path).is_file())
