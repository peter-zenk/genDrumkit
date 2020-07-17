'''
Created on Jun 14, 2020

@author: peter
'''


from dataclasses import dataclass, field
from typing import List
import logging

from gen_drum_kit.drum_kit.Metadata   import Metadata
from gen_drum_kit.drum_kit.Instrument import Instrument
from gen_drum_kit.drum_kit.Channel    import Channel


logger = logging.getLogger(__name__)

@dataclass
class DrumKit():
    """
    Central drum kit data base
    """
    name:        str              = "kit_name"
    samplerate:  int              = 44100
    metadata:    Metadata         = Metadata()
    channels:    List[Channel]    = field(default_factory=list)
    instruments: List[Instrument] = field(default_factory=list)


    def __post_init__(self) :
        logger.debug("Running in debug mode ...")
