'''
Created on Jun 15, 2020

@author: peter
'''

from dataclasses import dataclass


@dataclass
class Audio():
  """ DO NOT CHANGE ORDER """
  channel:     str = "instr_ch"
  file_name:   str = "path/to/kit/sample"
  filechannel: int = 1
  src_fn:      str = None


  def __post_init__(self):
    if not self.src_fn:
      self.src_fn = self.file_name

        