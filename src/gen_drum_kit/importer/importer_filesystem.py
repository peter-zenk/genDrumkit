'''
Created on Jun 14, 2020

@author: peter
'''

from gen_drum_kit.importer.importer_base import ImporterBase


import logging
from gen_drum_kit.builder.builder_filesystem import Builder_Filesystem
logger = logging.getLogger(__name__)



class ImporterFS(ImporterBase):

  def __init__(self, params):
    super().__init__(params)
    logger.debug("Running in debug mode ...")
    logger.debug("ImporterBase '%s' created.", __name__)

  def importData(self):

    self._read_map_file()
    

  """ private functions """
  
  def _createBuilder(self): 
    """ create and return the builder """ 
    logger.info("Creating default drum kit from file system data!") 
    return(Builder_Filesystem(params=self._params, mapDB=self._channel_map))
    