'''
Created on Jun 14, 2020

@author: peter
'''

import abc
import logging
logger = logging.getLogger(__name__)

class Exporter_Base(metaclass=abc.ABCMeta):
    '''
    base class for exporter
    '''

    def __init__(self, drumkit, params):
        logger.debug("Running in debug mode ...")
        self._drumkit = drumkit
        self._params  = params


    @abc.abstractmethod
    def export(self):
        """ export the drum kit DB to a specific output format """
