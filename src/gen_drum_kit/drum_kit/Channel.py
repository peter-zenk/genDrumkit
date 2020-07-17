'''
Created on Jun 15, 2020

@author: peter
'''

from dataclasses import dataclass


@dataclass
class Channel():
    """ info about a audio output channel """
    name: str = "channel"
