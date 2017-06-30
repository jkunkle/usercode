import os
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--run', dest='run', default=False, action='store_true', help='Run filtering' )
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local', dest='local', default=False, action='store_true', help='Run locally, not on batch' )
options = p.parse_args()

if not options.run and not options.check :
    options.run = True

out_prefix = '/data/users/jkunkle/RecoPhoton/'
base = r'/data/users/jkunkle/RecoPhoton/Photon_2015_11_23'

qcd_jobs = [
        (base, 'QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8'               ),
        (base, 'QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8'             ),
        (base, 'QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8'               ),
        (base, 'QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8'             ),
        (base, 'QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8'               ),
        (base, 'QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8'               ),
        (base, 'QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8'              ),
]

dip_jobs = [
        (base, 'DiPhotonJetsBox_M40_80-Sherpa'),
        (base, 'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa' ),
]


top_configs = [ 
                { 
                  'jobs'        : [(base, 'SinglePhoton'),(base, 'GJet_Pt-15ToInf_TuneCUETP8M1_13TeV-pythia8')] + dip_jobs,
                  'module'      : 'ConfTAndP.py',
                  'args'        : {'functions' : 'MakeGJNtuple' },
                  'output_name' : 'FakePhotonProbeWithTrig_2015_11_27',
                  'tag'         : 'gj',
                },
                #{ 
                #  'jobs'        : qcd_jobs,
                #  'module'      : 'ConfTAndP.py',
                #  'args'        : {'functions' : 'MakeQCDNtuple' },
                #  'output_name' : 'FakePhotonProbe_2015_11_27',
                #  'tag'         : 'qcd',
                #},
                #{ 
                #  'jobs'        : [ (base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8')],
                #  'module'      : 'ConfTAndP.py',
                #  'args'        : {'functions' : 'MakeZmumuNtuple' },
                #  'output_name' : 'FakePhotonProbe_2015_11_27',
                #  'tag'         : 'dy',
                #},
                #{ 
                #  'jobs'        : [ (base, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8')],
                #  'module'      : 'ConfTAndP.py',
                #  'args'        : {'functions' : 'MakeWmunuNtuple' },
                #  'output_name' : 'FakePhotonProbe_2015_11_27',
                #  'tag'         : 'wlnu',
                #},
]


if options.local :
    #--------------
    # not batch
    #--------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir %(out_prefix)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s --disableOutputTree --enableKeepFilter  --moduleArgs "%(moduleArgs)s" '
else :
    #--------------
    # for batch
    #--------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir %(out_prefix)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s  --nFilesPerJob %(nFilesPerJob)d --condor --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s  --disableOutputTree --enableKeepFilter  --moduleArgs "%(moduleArgs)s" '


if options.resubmit :
    command_base += ' --resubmit'

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(job)s --filteredDS %(out_prefix)s/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt tupel/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'


nFilesPerJob = 1
nproc=6
treename='tupel/EventTree'

if options.run :
    for config in top_configs :

        module_arg = config['args']

        module_str = '{ '
        for key, val in module_arg.iteritems() :
            module_str += '\'%s\' : \'%s\',' %( key, val)
        module_str += '}'

        for base, job in config['jobs']:

            command = command_base %{ 'base': base , 'job' : job, 'output' : config['output_name'], 'module' : config['module'],  'tag' : config['tag'], 'nproc' : nproc, 'exe' : 'RunAnalysis%s%s' %(config['tag'], job), 'nFilesPerJob': nFilesPerJob, 'treename' : treename, 'out_prefix' : out_prefix, 'moduleArgs' : module_str}

            print command
            os.system(command)



if options.check :
    for config in top_configs :
    
        for base, job in jobs:
    
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'treename' : treename, 'out_prefix' : out_prefix}
            print command
            os.system(command)
        
        for base, job in jobs_mc :
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'treename' : treename, 'out_prefix' : out_prefix}
            print command
            os.system(command)



