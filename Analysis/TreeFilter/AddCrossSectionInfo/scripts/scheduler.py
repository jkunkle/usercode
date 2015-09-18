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

jobs_mc = [
        #('job_summer12_DYJetsToLL', 'DYJetsToLL'),
        ('job_summer12_Zg', 'Zg'),
        ('job_summer12_Wg', 'Wg'),
        ('job_summer12_Wjets', 'Wjets'),
        ('job_summer12_ttjets_1l', 'ttjets_1l'),
        ('job_summer12_ttjets_2l', 'ttjets_2l'),
]

base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPGG_2015_09_14'
output_tag = 'WithXS'
nFilesPerJob = 1
nproc=6
treename='ggNtuplizer/EventTree'
module = 'Conf.py'

xsFile = '/afs/cern.ch/user/j/jkunkle/usercode/Plotting/cross_sections/wgamgam.py'

command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir %(base)s/%(job)s%(tag)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s --enableRemoveFilter'

if options.resubmit :
    command_base += ' --resubmit'

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(job)s --filteredDS /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'

if options.run :
    for job, key in jobs_mc :
        module_str = '{ \'xsFile\' : \'%s\' , \'xsKey\' : \'%s\' }' %(  xsFile, key )
    
        command = command_base %{ 'base': base , 'job' : job, 'module' : module, 'moduleArgs' : module_str, 'tag' : output_tag, 'nproc' : nproc, 'exe' : 'RunAnalysis%s' %(job), 'nFilesPerJob': nFilesPerJob, 'treename' : treename}

        print command
        os.system(command)


if options.check :
    for config in top_configs :
    
        for base, job in jobs_data :
    
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'treename' : treename}
            print command
            os.system(command)
        
        for base, job in jobs_mc :
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'treename' : treename}
            print command
            os.system(command)



