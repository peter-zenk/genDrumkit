# genDrumkit

Python3 tool to convert virtual drumkits for (home-)recording from one format into another one

## License
GPL-3.0
https://opensource.org/licenses/GPL-3.0

## Wiki
https://github.com/peter-zenk/genDrumkit/wiki

## Usage

```
Usage: genDrumkit [-h] [--kit_name DRUMKIT_NAME] [--output_dir OUT_DIR] [--impFmt {DUMMY,HG}] [--expFmt {DG}] [--channel_map CHANNEL_MAP] [--hg_db HG_DB] [--hg_xml HG_XML]
                  [--hg_midi_start HG_MIDI_START] [--hg_stereo] [--hg_mode {KIT,TPL}] [--src_dir SRC_DIR] [--sample_src_pol {USE,TRG}] [--sample_level {normalized,scaled}]
                  [--log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Create a drum kit

optional arguments:
  -h, --help            show this help message and exit

General:
  Common options

  --kit_name DRUMKIT_NAME, -kn DRUMKIT_NAME
                        Drum kit name: Default: ''
  --output_dir OUT_DIR, -od OUT_DIR
                        Directory path where output is generated. Default: '.'
  --impFmt {DUMMY,HG}, -imp {DUMMY,HG}
                        Drum kit import format. Default: HG (Hydrogen)
  --expFmt {DG}, -exp {DG}
                        Drum kit export format. Default: DG (DrumGizmo)
  --channel_map CHANNEL_MAP, -cm CHANNEL_MAP
                        Channel/Instrument map file. Default 'map.csv'

Hydrogen:
  Options for Hydrogen importer

  --hg_db HG_DB, -hgd HG_DB
                        Hydrogen DB file. (*.h2drumkit). Default ''
  --hg_xml HG_XML, -hgx HG_XML
                        Hydrogen XML file. Ignored, if Hydrogen DB is specified. Default ''
  --hg_midi_start HG_MIDI_START, -hgmi HG_MIDI_START
                        Hydrogen midi start for default mapping. Default: 36
  --hg_stereo, -hgs     Connect channels and instruemnts via stereo. Default: mono
  --hg_mode {KIT,TPL}, -hgmo {KIT,TPL}
                        Hydrogen execution mode. KIT: create drumkit, LST: create map list template. Default 'KIT'

Audio samples:
  Options for audio sample handling

  --src_dir SRC_DIR, -sd SRC_DIR
                        Directory path to sample sources (top level). Default: 'sample_src_dir'
  --sample_src_pol {USE,TRG}, -ssp {USE,TRG}
                        Policy to build src sample path. TRG: structure like target, USE: use name as is. Default: 'USE'
  --sample_level {normalized,scaled}, -sl {normalized,scaled}
                        Samples are scaled or normalized. Default: 'normalized'

Report:
  Reporting and debug options

  --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}, -ll {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set logging level. Default: INFO

```
