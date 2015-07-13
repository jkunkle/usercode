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

#base = '/eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2014_01_16'
#base = '/eos/cms/store/group/phys_egamma/cmkuo/'
#base = '/eos/cms/store/user/jkunkle/Samples/ggNtuples'
base = r'/eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2015_04_05'
base_nlo = r'/eos/cms/store/user/cranelli/WGamGam/NLO_ggNtuples'
#base_nlo = r'/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/'

jobs = [
        #(base, 'job_electron_2012a_Jan22rereco'),
        #(base, 'job_electron_2012b_Jan22rereco'),
        #(base, 'job_electron_2012c_Jan2012rereco'),
        #(base, 'job_electron_2012d_Jan22rereco'),
        #(base, 'job_muon_2012a_Jan22rereco'),
        #(base, 'job_muon_2012b_Jan22rereco'),
        #(base, 'job_muon_2012c_Jan22rereco'),
        #(base, 'job_muon_2012d_Jan22rereco'),

         (base_nlo, 'job_NLO_WAA_ISR'),
         #(base_nlo, 'job_NLO_WAA_FSR'),

        #(base, 'job_summer12_DYJetsToLL'),
        #(base, 'job_summer12_Zg'),
        #(base, 'job_summer12_Wg'),
        #(base, 'job_summer12_Wjets'),
        #(base, 'job_summer12_ttjets_1l'),
        #(base, 'job_summer12_ttjets_2l'),
        #(base, 'job_summer12_Zgg'),
        #(base, 'job_summer12_WAA_ISR'),
        #(base, 'job_summer12_Wgg_FSR'),
        #(base, 'job_summer12_ttg'),
        #(base, 'job_summer12_WgPt130'),
        #(base, 'job_summer12_WgPt50-130'),
        #(base, 'job_summer12_WgPt30-50'),
        #(base, 'job_summer12_WgPt20-30'),
        #(base, 'job_summer12_DiPhotonBorn_Pt-10To25'),
        #(base, 'job_summer12_WH_ZH_125'),
        #(base, 'job_summer12_WWW'),
        #(base, 'job_summer12_WWZ'),
        #(base, 'job_summer12_WW_2l2nu'),
        #(base, 'job_summer12_WWg'),
        #(base, 'job_summer12_WZZ'),
        #(base, 'job_summer12_WZ_3lnu'),
        #(base, 'job_summer12_ZZZ'),
        #(base, 'job_summer12_ZZ_2e2mu'),
        #(base, 'job_summer12_ZZ_2e2tau'),
        #(base, 'job_summer12_ZZ_2l2nu'),
        #(base, 'job_summer12_ZZ_2l2q'),
        #(base, 'job_summer12_ZZ_2mu2tau'),
        #(base, 'job_summer12_ZZ_2q2nu'),
        #(base, 'job_summer12_ZZ_4e'),
        #(base, 'job_summer12_ZZ_4mu'),
        #(base, 'job_summer12_ZZ_4tau'),
        #(base, 'job_summer12_diphoton_box_10to25'),
        #(base, 'job_summer12_diphoton_box_250toInf'),
        #(base, 'job_summer12_diphoton_box_25to250'),
        #(base, 'job_summer12_ggZZ_2l2l'),
        #(base, 'job_summer12_ggZZ_4l'),
        #(base, 'job_summer12_t_s'),
        #(base, 'job_summer12_t_t'),
        #(base, 'job_summer12_t_tW'),
        #(base, 'job_summer12_tbar_s'),
        #(base, 'job_summer12_tbar_t'),
        #(base, 'job_summer12_tbar_tW'),
        #(base, 'job_jfaulkne_WZA'),
        #(base, 'job_summer12_ttZ'),
        #(base, 'job_summer12_ttW'),
        #(base, 'QCD_Pt-40_doubleEMEnriched')

        ##(base, 'job_summer12_ttinclusive'),
]
#command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s/ --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfBasic.py --enableKeepFilter --nFilesPerJob %(nfiles)d --nproc %(nproc)d --confFileName %(job)s.txt '
if options.local :
    command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --nFilesPerJob %(nFilesPerJob)d --nproc 5 --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s  --enableKeepFilter'
else :
    command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --nFilesPerJob %(nFilesPerJob)d --batch --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s  --enableKeepFilter'

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(job)s --filteredDS /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'

if options.resubmit :
    command_base += ' --resubmit'

#output = 'SignalTruth_2014_03_08'
#nFilesPerJob = 0
#nProc = 6
#nSplit=6
#
#first = True
#for base, job in jobs :
#    command = command_base %{ 'base' : base, 'job' : job, 'nfiles' : nFilesPerJob, 'output' : output, 'nproc' : nProc, 'nsplit': nSplit}
#    if not first :
#        command += ' --noCompile'
#    print command
#    os.system(command)
#
#    if first :
#        first = False

top_configs = [ 
                #{ 
                #  'module'      : 'ConfBasic.py',
                #  'output_name' : 'SingleLeptonLoose_2015_04_10',
                #  'tag'         : 'singlLep',
                #},
                { 
                  'module'      : 'ConfTruthFilter.py',
                  'output_name' : 'WAANLOTruth_2015_06_23',
                  'tag'         : 'truth',
                },
]

nFilesPerJob = 5
nproc=5
treename='ggNtuplizer/EventTree'

if options.run :
    for config in top_configs :
    
        for base, job in jobs :
    
            command = command_base %{ 'base': base , 'job' : job, 'output' : config['output_name'], 'module' : config['module'], 'tag' : config['tag'], 'nproc' : nproc, 'exe' : 'RunAnalysis%s%s' %(config['tag'], job), 'nFilesPerJob': nFilesPerJob, 'treename' : treename}
            print command
            os.system(command)
        

if options.check :
    for config in top_configs :
    
        for base, job in jobs :
    
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'treename' : treename}
            print command
            os.system(command)


