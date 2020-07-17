'''
Created on Jun 14, 2020

@author: peter
'''

import sys
import logging
from shutil   import rmtree
from platform import system

from gen_drum_kit.parameter import Parameter
from gen_drum_kit.factory   import ImporterFactory, ExporterFactory


logger = logging.getLogger(__name__)


class Main():
    """ The top level class handling the program flow """

    def __init__(self):
        self._impFactory = ImporterFactory()
        self._expFactory = ExporterFactory()
        self._params = None # defined later

    @staticmethod
    def _check_environment():

        if sys.hexversion < 50856688:
            #check python version
            print("INFO: Your version of python is " + str(sys.version_info))
            sys.exit("ERROR: You must use at least python 3.8.2. Aborting ...")

        if system() != "Linux":
            # only Linux will be supported
            print("INFO: You are running on :", system())
            sys.exit("ERROR: You must run on a 'Linux' system!")

    def _init_program(self):
        # initialize the program context
        self._check_environment()
        self._params = Parameter()


    def _cleanup(self):
        # cleaning up on exit
        logger.info("Cleaning up ...")
        for item in self._params.clean_rm:
            logger.debug("Removing '%s' ...", item)
            try:
                rmtree(item)
            except:
                logger.error("Could not remove '%s'!", item)

    def run(self):
        """ this is the main run() task to be called by the client script """

        # command line, default settings, initial sanity checks
        self._init_program()
        logger.debug("Running in debug mode")

        # create the importer and import data
        Imp = self._impFactory.create(self._params)
        Imp.importData()

        # build the drum kit object based on the data read by the importer
        Drumkit = Imp.buildDrumkitDB()
        logger.debug(Drumkit)

        # create the exporter and export the output drum kit with the data
        # from the drum kit object
        Exp = self._expFactory.create(Drumkit, self._params)
        Exp.export()

        self._cleanup()

        logger.info("Finished program ...")
