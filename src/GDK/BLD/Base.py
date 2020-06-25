'''
Created on Jun 17, 2020

@author: peter
'''

import abc


import logging
logger = logging.getLogger(__name__)

class BLD_Base(metaclass=abc.ABCMeta):
  '''
    classdocs
  '''

  def __init__(self, params):
    self._params = params

  @abc.abstractmethod   
  def buildDrumkit(self): pass  