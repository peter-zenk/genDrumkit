'''
Created on Jun 14, 2020

@author: peter
'''

from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
from typing import List
from argparse import ArgumentParser



import logging
logger = logging.getLogger(__name__)


class _ExtEnum(Enum):
  @classmethod
  def list(cls):
    return list(map(lambda c: c.value, cls))

class ImpType(_ExtEnum):
  DUMMY = "DUMMY"
  HG    = "HG"  # Hydrogen
  
class ExpType(_ExtEnum):
  DG    = "DG"  # DrumGizmo
  
class HgMode(_ExtEnum):
  KIT   = "KIT"
  TPL   = "TPL"
  
class SampleLevel(_ExtEnum):
  normalized = "normalized"
  scaled     = "scaled"

class SampleSrcPolicy(_ExtEnum):  
  USE   = "USE"  #  append to sample_src_dir as it is
  TRG   = "TRG"  # same structure as exporter uses for target
  

@dataclass
class Parameter(object):
    '''
    - Global parameters for import and export
    '''
  
    out_dir:            str  = "."              # directory where kit is created
    drumkit_name:       str  = "drumkit"        # name of drum kit
    src_dir:            str  = "path_to_samples"
    samples_level:      str  = "normalized"     # samples are normalized or scaled
    samples_src_pol:    open = "USE"            # policy for input sample file name

    channel_map:        open = None             # CSV file with mapping from instrument to channel
    
    """ Importers """
    impFmt:             open = None             # Type of importer
    
    HG_xml:             str  = "drumkit.xml"    # Hydrogen drumkit XML file
    HG_db:              str  = "drumkit.h2drumkit"               # Hydrogen data base file 
    HG_midi_start:      str  = 36               # Hydrogen midi start for default mapping
    HG_mode:            str  = "KIT"            # run mode for Hydrogen processing
    HG_stereo:          int  = False
    
    """ Exporters """
    expFmt:             open  = None            # Type of exporter
    
    """ Misc """
    tmp_dir:            str   = ".genDrumkit"   # where temp data is created
    channel_limit:      int   = 16 # 16 outputs currently supported by DrumGizmo
    
    # list of files/dirs to remove, for clean-up at end of program
    clean_rm:            List[str]  = field(default_factory=list)
     

    def __post_init__(self):
      self._opts = self._process_cmd_line()
      self._config_logging(self._opts.loglevel)
      self._set_params()
      self._run_checks()
      logger.debug(self)
      
      
    def _process_cmd_line(self):
      
      parser = ArgumentParser(description="Create a drum kit")
      
      group_gn = parser.add_argument_group('General', 'Common options')

      group_gn.add_argument("--kit_name", "-kn", type=str, dest="drumkit_name", 
                          default="",
                          help="Drum kit name: Default: ''")
      
      group_gn.add_argument("--output_dir", "-od", type=str, dest="out_dir", 
                          default=".",
                          help="Directory path where output is generated. Default: '.'")

      group_gn.add_argument("--impFmt", "-imp",  dest="impFmt",
                          choices=ImpType.list(),   default="HG",                      
                          help="Drum kit import format. Default: HG (Hydrogen)")
      
      group_gn.add_argument("--expFmt", "-exp", dest="expFmt",
                          default="DG",
                          choices=ExpType.list(),
                          help="Drum kit export format. Default: DG (DrumGizmo)")

      group_gn.add_argument("--channel_map", "-cm", type=str, dest="channel_map",
                          default="map.csv",
                          help="Channel/Instrument map file. Default 'map.csv'")
      
    
      
      group_hg = parser.add_argument_group('Hydrogen', 'Options for Hydrogen importer')

      group_hg.add_argument("--hg_db", "-hgd", type=str, dest="HG_db",
                          default="",
                          help="Hydrogen DB file. (*.h2drumkit). Default ''")
      
      group_hg.add_argument("--hg_xml", "-hgx", type=str, dest="HG_xml",
                          default="",
                          help="Hydrogen XML file. Ignored, if Hydrogen DB is specified. Default ''")
      
      group_hg.add_argument("--hg_midi_start", "-hgmi", type=int, dest="HG_midi_start",
                          default=36,
                          help="Hydrogen midi start for default mapping. Default: 36")
      
      group_hg.add_argument("--hg_stereo", "-hgs", action="store_true", dest="HG_stereo",
                          default=False, 
                          help="Connect channels and instruemnts via stereo. Default: mono")
      
      group_hg.add_argument("--hg_mode", "-hgmo", type=str, dest="HG_mode",
                          choices=HgMode.list(),  default="RUN",
                          help="Hydrogen execution mode. KIT: create drumkit, LST: create map list template.\
                          Default 'KIT'")


      group_sm = parser.add_argument_group('Audio samples', 'Options for audio sample handling')
          
      group_sm.add_argument("--src_dir", "-sd", type=str, dest="src_dir", 
                          default="sample_src_dir",
                          help="Directory path to sample sources (top level). Default: 'sample_src_dir'")
      
      group_sm.add_argument("--sample_src_pol", "-ssp", type=str, dest="samples_src_pol", 
                          choices=SampleSrcPolicy.list(),  default="USE",
                          help="Policy to build src sample path. TRG: structure like target, USE: use name as is. Default: 'USE'")
      
      group_sm.add_argument("--sample_level", "-sl", type=str, dest="samples_level", 
                          choices=SampleLevel.list(),  default="normalized",
                          help="Samples are scaled or normalized. Default: 'normalized'")
      
 
      group_rp = parser.add_argument_group('Report', 'Reporting and debug options')          

      group_rp.add_argument("--log_level", "-ll", dest="loglevel", default=logging.INFO,
                          choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"), 
                          help="Set logging level. Default: INFO")
     
      return(parser.parse_args())
      
    def _config_logging(self, loglevel="INFO"):
      logging.basicConfig(
      # format="%(asctime)s [%(levelname)s] %(message)s",
        format="genKit (%(filename)s) - [%(levelname)s]:   %(message)s",
        handlers=[
            logging.FileHandler("genDrumkit.log"),  
            logging.StreamHandler()
        ],
        level=loglevel,
      )

    def _set_params(self):
      """ map self._opts  to self """
      for arg in vars(self._opts):
        setattr(self, arg, getattr(self._opts, arg))
        
    def _run_checks(self):
      if not Path(self.out_dir).is_dir():
        logger.error("Output directory '%s' not found. Aborting ...", self.out_dir)
        exit(1)
      if self.impFmt == "HG" and not self.HG_db and not self.HG_xml:
        logger.error("Neither Hydrogen DB file nor Hydrogen XML file specified. Aborting ...")
        exit(1)
  