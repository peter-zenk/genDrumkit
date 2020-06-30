'''
Created on Jun 14, 2020

@author: peter
'''

from gen_drum_kit.importer.Importer import Importer
import sys
import re
import csv
import tarfile
import gzip
from os import path
import xml.etree.ElementTree as ET

import logging
logger = logging.getLogger(__name__)

from gen_drum_kit.drum_kit.DrumKit import DrumKit
from gen_drum_kit.builder.BLD_HG import BLD_HG
from gen_drum_kit.Util import decomment, dir_exists

class HgImporter(Importer):

  def __init__(self, params):
    super().__init__(params)
    logger.debug("Running in debug mode ...")
    logger.debug("Importer '%s' created.", __name__)

  def load(self):
    self._prepare()
    """ Load drumkit info from XML file and create a drumkit object"""
    logger.info("Loading Hydrogen XML file '%s'...", self._params.HG_xml)
    self._xml = self._read_xml(self._params.HG_xml)
    self._debug_print() # only in debug mode
    self._read_map_file()
    
  def createDrumkit(self):  
    logger.info("Creating drum kit from Hydrogen data.")    
    Builder = BLD_HG(params=self._params, xml=self._xml, map=self._channel_map)
    drumkit = Builder.buildDrumkit()

    return(drumkit)
  

  """ private functions """
  
  def _read_xml(self, HG_xml):
    try:
      tree = ET.parse(HG_xml)
    except: 
      logger.error("Error reading XML from '%s'! Aborting ...", HG_xml)
      sys.exit(2) 
    logger.info("XML file '%s' successfully read", HG_xml)

    self._xml_remove_namespace(tree)
    return(tree)
  
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
  
  def _xml_remove_namespace(self, tree):
    root = tree.getroot()
    
    namespaces = re.findall(r"{.*}", root.tag)
    
    try:
      namespace = namespaces[0]
      logger.debug(namespace)
    except:
      return()  # nothing to be done

    nsl = len(namespace)
    for elem in root.getiterator():
        if elem.tag.startswith(namespace):
            elem.tag = elem.tag[nsl:] 
      
  def _debug_print(self):
    #ET.dump(self._xml)
    root = self._xml.getroot()
    logger.debug("XML Root is: '%s'", root)
    for n1 in root:
      logger.debug("\t%s - %s", n1.tag, n1.text)
      for n2 in n1:
        logger.debug("\t\t%s - %s", n2.tag, n2.text)
        for n3 in n2:
          logger.debug("\t\t\t%s - %s", n3.tag, n3.text)
          for n4 in n3:
            logger.debug("\t\t\t\t%s - %s", n4.tag, n4.text)
            for n5 in n4:
              logger.debug("\t\t\t\t\t%s - %s", n5.tag, n5.text)   
              
              
  def _prepare(self):
    if self._params.HG_db:
      self._extract_HG_db()
  
  def _extract_HG_db(self):
    if not path.exists(self._params.HG_db):
      logger.warning("Hydrogen DB '%s' does not exists. Aborting ...", self._params.HG_db )
      logger.info("Trying on unpacked kit (Hydrogen XML)...")
      return()
    
    # if kit name is not set use base name of HG db file
    if not self._params.drumkit_name: 
      self._params.drumkit_name = path.basename(self._params.HG_db).replace(".h2drumkit", "")
          
    self._params.src_dir = self._params.tmp_dir + "/" + self._params.drumkit_name
    self._params.HG_xml  = self._params.src_dir + "/drumkit.xml"

    """ unpack hydrogen file """
    logger.info("Unpacking Hydrogen data file '%s' to '%s' ...", self._params.HG_db,
                self._params.tmp_dir)
       
    try:   # open archive, could be gzipped tar or plain tar
      logger.debug("Assume it it is gzip'ed tar archive ...")
      tar = tarfile.open(self._params.HG_db, "r:gz")
    except:
      logger.debug("Failed: Assume it is old style tar'ed archive ...")
      try:
        tar = tarfile.open(self._params.HG_db, "r")
      except:
        logger.error("Failed to open Hydrogen data file. Aborting ...")
        exit(1)
        
    try:   # extract
      logger.debug("Extracting ...")
      tar.extractall(self._params.tmp_dir)
      tar.close()
    except:
      logger.error("Failed to unpack Hydrogen data file. Aborting ...")
      exit(1)
      
    # check if name from Hydrogen DB file matches unpacked directory name  
    if not dir_exists(self._params.src_dir):
      logger.error("Name of drum kit '%s' seems to be incorrect! " +
                   "Please check the unpacked data in directory '%s'. Aborting ..." ,
                   self._params.drumkit_name, self._params.tmp_dir)
      exit(1)
    self._params.clean_rm.append(self._params.src_dir)
    
  
    
  
  