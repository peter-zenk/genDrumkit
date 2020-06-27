'''
Created on Jun 14, 2020

@author: peter
'''


_main_comment="\n\
DrumGizmo drumkit created by 'genDrumkit'\n\
Author: Peter Zenk \n\
Email:  email@peterzenk.de \n\
"


from shutil import copy2
from os.path import dirname
import xml.etree.ElementTree as ET

from GDK.EXP.Exporter import Exporter
from GDK.Util import mkdir, dir_exists, file_exists


import logging
logger = logging.getLogger(__name__)

class DgExporter(Exporter):
  """ Drum Gizmo Exporter """

  def __init__(self, drumkit, params):
    super().__init__(drumkit, params)
    logger.debug("Running in debug mode ...")
          
    self._kit_dir = self._drumkit_dir()
    self._midi_fn = self._midi_xml_fn()
    self._kit_fn  = self._kit_xml_fn(params) 
    logger.debug("Exporter '%s' created.", __name__)
    logger.info("Exporting drumkit DB to DrumGizmo format ...")
    
  def export(self):
    self._create_directories()
    self._export_midi_file()
    self._export_drum_kit_file()
    self._export_instr_files()
    self._copy_samples()
    logger.info("Drum kit exported to: '%s'", self._kit_dir)
  
  def _create_directories(self):
    mkdir(self._kit_dir)
 

  """ functions to create XML tree """
  
  def _export_midi_file(self): 
    midimap = ET.Element("midimap")
    for instr in self._drumkit.instruments:
      mp = ET.SubElement(midimap, "map", note=str(instr.midi_note), instr=instr.name)
    
    tree = ET.ElementTree(midimap)
    self._write_xml(tree, self._midi_fn)  

    logger.info("Midi XML created: '" + self._midi_fn + "'")
    
  def _export_drum_kit_file(self): 
    drumkit = ET.Element("drumkit", name=self._drumkit.name, samplerate=str(self._drumkit.samplerate))
    
    drumkit.append(ET.Comment(_main_comment))
    
    metadata      = ET.SubElement(drumkit, "metadata")
    metadata_dict = self._drumkit.metadata.__dict__
    for key, value in metadata_dict.items(): 
      if(key == "image"):
        mi = ET.SubElement(metadata, "logo", src=value)
      else:
        mi = ET.SubElement(metadata, key )
        mi.text = value
    
    channels = ET.SubElement(drumkit, "channels")
    for channel in self._drumkit.channels:
      ch = ET.SubElement(channels, "channel", name=channel.name)
      
    instruments = ET.SubElement(drumkit, "instruments")
    for instrument in self._drumkit.instruments:
      instr = ET.SubElement(instruments, "instrument", name=instrument.name, file=instrument.xml)
      if (instrument.group):
        instr.set("group", instrument.group)
      for chmap in instrument.channelmaps:
        cm = ET.SubElement(instr, "channelmap", {'in':chmap.inp, 'out':chmap.out, 'main':chmap.main})
    
    tree = ET.ElementTree(drumkit)
    self._write_xml(tree, self._kit_fn)
  
    logger.info("Drum kit XML created: '" + self._kit_fn + "'")
  
  def _export_instr_files(self):
    for instrument in self._drumkit.instruments:
      mkdir(self._instrument_dir(instrument))
      self._export_instr_file(instrument)
    logger.info("Instrument XML files created")
  
  def _export_instr_file(self, instrument): 
    xml_fn = self._instrument_xml_fn(instrument)
    instr  = ET.Element("instrument", name=instrument.name, version=instrument.version)
    
    metadata      = ET.SubElement(instr, "metadata")
    metadata_dict = self._drumkit.metadata.__dict__
    for key, value in metadata_dict.items(): 
      if(key == "image"):
        mi = ET.SubElement(metadata, key, filename=value)
      else:
        mi = ET.SubElement(metadata, key )
        mi.text = value
        
    samples = ET.SubElement(instr, "samples")
    for sample in instrument.samples:
      smp = ET.SubElement(samples, "sample", name=sample.name, normalized=sample.normalized, power=str(sample.power))
      for audio in sample.audios:
        mkdir(self._sample_dir(instrument, audio))
        aud = ET.SubElement(smp, "audiofile", channel=audio.channel, 
                            file=audio.file_name, filechannel=str(audio.filechannel))
       
    tree = ET.ElementTree(instr) 
    self._write_xml(tree, xml_fn)
    logger.debug("Intrument XML file created: '" + xml_fn + "'")

  def _write_xml(self, tree, fname):
    tree.write(fname, encoding='utf-8', xml_declaration=True, method="xml")

  
  def _copy_samples(self):
    src_dir = self._params.src_dir
    if not dir_exists(src_dir):
      logger.warning("Samples source directory '%s' not found. Samples not copied", src_dir)
      return
    for instrument in self._drumkit.instruments:
      for sample in instrument.samples:
        for audio in sample.audios:
          src_sample_fn = self._src_sample_fn(instrument, audio)
          if not file_exists(src_sample_fn):
            logger.warning("Sample source file '%s' does not exist! Not copied", src_sample_fn)
            continue
          trg_sample_fn = self._sample_fn(instrument, audio)
          logger.debug("Copying '%s' to '%s'...", src_sample_fn, trg_sample_fn )
          copy2(src_sample_fn, trg_sample_fn)
    logger.info("Samples copied from '%s'", src_dir)
    
        
    
  """  Directory pathname construction """  
  
  def _drumkit_dir(self) -> str:
    return(self._params.out_dir + "/" + self._drumkit.name)
  
  def _instrument_dir(self, instrument) -> str:
    return(self._drumkit_dir() + "/" + instrument.name)  
   
  def _sample_dir(self, instrument, audio) -> str:
    return(self._instrument_dir(instrument) + "/" + dirname(audio.file_name))
   
  """ XML file name construction """
  
  def _midi_xml_fn(self) -> str:
    return(self._drumkit_dir() + "/" + self._drumkit.name + "-midi.xml")
    
  def _kit_xml_fn(self, params) -> str:
    return(self._drumkit_dir() + "/" + self._drumkit.name + "-kit.xml")
 
  def _instrument_xml_fn(self, instrument) -> str:
    return(self._drumkit_dir() + "/" + instrument.xml)
   
  """ Sound sample file name construction """
  
  def _sample_fn(self, instrument, audio) -> str:
    return(self._instrument_dir(instrument) + "/" + audio.file_name)
   
  def _src_sample_fn(self, instrument, audio) -> str: 
    if self._params.samples_src_pol == "TRG":
      return(self._params.src_dir + "/" + instrument.name + "/" + audio.file_name)
    if self._params.samples_src_pol == "USE":
      return(self._params.src_dir + "/" + audio.src_fn)


  """ utility functions """
    