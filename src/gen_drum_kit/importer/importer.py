'''
Created on Jun 14, 2020

@author: peter
'''

import abc


import logging
logger = logging.getLogger(__name__)


class Importer(metaclass=abc.ABCMeta):
    '''
    Abstract base class for converter
    '''
    def __init__(self, params):
      logger.debug("Running in debug mode ...")
      self._params = params
   
    @abc.abstractmethod  
    def load(self): pass
    
    @abc.abstractmethod     
    def createDrumkit(self) : pass

    
    
    