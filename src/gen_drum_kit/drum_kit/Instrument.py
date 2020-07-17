'''
Created on Jun 15, 2020

@author: peter
'''
from dataclasses import dataclass, field
from typing import List
import logging

from gen_drum_kit.drum_kit.Metadata   import Metadata
from gen_drum_kit.drum_kit.ChannelMap import ChannelMap
from gen_drum_kit.drum_kit.Sample     import Sample


logger = logging.getLogger(__name__)

@dataclass
class Instrument():
    """ info for an instrument (drum) """
    name:              str      = "<instr_name>"
    version:           str      = "2.0"
    metadata:          Metadata = Metadata()
    midi_note:         int      = 36
    xml:               str      = "<instr_xml_filename>"
    group:             str      = ""
    channelmaps: List[ChannelMap]    = field(default_factory=list)
    samples:     List[Sample]        = field(default_factory=list)

    def __post_init__(self) :
        logger.debug("Running in debug mode ...")
