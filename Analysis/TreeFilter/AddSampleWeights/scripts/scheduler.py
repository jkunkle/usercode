import os
from argparse import ArgumentParser

import analysis_utils
import scheduler_base
from scheduler_base import JobConf

p = ArgumentParser()
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--clean', dest='clean', default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--batch', dest='batch', default=False, action='store_true', help='Run on batch' )
p.add_argument( '--test', dest='test', default=False, action='store_true', help='Run a test job' )
p.add_argument( '--xsFile', dest='xsFile', default=None, help='path to cross section file' )
p.add_argument( '--lumi', dest='lumi', type=float, default=1., help='integrated luminosity' )
options = p.parse_args()

if not options.check :
    options.run = True
else :
    options.run = False

options.local = ( not options.batch )

base = '/data/users/jkunkle/Resonances/'

weightMap = analysis_utils.read_xsfile( options.xsFile, options.lumi, print_values=False )
print weightMap

jobs = [
        #JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'         , suffix = 'XSWeight'  , weight=weightMap['WGToLNuG-madgraphMLM']['scale']                   ),
        #JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , suffix = 'XSWeight'  , weight=weightMap['WGToLNuG_PtG-130-madgraphMLM']['scale']),
        #JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , suffix = 'XSWeight'  , weight=weightMap['WGToLNuG_PtG-500-madgraphMLM']['scale']),
        JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         , suffix = 'XSWeight' , weight=weightMap['WGToLNuG-amcatnloFXFX']['scale']),
        JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' , suffix = 'XSWeight' , weight=weightMap['WGToLNuG_PtG-130-amcatnloFXFX']['scale']),
        JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' , suffix = 'XSWeight' , weight=weightMap['WGToLNuG_PtG-500-amcatnloFXFX']['scale']),
]

options.nFilesPerJob = 1

options.nproc = 4
options.treename='tupel/EventTree'
options.exename='RunAnalysis'
options.copyInputFiles=False
options.enableKeepFilter=False
options.enableRemoveFilter=False


module = 'Conf.py'
input_dir = 'LepGamma_mug_2017_04_12'
tag = 'mug'

configs = [ ]

for j in jobs :

    config = {'module' : module,
              'input' : input_dir,
              'output' : base+input_dir,
              'tag' : tag,
              'args' : {'weight': j.weight }
             }

    scheduler_base.RunJobs( j,config, options)

