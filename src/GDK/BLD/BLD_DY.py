'''
Created on Jun 17, 2020

This class builds a default Drumkit object

@author: peter
'''
from GDK.DK.DrumKit    import DrumKit
from GDK.DK.Instrument import Instrument
from GDK.DK.Channel    import Channel
from GDK.DK.ChannelMap import ChannelMap
from GDK.DK.Sample     import Sample
from GDK.DK.Audio      import Audio

from GDK.BLD.Base import BLD_Base

import logging
logger = logging.getLogger(__name__)


class BLD_Dummy(BLD_Base):
  
  def __init__(self, params):
    super().__init__(params)
 
  def buildDrumkit(self):
    logger.info("Building dummy drumkit DB ...")
    if not self._params.drumkit_name:
      logger.warning("Name for drum kit not specified. Using 'mykit' ...")
      self._params.drumkit_name = "mykit"
    self._drumkit = DrumKit(name=self._params.drumkit_name)
    self._add_instruments()
    self._add_channels()
    return(self._drumkit)
 
  """ private functions """
     
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

      """ 2 main channelmaps as default """
      if not group: outch=instr
      else:         outch=group
      instrument.channelmaps.append(ChannelMap(inp=(instr + "_R"), out=(outch + "_R"), main="true"))
      instrument.channelmaps.append(ChannelMap(inp=(instr + "_L"), out=(outch + "_L"), main="true"))

      """ 1 samples with 2 audios as default """
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