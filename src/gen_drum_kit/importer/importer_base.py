'''
Created on Jun 14, 2020

@author: peter
'''

import abc
import csv
import logging

from gen_drum_kit.util   import decomment


logger = logging.getLogger(__name__)



class ImporterBase(metaclass=abc.ABCMeta):
    '''
    Abstract base class for converter
    '''
    def __init__(self, params):
        logger.debug("Running in debug mode ...")
        self._params      = params
        self._channel_map = None # assigned later

    @abc.abstractmethod
    def importData(self):
        """ import the drum kit data from the related format """

    def buildDrumkitDB(self):
        """ build the drum kit DB from the imported data """
        Builder = self._createBuilder()
        drumkit = Builder.buildDrumkit()
        return(drumkit)


    # private functions ------------------

    @abc.abstractmethod
    def _createBuilder(self):
        """ create and return the builder """

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


        logger.debug(self._channel_map)
