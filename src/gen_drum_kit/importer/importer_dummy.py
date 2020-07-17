'''
Created on Jun 14, 2020

@author: peter
'''
import logging

from gen_drum_kit.importer.importer_base   import ImporterBase
from gen_drum_kit.builder.builder_dummy    import Builder_Dummy


logger = logging.getLogger(__name__)


class ImporterDummy(ImporterBase):
    """ importer that does nothing """

    def __init__(self, params):
        super().__init__(params)
        logger.debug("Running in debug mode ...")
        logger.debug("ImporterBase '%s' created.", __name__)

    def importData(self):
        pass

    def _createBuilder(self):
        # create and return the builders
        logger.info("Creating default drum kit. No external input loaded!")
        return(Builder_Dummy(self._params))
