'''
Created on Jun 17, 2020

@author: peter
'''


from gen_drum_kit.drum_kit.DrumKit     import DrumKit
from gen_drum_kit.drum_kit.Instrument  import Instrument
from gen_drum_kit.drum_kit.Channel     import Channel
from gen_drum_kit.drum_kit.ChannelMap  import ChannelMap
from gen_drum_kit.drum_kit.Sample      import Sample
from gen_drum_kit.drum_kit.Audio       import Audio
from gen_drum_kit.drum_kit.Metadata    import Metadata

from gen_drum_kit.builder.builder_base import Builder_Base



import logging
logger = logging.getLogger(__name__)


class Builder_Hydrogen(Builder_Base):

  def __init__(self, params, xml, mapDB):
    super().__init__(params)
    self._xml = xml
    self._map = mapDB
  
  def buildDrumkit(self):
    logger.info("Building drumkit DB from Hydrogen data ...")
    self._prepare()
    
    if self._params.HG_mode == "TPL":
      logger.info("TPL: Creating map template file only")
      self._create_channelmap_template()
      logger.info("Program finished")
      exit(0)
      
    self._drumkit = DrumKit(name=self._params.drumkit_name)
    self._add_metadata()
    self._add_instruments()
    self._add_channels()
    return(self._drumkit)
  
  
  """ private functions """
  
  def _prepare(self):
    self._root =  self._xml.getroot()
    self._params.drumkit_name = self._root.findtext('name').strip()
    self._extract_map_info()
        
  def _add_metadata(self):
    author     =  self._root.findtext('author', "")
    email      =  self._root.findtext('email', "")
    name       =  self._root.findtext('name', "").strip()
    info       =  self._root.findtext('info', "")
    licens     =  self._root.findtext('license', "")
    image      =  self._root.findtext('image', "")
   
    self._drumkit.metadata = Metadata(title=name, image=image, notes=name, description= info, 
                                   license=licens, author=author, email=email)
 
  def _add_instruments(self):
    for xml_instr in self._root.find('instrumentList'):
      ii   = self._xml_extract_instr_info(xml_instr)
      name = ii['name']
      
      """ overwrite group info if exists (from map file)"""
      if name in self._groups.keys()  and self._groups[name]:  
        ii["group"] = self._groups[name]
        
      """ construct midi from id if it does not exist """
      if not ii['midi_note']:
        ii['midi_note'] = str( int(ii['id']) + self._params.HG_midi_start)
      
      logger.debug(ii)
      
      """ create instrument """
      instrument = Instrument(name=name, 
                              midi_note=ii['midi_note'], 
                              xml=name + "/" + name + ".xml",
                              metadata=self._drumkit.metadata, 
                              group=ii['group'])
      
      """ adding channel maps """
      self._add_channel_maps(name=name, instrument=instrument)
              
      """ adding samples """
      self._add_samples(ii=ii, instrument=instrument)
            
      """ add instrument to list """
      self._drumkit.instruments.append(instrument)
      
  def _add_channel_maps(self, name, instrument):
    if name in self._channel_map.keys():
      outch = self._channel_map[name]
    else:
      outch = name
  
    
    if self._params.HG_stereo: # 2 channels, stereo
      instrument.channelmaps.append(ChannelMap(inp=(name + "_R"), out = (outch + "_R"), main="true"))
      instrument.channelmaps.append(ChannelMap(inp=(name + "_L"), out = (outch + "_L"), main="true"))
    else:   # 1 channel mono
      instrument.channelmaps.append(ChannelMap(inp=(name ), out = (outch), main="true"))
         
  def _add_channels(self):
    channels = self._drumkit.channels
    
  
    for channel in self._channel_list:
      if self._params.HG_stereo: # 2 channels stereo
        channels.append(Channel(name=channel + "_R"))
        channels.append(Channel(name=channel + "_L")) 
      else:   # 1 channel, mono
        channels.append(Channel(name=channel))
           
  def _add_samples(self, ii, instrument):
    
    """
     several ways for definition of samples
      1. layer(s) inside instrument.instrumentComponent (1 or more samples)
      2. layer(s) inside instrument  (1 or more samples)
      3. filename inside instrumen  (1 sample)
    """

    
    if ii['instrumentComponent']:   # case 1
      layers = ii['instrumentComponent'].findall('layer')
      si = self._xml_extract_sample_info(layers)
      logger.debug(si)
      self._construct_samples(ii=ii, si=si, instrument=instrument)
     
    elif  ii['layers']:
      si = self._xml_extract_sample_info(ii['layers'])
      logger.debug(si)
      self._construct_samples(ii=ii, si=si, instrument=instrument)
      
    else:
      sample = Sample(name=ii['name'], power="1.0" )
      self._add_audios(sample=sample, name=ii['name'], fn=ii['filename'])   
      instrument.samples.append(sample)
  
  def _construct_samples(self, ii, si, instrument):
      no = 0
      for smpl in si:
        no = no + 1
        sample = Sample(name=ii['name'] + "-" + str(no), power=smpl['max'] )
  
        self._add_audios(sample=sample, name=ii['name'], fn=smpl['filename'])      
        instrument.samples.append(sample)
  
  def _add_audios(self, sample, name, fn ):
    if self._params.HG_stereo:   # 2 channels per instrument , stereo
      sample.audios.append(Audio(channel=(name+"_R"), src_fn=fn,
                                 file_name="samples/" + fn, filechannel=1))
      sample.audios.append(Audio(channel=(name+"_L"), src_fn=fn,
                                 file_name="samples/" + fn, filechannel=2))

    else:  # 1 channel per instrument - mono
      sample.audios.append(Audio(channel=(name), src_fn=fn,
                                 file_name="samples/" + fn, filechannel=1))            
  def _extract_map_info(self):
    self._channel_map  = {}
    self._channel_list = []
    self._groups       = {}
    
    logger.warning("midi info from map file not used yet")
     
    if len(self._map) != 0: # map exists      
      for item in self._map:
        """ <instr>, <channel>, <midi>, <group>"""
        instr    = item.pop(0).strip()       
        channel = item.pop(0).strip()       
        midi    = item.pop(0).strip()   
  
        group   = item.pop(0).strip()        

        self._channel_map[instr] = channel  # instr - channel      
        self._groups[instr]      = group    # instr - groups
        self._channel_list.append(channel) 
    else:  # defaults
      for xml_instr in self._root.find('instrumentList'):
        name = xml_instr.findtext('name').strip()
        self._channel_list.append(name)
        self._channel_map[name] = name   # instr - channel
       
    self._channel_list = list(dict.fromkeys(self._channel_list)) # remove duplicates

    no_of_ch =   len(self._channel_list) * 2  if self._params.HG_stereo else len(self._channel_list)
    if (no_of_ch > self._params.channel_limit):
      logger.warning("Number of total channels (%s) is greater than limit! DrumGizmo might only support %s channels",
                   no_of_ch, self._params.channel_limit)

    logger.debug(self._channel_list)
    logger.debug(self._channel_map)
    logger.debug(self._groups)  
    

  def _xml_extract_instr_info(self, xml_instr):
    info = {}
    
    logger.debug(xml_instr)
    for child in xml_instr:
      logger.debug("\t\t%s - %s", child.tag, child.text)
   
    info['id']                  = xml_instr.findtext('id', "")
    name                        = xml_instr.findtext('name', "")
    info['midi_note']           = xml_instr.findtext('midiOutNote', "")
    info['isHihat']             = xml_instr.findtext('isHihat', "")
    info['muteGroup']           = xml_instr.findtext('muteGroup', "")
    info['instrumentComponent'] = xml_instr.find('instrumentComponent') 
    info['layers']              = xml_instr.findall('layer') 
    info['filename']            = xml_instr.findtext('filename', "sample-does-not-exist") 
    
    info['name'] = name.replace("\"", "").replace("/", "-").replace(":","-")

    # remove leading and trailing spaces if element is a string
    for k in info.keys():
      if type(info[k]) == str:
        info[k] = info[k].strip()    
    
    # handle group
    if   info['muteGroup'] and (info['muteGroup'] != '-1' ):
      info['group'] = "group_" + info['muteGroup']
    else:
      info['group'] = ""
  
    return(info)
  
  def _xml_extract_sample_info(self, layers):
    info = []
    
    for xml_smpl in layers:
      smpl = {}
      for child in xml_smpl:
        logger.debug("\t\t%s - %s", child.tag, child.text)
      smpl['min']        = xml_smpl.findtext('min', "")
      smpl['max']        = xml_smpl.findtext('max', "")
      smpl['filename']   = xml_smpl.findtext('filename', "")
      info.append(smpl)
    info = sorted(info, key=lambda k: k['max']) ## sort samples according to max
    return(info)


  def _create_channelmap_template(self):
  
    instr_list = []
    for xml_instr in self._root.find('instrumentList'):
      name = xml_instr.findtext("name").strip()
      instr_list.append(name)
   
    self._create_map_template(instr_list)
    
    