'''
Created on Jun 15, 2020

@author: peter
'''

from typing import List
from dataclasses import dataclass, field
import logging

from gen_drum_kit.drum_kit.Audio import Audio


logger = logging.getLogger(__name__)

@dataclass
class Sample():
    """ info for a specific sample of an instrument """
    # kit_name:    str = "<kit>"
    name:        str = "<instr_sample>"
    normalized:  str = "true"
    power:       int = 1.0
    audios: List[Audio]    = field(default_factory=list)

    def __post_init__(self):
        logger.debug("Running in debug mode ...")
