'''
Created on Jun 14, 2020

@author: peter
'''


from dataclasses import dataclass, field
from typing import List

from GDK.DK.Metadata   import Metadata
from GDK.DK.Instrument import Instrument
from GDK.DK.Channel    import Channel

import logging
logger = logging.getLogger(__name__)

@dataclass
class DrumKit(object):
  """
  Central drum kit database
  """
  name:        str              = "kit_name"
  samplerate:  int              = 44100
  metadata:    Metadata         = Metadata()
  channels:    List[Channel]    = field(default_factory=list)
  instruments: List[Instrument] = field(default_factory=list)
  
 
  def __post_init__(self) :
    logger.debug("Running in debug mode ...")

   
  

