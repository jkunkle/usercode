import os

base_muon = '/eos/cms/store/user/abelloni/Wgamgam/FilteredSamplesDec13'
base_elec = '/eos/cms/store/user/jkunkle/Wgamgam/FilteredSamplesDec13'
base_data = '/eos/cms/store/group/phys_smp/ggNtuples/data'
base_mc2 = '/eos/cms/store/group/phys_smp/ggNtuples/mc'
base_mc = '/eos/cms/store/group/phys_egamma/cmkuo'
base_skim = '/eos/cms/store/group/phys_egamma/cmkuo/skim_gg'

jobs = [

        (base_skim, 'job_summer12_gjet_pt20to40_doubleEM', 10),
        (base_skim, 'job_summer12_gjet_pt40_doubleEM', 10),
        (base_skim, 'job_summer12_qcd_pt30to40_doubleEM', 10),
        (base_skim, 'job_summer12_qcd_pt40_doubleEM', 10),
]

#command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s/ --fileKey tree.root --outputDir /tmp/jkunkle/%(base)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob %(nfiles)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --nproc %(nsplit)d --confFileName %(job)s '

#command_base = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob %(nfiles)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --nproc %(nproc)d --confFileName %(job)s.txt '

command_base = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/ConfWgamgamReco.py  --nproc %(nproc)s  --nsplit %(nsplit)d --exeName %(exename)s  '

#command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob 1 --nproc %(nproc)s --confFileName %(job)s.txt '

output = 'PhSkimMod_2014_04_15'
nFilesPerJob = 1
nProc = 6
exename='RunAnalysis'
#treename='ggNtuplizer/EventTree'
treename='tt'

for base, job, nsplit in jobs :
    command = command_base %{ 'base' : base, 'job' : job, 'nfiles' : nFilesPerJob, 'output' : output, 'nsplit': nsplit, 'nproc' : nProc, 'exename' : exename, 'treename' : treename }
    print command
    os.system(command)
