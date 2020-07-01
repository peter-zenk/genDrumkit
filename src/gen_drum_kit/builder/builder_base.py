'''
Created on Jun 17, 2020

@author: peter
'''

import abc


import logging
logger = logging.getLogger(__name__)

class Builder_Base(metaclass=abc.ABCMeta):
  '''
    classdocs
  '''

  def __init__(self, params):
    self._params = params

  @abc.abstractmethod   
  def buildDrumkit(self): pass  
  
  def _create_map_template(self, instr_list):
    """
    create and write a map template
    """
    map_list = []
    map_list.append("# Version 1.0")
    map_list.append("# --------------------------------------------------------")    
    map_list.append("# Map File for: '"+self._params.drumkit_name+"'")
    map_list.append("# --------------------------------------------------------")    
    map_list.append("# Format:")
    map_list.append("# <Instr>, <Channel, [<Midi>], [<Group>], [<Res1>], [<Res2>] ")   
    map_list.append("#    <Instr>   : Name of instrument. Mandatory")    
    map_list.append("#    <Channel> : Name of output channel. Mandatory")    
    map_list.append("#    <Midi>    : Midi note for instrument. Optional")    
    map_list.append("#    <Group>   : instrument belongs to a common group. e.g. HiHat. Optional")    
    map_list.append("#    <Res1>    : for future usage")    
    map_list.append("#    <Res2>    : for future usage")    
    map_list.append("# Note: Either all or no midi notes should be specified.")
    map_list.append("#    ")    
    map_list.append("# Examples:")    
    map_list.append("#    Snare1, Snare, 38 ,     ,")
    map_list.append("#    Snare2, Snare,  ,     ,")
    map_list.append("#    HiHat Open, HiHat, 45, Group1")
    map_list.append("#    HiHat Closed, HiHat, 46, Group1")
    map_list.append("#    Kick1 , Kick, 43 , ,")
    map_list.append("#    ")    
    map_list.append("# --------------------------------------------------------")    
    for name in instr_list:
      map_list.append("{:20}, {:20},     ,     ,     ,      ,".format(name, name))
    map_list.append("# --------------------------------------------------------")    
    map_list.append("# End of map")
    map_list.append("# --------------------------------------------------------\n")    
    
    tmpl_fn = self._params.drumkit_name + ".tmpl.csv"
    
    with open(tmpl_fn, mode='wt', encoding='utf-8') as f:
      f.write('\n'.join(map_list))
    logger.info("Map template file '%s' written.", tmpl_fn)