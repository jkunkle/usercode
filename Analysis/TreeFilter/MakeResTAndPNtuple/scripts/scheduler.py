import os
from argparse import ArgumentParser

import scheduler_base
from scheduler_base import JobConf

p = ArgumentParser()
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--clean', dest='clean', default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--batch', dest='batch', default=False, action='store_true', help='Run on batch' )
options = p.parse_args()

if not options.check :
    options.run = True
else :
    options.run = False

options.local = ( not options.batch )

base = '/data/users/jkunkle/Resonances/'

jobs = [
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M200_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M300_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M400_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M500_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M600_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M700_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M800_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M1000_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M1200_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M2000_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M3000_width0p01'                         ),
        JobConf(base, 'MadGraphChargedResonance_WGToLNu_M4000_width0p01'                         ),
]

options.nFilesPerJob = 2
options.nproc = 6
options.treename='tupel/EventTree'
options.exename='RunAnalysis'
options.copyInputFiles=False
options.enableKeepFilter=True
options.disableOutputTree=True

#input_base = 'RecoOutput_2017_01_16'
input_base = 'RecoOutputSig_2017_01_26'

configs = [ 

    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'makeMCMuon' },
        'input'  : input_base,
        'output' : base+'MuonEff_2016_01_30',
        'tag'    : 'mumc',
    },
    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'makeMCElectron' },
        'input'  : input_base,
        'output' : base+'ElectronEff_2016_01_30',
        'tag'    : 'elmc',
    },
    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'makeMCPhoton', 'useWMu' : True },
        'input'  : input_base,
        'output' : base+'PhotonEffMuCh_2016_01_30',
        'tag'    : 'phmumc',
    },
    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'makeMCPhoton', 'useWEl' : True },
        'input'  : input_base,
        'output' : base+'PhotonEffElCh_2016_01_30',
        'tag'    : 'phelmc',
    },

]

scheduler_base.RunJobs( jobs, configs, options)

