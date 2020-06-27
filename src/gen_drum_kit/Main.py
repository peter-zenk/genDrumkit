'''
Created on Jun 14, 2020

@author: peter
'''


import sys
from shutil import rmtree
from platform import system

from GDK.Parameter import Parameter
from GDK.Factory   import ImporterFactory, ExporterFactory

import logging
logger = logging.getLogger(__name__)


class Main(object):

  def __init__(self):
    self._impFactory = ImporterFactory()
    self._expFactory = ExporterFactory()
    
  def _check_environment(self):
    """See that the no old version of python is used"""

    if sys.hexversion < 50856688:
      print("INFO: Your version of python is " + str(sys.version_info))
      sys.exit("ERROR: You must use at least python 3.8.2. Aborting ...")
      
    if system() != "Linux":
      print("INFO: You are running on :", system())
      sys.exit("ERROR: You must run on a 'Linux' system!")
   
  def _init_program(self):
    self._check_environment() 
    self._params = Parameter()

  def _cleanup(self):
    logger.info("Cleaning up ...")
    for item in self._params.clean_rm:
      logger.debug("Removing '%s' ...", item)
      try: 
        rmtree(item)
      except:
        logger.error("Could not remove '%s'!", item)
  
  def run(self):

    """Do the main script processing"""
    self._init_program()
    logger.debug("Running in debug mode")   

    Imp = self._impFactory.create(self._params)
    Imp.load()
    
    Drumkit = Imp.createDrumkit()
    logger.debug(Drumkit)

    Exp = self._expFactory.create(Drumkit, self._params)
    Exp.export()
    
    self._cleanup()

    logger.debug("Finished program ...")
    logger.info("Finished program ...")


