'''
Created on Jun 14, 2020

@author: peter
'''

import abc
import csv
from gen_drum_kit.util   import decomment

import logging
logger = logging.getLogger(__name__)


class ImporterBase(metaclass=abc.ABCMeta):
    '''
    Abstract base class for converter
    '''
    def __init__(self, params):
      logger.debug("Running in debug mode ...")
      self._params = params
   
    @abc.abstractmethod  
    def importData(self): 
      """ """
      pass
    
    @abc.abstractmethod     
    def buildDrumkitDB(self) : 
      """ create the internal drum kit data base """
      pass

    def _read_map_file(self):
      self._channel_map = []
      fn                = self._params.map_fn
      try:
        logger.info("Reading map file '%s' ...", fn)
       
        with open(fn) as csvfile:
          reader = csv.reader(decomment(csvfile))
          for row in reader:
            self._channel_map.append(row)   
      except:
        logger.warning("Could not read channel map file '%s'. Using default mapping ...", fn)
        return()
  
      logger.debug(self._channel_map)
    
    