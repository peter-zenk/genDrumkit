'''
Created on Jun 17, 2020

@author: peter
'''


from gen_drum_kit.drum_kit.DrumKit     import DrumKit
from gen_drum_kit.drum_kit.Instrument  import Instrument
from gen_drum_kit.drum_kit.Channel     import Channel
from gen_drum_kit.drum_kit.ChannelMap  import ChannelMap
from gen_drum_kit.drum_kit.Sample      import Sample
from gen_drum_kit.drum_kit.Audio       import Audio
from gen_drum_kit.drum_kit.Metadata    import Metadata

from gen_drum_kit.builder.builder_base import Builder_Base



import logging
logger = logging.getLogger(__name__)


class Builder_Filesystem(Builder_Base):

  def __init__(self, params, map):
    super().__init__(params)
    self._map = map
  
  def buildDrumkit(self):
    logger.info("Building drumkit DB from Hydrogen data ...")
    self._prepare()
    
    if self._params.HG_mode == "TPL":
      logger.info("TPL: Creating map template file only")
      self._create_channelmap_template()
      logger.info("Program finished")
      exit(0)
      
    self._drumkit = DrumKit(name=self._params.drumkit_name)
    self._add_metadata()
    self._add_instruments()
    self._add_channels()
    return(self._drumkit)
  
  
  """ private functions """
  
  def _prepare(self): pass

  def _add_metadata(self):
    author     =  'author'
    email      =  'email'
    name       =  'name'
    info       =  'info'
    licens     =  'license'
    image      =  'image'
   
    self._drumkit.metadata = Metadata(title=name, image=image, notes=name, description= info, 
                                   license=licens, author=author, email=email)
 
  def _add_instruments(self): pass
 
  def _add_channels(self): pass

    
    