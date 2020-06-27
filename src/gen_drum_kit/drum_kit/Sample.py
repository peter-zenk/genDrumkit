'''
Created on Jun 15, 2020

@author: peter
'''

from typing import List
from dataclasses import dataclass, field

from GDK.DK.Audio import Audio

import logging
logger = logging.getLogger(__name__)

@dataclass
class Sample(object):
  #kit_name:    str = "<kit>"
  name:        str = "<instr_sample>"
  normalized:  str = "true"
  power:       int = 1.0
  audios: List[Audio]    = field(default_factory=list)

  def __post_init__(self):
    logger.debug("Running in debug mode ...")
  

        