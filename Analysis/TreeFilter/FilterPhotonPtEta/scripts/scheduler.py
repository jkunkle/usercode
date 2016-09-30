import os
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--run'     , dest='run'     , default=False, action='store_true', help='Run filtering'              )
p.add_argument( '--check'   , dest='check'   , default=False, action='store_true', help='Run check of completion'    )
p.add_argument( '--clean'   , dest='clean'   , default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local'   , dest='local'   , default=True , action='store_true', help='Run locally'                )
p.add_argument( '--batch'   , dest='batch'   , default=False , action='store_true', help='Run batch'                )
options = p.parse_args()

if not options.run and not options.check :
    options.run = True

#base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDNoEleOlapRM_2015_11_09'
base = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhIDNoElOlapRm_2016_02_05'
#base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09'


jobs = [
        (base, 'job_summer12_DYJetsToLL_s10PhOlap'),
]

if options.batch :
    #--------------------
    # for batch submission
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --outputDir %(base)s/%(job)s_filt_pt_%(ptmin)d-%(ptmax)d_eta_%(etamin).2f-%(etamax).2f --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --moduleArgs "%(moduleArgs)s"  --batch --confFileName %(conf_file)s --nFilesPerJob %(nFilesPerJob)d --exeName %(exename)s_%(job)s '

else :

    #--------------------
    # not batch
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --outputDir %(base)s/%(job)s_filt_pt_%(ptmin)d-%(ptmax)d_eta_%(etamin).2f-%(etamax).2f --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --confFileName %(conf_file)s --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --exeName %(exename)s  '
    
if options.resubmit :
    command_base += ' --resubmit '

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(job)s  --filteredDS %(base)s/%(job)s_filt_pt_%(ptmin)d-%(ptmax)d_eta_%(etamin).2f-%(etamax).2f --treeNameOrig %(treename)s --histNameFilt ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'


#pt_bins = [(15,25),(25,30), (30,35), (35,40),(40,45),(45,50), (50,60), (60,70),(70,1000000) ]
pt_bins = [
           (15,25),
           (25,30), 
           (30,35), 
           (35,40),
           (40,45),
           (45,50), 
           (50,60), 
           (60,70),
           (70,1000000) 
]
eta_bins = [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44), (1.57, 2.1), (2.1, 2.2), (2.2, 2.4), (2.4, 2.5) ]
#eta_bins = [(1.57, 2.1), (2.1, 2.2), (2.2, 2.4), (2.4, 2.5) ]
#eta_bins = [(1.57, 2.1)]

eveto = 'PSV'
#types = [ 'inv', 'nom',]
types = [ 'inv']
nph = ' == 1'

configs = []
for tp in types :
    for ptmin, ptmax in pt_bins :
        for etamin, etamax in eta_bins :
    
            this_config = { 'eveto' : eveto, 'type' : tp, 'nph' : nph, 'ptmin' : ptmin, 'ptmax' : ptmax, 'etamin' : etamin, 'etamax' : etamax }

            configs.append(this_config)

module = 'ConfFilter.py'
nFilesPerJob = 1
nProc = 6
exename='RunAnalysis'
treename='ggNtuplizer/EventTree'

if options.run :
    for config in configs :
        first = True

        for base, job in jobs :
            job_confname = 'conf_%s_pt_%d-%d_eta_%.2f-%.2f.txt' %(job, config['ptmin'],config['ptmax'],config['etamin'],config['etamax'])
            job_exename= '%s_pt_%d-%d_eta_%.2f-%.2f' %(job, config['ptmin'],config['ptmax'],config['etamin'],config['etamax'])

            module_str = '{ '
            module_str += '\'ptmin\' : \'%d\', ' %config['ptmin']
            module_str += '\'ptmax\' : \'%d\', ' %config['ptmax']
            module_str += '\'etamin\' : \'%f\', ' %config['etamin']
            module_str += '\'etamax\' : \'%f\', ' %config['etamax']
            module_str += '\'nph\' : \'%s\', ' %( config['nph'] )
            module_str += '\'eveto\' : \'%s\', ' %( config['eveto'] )
            module_str += '\'type\' : \'%s\', ' %( config['type'] )
            module_str += '}'
            
            print module_str

            command = command_base %{ 'base' : base, 'job' : job, 'nFilesPerJob' : nFilesPerJob, 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : module, 'moduleArgs' : "%s" %module_str, 'ptmin' : config['ptmin'], 'ptmax' : config['ptmax'], 'etamin' : config['etamin'], 'etamax' : config['etamax'], 'conf_file' : job_confname }

            #if not first :
            #    command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first :
                first = False

if options.check :
    for config in configs :
    
        for base, job in jobs :

            job_name = 'conf_%s_pt_%d-%d_eta_%.2f-%.2f.txt' %(job, config['ptmin'],config['ptmax'],config['etamin'],config['etamax'])
    
            command = check_commands_base%{ 'base': base , 'job' : job, 'ptmin' : config['ptmin'], 'ptmax' : config['ptmax'], 'etamin' : config['etamin'], 'etamax' : config['etamax'], 'treename' : treename}
            print command                                                                               
            os.system(command)                                                                          
                                                                                                        



