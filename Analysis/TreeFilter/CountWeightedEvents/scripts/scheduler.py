import scheduler_base
from scheduler_base import JobConf

from argparse import ArgumentParser
from argparse import Namespace


parser = ArgumentParser()

options = parser.parse_args()

print options
print isinstance( options, Namespace)

base = '/data/users/jkunkle/Resonances/'

jobs = [
        JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' ),
        JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ),
        JobConf(base, 'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                  ),
]


options.run = True
options.nFilesPerJob = 0
options.nproc = 1
options.treename='tupel/EventTree'
options.exename='RunAnalysis'

configs = [ 
    {
        'module' : 'ConfTemplate.py',
        'input'  : 'RecoOutput_2016_12_23',
        'output' : 'TEST',
        'tag'    : 'test',
    },
]

scheduler_base.RunJobs( jobs, configs, options)

