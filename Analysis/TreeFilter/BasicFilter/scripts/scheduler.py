import os
#base = '/eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2014_01_16'
#base = '/eos/cms/store/group/phys_egamma/cmkuo/'
base = '/eos/cms/store/user/jkunkle/Samples/ggNtuples'

jobs = [
       #(base, 'job_electron_2012a_Jan22rereco'),
       #(base, 'job_electron_2012b_Jan22rereco'),
       #(base, 'job_electron_2012c_Jan2012rereco'),
       #(base, 'job_electron_2012d_Jan22rereco'),
       #(base, 'job_muon_2012a_Jan22rereco'),
       #(base, 'job_muon_2012b_Jan22rereco'),
       #(base, 'job_muon_2012c_Jan22rereco'),
       #(base, 'job_muon_2012d_Jan22rereco'),
       #(base, 'job_summer12_DYJetsToLL'),
       #(base, 'job_summer12_WAA_ISR'),
       #(base, 'job_summer12_Wgg_FSR'),
       #(base, 'job_summer12_WH_ZH_125'),
       #(base, 'job_summer12_WWW'),
       #(base, 'job_summer12_WWZ'),
       #(base, 'job_summer12_WW_2l2nu'),
       #(base, 'job_summer12_WWg'),
       #(base, 'job_summer12_WZZ'),
       #(base, 'job_summer12_WZ_2l2q'),
       #(base, 'job_summer12_WZ_3lnu'),
       #(base, 'job_summer12_Wg'),
       #(base, 'job_summer12_Wjets'),
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
       #(base, 'job_summer12_Zg'),
       (base, 'job_summer12_Zgg'),
       #(base, 'job_summer12_diphoton_box_10to25'),
       #(base, 'job_summer12_diphoton_box_250toInf'),
       #(base, 'job_summer12_diphoton_box_25to250'),
       #(base, 'job_summer12_ggH_125'),
       #(base, 'job_summer12_t_s'),
       #(base, 'job_summer12_t_t'),
       #(base, 'job_summer12_t_tW'),
       #(base, 'job_summer12_tbar_s'),
       #(base, 'job_summer12_tbar_t'),
       #(base, 'job_summer12_tbar_tW'),
       #(base, 'job_summer12_ttg'),
       #(base, 'job_summer12_ttjets_1l'),
       #(base, 'job_summer12_ttjets_2l'),
]

#command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s/ --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfBasic.py --enableKeepFilter --nFilesPerJob %(nfiles)d --nproc %(nproc)d --confFileName %(job)s.txt '
command_base = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfBasic.py --enableKeepFilter --nFilesPerJob %(nfiles)d --nproc %(nproc)d --nsplit %(nsplit)d --confFileName %(job)s.txt '

output = 'SignalTruth_2014_03_08'
nFilesPerJob = 0
nProc = 6
nSplit=6

first = True
for base, job in jobs :
    command = command_base %{ 'base' : base, 'job' : job, 'nfiles' : nFilesPerJob, 'output' : output, 'nproc' : nProc, 'nsplit': nSplit}
    if not first :
        command += ' --noCompile'
    print command
    os.system(command)

    if first :
        first = False

