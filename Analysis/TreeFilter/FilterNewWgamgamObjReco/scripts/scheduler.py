import os

base_alberto = '/eos/cms/store/user/abelloni/Wgamgam/FilteredSamplesJan14'
base_josh = '/eos/cms/store/user/jkunkle/Wgamgam/FilteredSamplesJan14'
#base_data = '/eos/cms/store/group/phys_smp/ggNtuples/data'
base_mc2 = '/eos/cms/store/group/phys_smp/ggNtuples/mc'
base_mc = '/eos/cms/store/group/phys_egamma/cmkuo'

jobs = [

    ##(base_alberto, 'job_electron_2012a_Jan22rereco'),
    ##(base_alberto, 'job_electron_2012b_Jan22rereco'),
    ##(base_josh, 'job_electron_2012c_Jan2012rereco'),
    (base_josh, 'job_electron_2012d_Jan22rereco'),
    (base_josh, 'job_muon_2012a_Jan22rereco'),
    #(base_josh, 'job_muon_2012b_Jan22rereco'),
    (base_josh, 'job_muon_2012c_Jan22rereco'),
    (base_josh, 'job_muon_2012d_Jan22rereco'),
    #(base_josh, 'job_summer12_DYJetsToLL'),
    #(base_josh, 'job_summer12_WAA_ISR'),
    #(base_josh, 'job_summer12_WH_ZH_125'),
    #(base_josh, 'job_summer12_WWW'),
    #(base_josh, 'job_summer12_WWZ'),
    #(base_josh, 'job_summer12_WW_2l2nu'),
    #(base_josh, 'job_summer12_WWg'),
    #(base_josh, 'job_summer12_WZZ'),
    #(base_josh, 'job_summer12_WZ_2l2q'),
    #(base_josh, 'job_summer12_WZ_3lnu'),
    #(base_josh, 'job_summer12_Wg'),
    #(base_josh, 'job_summer12_Wgg_FSR'),
    #(base_josh, 'job_summer12_Wjets'),
    #(base_josh, 'job_summer12_ZZZ'),
    #(base_josh, 'job_summer12_ZZ_2e2mu'),
    #(base_josh, 'job_summer12_ZZ_2e2tau'),
    #(base_josh, 'job_summer12_ZZ_2l2nu'),
    #(base_josh, 'job_summer12_ZZ_2l2q'),
    #(base_josh, 'job_summer12_ZZ_2mu2tau'),
    #(base_josh, 'job_summer12_ZZ_2q2nu'),
    #(base_josh, 'job_summer12_ZZ_4e'),
    #(base_josh, 'job_summer12_ZZ_4mu'),
    #(base_josh, 'job_summer12_ZZ_4tau'),
    #(base_josh, 'job_summer12_Zg'),
    #(base_josh, 'job_summer12_diphoton_box_10to25'),
    #(base_josh, 'job_summer12_diphoton_box_250toInf'),
    #(base_josh, 'job_summer12_diphoton_box_25to250'),
    #(base_josh, 'job_summer12_ggH_125'),
    #(base_josh, 'job_summer12_ggZZ_2l2l'),
    #(base_josh, 'job_summer12_ggZZ_4l'),
    #(base_josh, 'job_summer12_t_s'),
    #(base_josh, 'job_summer12_t_t'),
    #(base_josh, 'job_summer12_t_tW'),
    #(base_josh, 'job_summer12_tbar_s'),
    #(base_josh, 'job_summer12_tbar_t'),
    #(base_josh, 'job_summer12_tbar_tW'),
    #(base_josh, 'job_summer12_ttW'),
    #(base_josh, 'job_summer12_ttZ'),
    #(base_josh, 'job_summer12_ttg'),
    #(base_josh, 'job_summer12_ttjets_1l'),
    #(base_josh, 'job_summer12_ttjets_2l'),

]

command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s/ --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob %(nfiles)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --nproc %(nproc)d --confFileName %(job)s.txt --exeName %(exe)s '

#command_base = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob %(nfiles)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --nproc %(nproc)d --confFileName %(job)s.txt '

#command_base = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob %(nfiles)d --nproc %(nproc)s --confFileName %(job)s.txt --nsplit %(nsplit)d '

#command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob 1 --nproc %(nproc)s --confFileName %(job)s.txt '

output = 'RecoOutput_2014_01_16'
nFilesPerJob = 2
nSplit = 8
nProc = 8
exe='RunAnalysis'

first = True
for base, job in jobs :
    command = command_base %{ 'base' : base, 'job' : job, 'nfiles' : nFilesPerJob, 'nsplit' : nSplit, 'output' : output, 'nproc' : nProc, 'exe' : exe }
    if not first :
        command += ' --noCompile'
    print command
    os.system(command)

    if first :
        first = False
