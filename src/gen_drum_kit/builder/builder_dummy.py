'''
Created on Jun 17, 2020

This class builds a default Drumkit object

@author: peter
'''

import logging

from gen_drum_kit.drum_kit.DrumKit     import DrumKit
from gen_drum_kit.drum_kit.Instrument  import Instrument
from gen_drum_kit.drum_kit.Channel     import Channel
from gen_drum_kit.drum_kit.ChannelMap  import ChannelMap
from gen_drum_kit.drum_kit.Sample      import Sample
from gen_drum_kit.drum_kit.Audio       import Audio

from gen_drum_kit.builder.builder_base import Builder_Base


logger = logging.getLogger(__name__)


class Builder_Dummy(Builder_Base):
    """ creates a default drum kit from hard-coded parameters """

    def __init__(self, params):
        super().__init__(params)
        self._drumkit = None # assigned later

    def buildDrumkit(self):
        logger.info("Building dummy drumkit DB ...")
        if not self._params.drumkit_name:
            logger.warning("Name for drum kit not specified. Using 'mykit' ...")
            self._params.drumkit_name = "mykit"
        self._drumkit = DrumKit(name=self._params.drumkit_name)
        self._add_instruments()
        self._add_channels()
        return(self._drumkit)

    ### private functions ----------------------

    def _add_instruments(self):
        dk     = self._drumkit
        instrs = self._drumkit.instruments
        Instruments = [
          ("Kick",     38, ""),
          ("Snare",    40, ""),
          ("HHclosed", 42, "HiHat"),
          ("HHopen",   46, "HiHat"),
          ("Ride",     51, ""),
          ("TomH",     50, ""),
          ("TomM",     48, ""),
          ("TomL",     45, ""),
        ]
        for instr, midi, group in Instruments:
            instrument = Instrument(name=instr, midi_note=midi, metadata=dk.metadata, group=group)
            instrument.xml = instr + "/" + instr + ".xml"

            # 2 main channel maps as default
            if not group: 
                outch=instr
            else:         
                outch=group
            instrument.channelmaps.append(ChannelMap(inp=(instr + "_R"), out=(outch + "_R"), main="true"))
            instrument.channelmaps.append(ChannelMap(inp=(instr + "_L"), out=(outch + "_L"), main="true"))

            # 1 samples with 2 audios as default
            sample=Sample(name=instr)
            sample.audios.append(Audio(channel=(instr+"_R"), file_name="samples/"+instr+".wav", filechannel=1))
            sample.audios.append(Audio(channel=(instr+"_L"), file_name="samples/"+instr+".wav", filechannel=2))
            instrument.samples.append(sample)

            instrs.append(instrument)

    def _add_channels(self):
        channels = self._drumkit.channels
        Channels = [
          "Kick_R",
          "Kick_L",
          "Snare_R",
          "Snare_L",
          "HiHat_R",
          "HiHat_L",
          "Ride_R",
          "Ride_L",
          "TomH_R",
          "TomH_L",
          "TomM_R",
          "TomM_L",
          "TomL_R",
          "TomL_L",
         ]
        for ch in Channels:
            channels.append(Channel(name=ch))
