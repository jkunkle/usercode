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

base = r'/eos/cms/store/user/jkunkle/Wgamgam/LepGammaNoPhIDNoEleOlap_2014_12_29'
#base = r'/eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2014_12_05'

jobs_data = [
    (base, 'job_electron_2012a_Jan22rereco'),
    (base, 'job_electron_2012b_Jan22rereco'),
    (base, 'job_electron_2012c_Jan2012rereco'),
    (base, 'job_electron_2012d_Jan22rereco'),
    #(base, 'job_muon_2012a_Jan22rereco'),
    #(base, 'job_muon_2012b_Jan22rereco'),
    #(base, 'job_muon_2012c_Jan22rereco'),
    #(base, 'job_muon_2012d_Jan22rereco'),
]
jobs_mc = [
    (base, 'job_summer12_DYJetsToLLPhOlap'),
    #(base, 'job_summer12_DYJetsToLL'),
    #(base, 'job_summer12_Zg'),
    #(base, 'job_summer12_Wg'),
    #(base, 'job_summer12_Wjets'),
    #(base, 'job_summer12_WAA_ISR'),
    #(base, 'job_summer12_WH_ZH_125'),
    #(base, 'job_summer12_WWW'),
    #(base, 'job_summer12_WWZ'),
    #(base, 'job_summer12_WW_2l2nu'),
    #(base, 'job_summer12_WWg'),
    #(base, 'job_summer12_WZZ'),
    #(base, 'job_summer12_WZ_2l2q'),
    #(base, 'job_summer12_WZ_3lnu'),
    #(base, 'job_summer12_WgPhOlap'),
    #(base, 'job_summer12_Wgg_FSR'),
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
    #(base, 'job_summer12_ggH_125'),
    #(base, 'job_summer12_ggZZ_2l2l'),
    #(base, 'job_summer12_ggZZ_4l'),
    #(base, 'job_summer12_t_s'),
    #(base, 'job_summer12_t_t'),
    #(base, 'job_summer12_t_tW'),
    #(base, 'job_summer12_tbar_s'),
    #(base, 'job_summer12_tbar_t'),
    #(base, 'job_summer12_tbar_tW'),
    #(base, 'job_summer12_ttW'),
    #(base, 'job_summer12_ttZ'),
    #(base, 'job_summer12_ttg'),
    #(base, 'job_summer12_ttjets_1l'),
    #(base, 'job_summer12_ttjets_2l'),

]

output_name = 'TAndPElFF_2015_01_01'
#output_name = 'TAndPMuMu_2014_11_27'
module = 'ConfTAndP.py'
#module = 'ConfMuonTAndP.py'
treename='ggNtuplizer/EventTree'

if options.local :
    command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(input)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --nFilesPerJob 1 --nproc 6 --enableRemoveFilter  --disableOutputTree'

else :

    command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(input)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --nFilesPerJob 1 --batch --enableRemoveFilter --disableOutputTree'

if options.resubmit :
    command_base += ' --resubmit'

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(job)s --filteredDS /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'

if options.run :
    for base, job in jobs_data+jobs_mc :
    
        command = command_base %{ 'input' : base+'/'+job, 'output' : output_name, 'job' : job, 'module' : module }
        print command
        os.system(command)
    
if options.check :
    for base, job in jobs_data+jobs_mc :
        command = check_commands_base%{ 'base': base , 'job' : job, 'output' : output_name, 'treename' : treename}
        print command
        os.system(command)
        
