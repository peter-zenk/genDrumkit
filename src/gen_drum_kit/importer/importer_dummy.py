'''
Created on Jun 14, 2020

@author: peter
'''

from gen_drum_kit.importer.importer_base   import ImporterBase
from gen_drum_kit.builder.builder_dummy    import Builder_Dummy


import logging
logger = logging.getLogger(__name__)


class ImporterDummy(ImporterBase):

  def __init__(self, params):
    super().__init__(params)
    logger.debug("Running in debug mode ...")
    logger.debug("ImporterBase '%s' created.", __name__)

  def importData(self):
    pass
    
  def buildDrumkitDB(self):
    logger.info("Creating default drum kit. No external input loaded!")

    Builder = Builder_Dummy(self._params)
    drumkit = Builder.buildDrumkit()
    return(drumkit)
