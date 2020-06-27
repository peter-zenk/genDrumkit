'''
Created on Jun 15, 2020

@author: peter
'''
from dataclasses import dataclass


@dataclass
class ChannelMap(object):
  
  inp:     str = "Instr_In"
  out:     str = "Instr_Out"
  main:    str = "true"
  
  def __post_init__(self): pass