'''
Created on Jun 14, 2020

@author: peter
'''

from GDK.IMP.HgImporter    import HgImporter
from GDK.IMP.DummyImporter import DummyImporter

from GDK.EXP.DgExporter import DgExporter

import logging
logger = logging.getLogger(__name__)



class ImporterFactory(object):
  
  def __init__(self):
    logger.debug("Running in debug mode")   
  
  def create(self, param):
    name = param.impFmt
    logger.debug("Creating importer '%s'", name)
    if (name == "DUMMY"):
      return(DummyImporter(param))
    if (name == "HG"):
      return(HgImporter(param))
    raise ValueError(name)
  
class ExporterFactory(object):
  
  def __init__(self):
    logger.debug("Running in debug mode")   
  
  def create(self, drumkit, param):
    name = param.expFmt
    logger.debug("Creating exporter '%s'", name)
    if (name == "DG"):
      return(DgExporter(drumkit, param))
    raise ValueError(name)