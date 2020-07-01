'''
Created on Jun 14, 2020

@author: peter

Factories to generate various importers and exporters
'''

from gen_drum_kit.importer.importer_hydrogen  import ImporterHydrogen
from gen_drum_kit.importer.importer_dummy     import ImporterDummy

from gen_drum_kit.exporter.exporter_drumgizmo import Exporter_Drumgizmo

import logging
from gen_drum_kit.importer.importer_filesystem import ImporterFS
logger = logging.getLogger(__name__)



class ImporterFactory(object):
  """ The importer factory """
  
  def __init__(self):
    logger.debug("Running in debug mode")   
  
  def create(self, param):
    """ create the importer object based on the value of 'param' """
    name = param.impFmt
    logger.debug("Creating importer '%s'", name)
    if (name == "DUMMY"):
      return(ImporterDummy(param))
    if (name == "HG"):
      return(ImporterHydrogen(param))
    if (name == "FS"):
      return(ImporterFS(param))
    raise ValueError(name)
  
class ExporterFactory(object):
  """ The exporter factory """
  
  def __init__(self):
    logger.debug("Running in debug mode")   
  
  def create(self, drumkit, param):
    """ create the exporter object based on the value of 'param' """
    name = param.expFmt
    logger.debug("Creating exporter '%s'", name)
    if (name == "DG"):
      return(Exporter_Drumgizmo(drumkit, param))
    raise ValueError(name)