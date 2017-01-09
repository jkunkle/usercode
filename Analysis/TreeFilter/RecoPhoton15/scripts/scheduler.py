import os
from argparse import ArgumentParser

import scheduler_base
from scheduler_base import JobConf

p = ArgumentParser()
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local', dest='local', default=False, action='store_true', help='Run locally' )
p.add_argument( '--test', dest='test', default=False, action='store_true', help='Run a local test job' )
options = p.parse_args()

if not options.check :
    options.run = True
else :
    options.run = False

options.batch = ( not options.local )


#base = '/data/users/jkunkle/Baobabs/'
base = '/store/user/jkunkle/'
base_signal = '/data/users/jkunkle/Samples/SignalMoriond/'
version = 'Resonances_v4'

jobs = [
        JobConf(base, 'SingleMuon', version=version, isData=True ),
        JobConf(base, 'SingleElectron', version=version, isData=True),
        #JobConf(base, 'SinglePhoton', version=version, isData=True),
        JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        JobConf(base, 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        JobConf(base, 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        JobConf(base, 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        JobConf(base_signal, 'MadGraphChargedResonance_WGToLNu_M200_width0p01'  ), 
        JobConf(base_signal, 'MadGraphChargedResonance_WGToLNu_M300_width0p01'  ), 
        JobConf(base_signal, 'MadGraphChargedResonance_WGToLNu_M400_width0p01'  ), 
        JobConf(base_signal, 'MadGraphChargedResonance_WGToLNu_M500_width0p01'  ), 
        JobConf(base_signal, 'MadGraphChargedResonance_WGToLNu_M600_width0p01'  ), 
        JobConf(base_signal, 'MadGraphChargedResonance_WGToLNu_M700_width0p01'  ), 
        JobConf(base_signal, 'MadGraphChargedResonance_WGToLNu_M800_width0p01'  ), 
        JobConf(base_signal, 'MadGraphChargedResonance_WGToLNu_M1000_width0p01'  ),
        JobConf(base_signal, 'MadGraphChargedResonance_WGToLNu_M1200_width0p01'  ),
]

jobs_nlo = [
        JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version),
        JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        , version=version),
        JobConf(base, 'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8'        , version=version),
        JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' , version=version),
        JobConf(base, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         , version=version),
        JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'      , version=version),
        JobConf(base, 'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                 , version=version),
]

options.filekey = 'ntuple'
options.nFilesPerJob = 1
options.nproc = 6
options.treename='tupel/EventTree'
options.exename='RunAnalysis'
options.copyInputFiles=False
options.enableKeepFilter=True
options.enableRemoveFilter=True

module = 'ConfPhotonReco.py'
#module = 'ConfTruthPhotonReco.py'

out_base = '/data/users/jkunkle/Resonances/'
configs = [ 
    {
        'module' : module,
        'args'   : { },
        'input'  : '',
        'output' : out_base+'RecoOutput_2017_01_09',
        'tag'    : 'reco',
    },
]

configs_nlo = [
    {
        'module' : module,
        'args'   : { 'ApplyNLOWeight' : 'true', 'doFHPFS' : 'true'  },
        'input'  : '',
        'output' : out_base+'RecoOutput_2017_01_09',
        'tag'    : 'nloreco',
    },
]

scheduler_base.RunJobs( jobs, configs, options)
scheduler_base.RunJobs( jobs_nlo, configs_nlo, options)

