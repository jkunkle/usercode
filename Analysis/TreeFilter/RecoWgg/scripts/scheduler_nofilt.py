import os

base_muon = '/eos/cms/store/user/abelloni/Wgamgam/FilteredSamplesDec13'
base_elec = '/eos/cms/store/user/jkunkle/Wgamgam/FilteredSamplesDec13'
base_data = '/eos/cms/store/group/phys_smp/ggNtuples/data'
base_mc2 = '/eos/cms/store/group/phys_smp/ggNtuples/mc'
base_mc = '/eos/cms/store/group/phys_egamma/cmkuo'
base_skim = '/eos/cms/store/group/phys_egamma/cmkuo/skim_gg'
base_me = '/eos/cms/store/user/jkunkle/Samples/ggNtuples'

jobs = [
        #(base_data, 'job_muon_2012a_Jan22rereco', 50),
        #(base_data, 'job_muon_2012b_Jan22rereco', 100),
        #(base_data, 'job_muon_2012c_Jan22rereco', 200),
        #(base_data, 'job_muon_2012d_Jan22rereco', 200),
        #(base_data, 'job_electron_2012a_Jan22rereco', 100),
        #(base_data, 'job_electron_2012b_Jan22rereco', 200),
        #(base_data, 'job_electron_2012c_Jan2012rereco', 400),
        #(base_data, 'job_electron_2012d_Jan22rereco', 400),
        #(base_mc, 'job_summer12_DiPhotonBorn_Pt-10To25', 10),
        #(base_mc2, 'job_summer12_DYJetsToLL', 50 ),
        #(base_mc, 'job_summer12_Wjets', 100),
        #(base_mc, 'job_summer12_Wg', 50),
        (base_mc, 'job_summer12_Zg', 50),
        #(base_mc, 'job_summer12_Wgg_FSR', 20),
        #(base_mc, 'job_summer12_WAA_ISR', 20),
        #(base_mc, 'job_summer12_ttjets_1l', 50),
        #(base_mc, 'job_summer12_ttjets_2l', 50),
        #(base_mc, 'job_summer12_ttg', 20),
        #(base_mc, 'job_summer12_WH_ZH_125', 10),
        #(base_mc, 'job_summer12_WWW', 10),
        #(base_mc, 'job_summer12_WWZ', 10),
        #(base_mc, 'job_summer12_WW_2l2nu', 10),
        #(base_mc, 'job_summer12_WWg', 10),
        #(base_mc, 'job_summer12_WZZ', 10),
        #(base_mc, 'job_summer12_WZ_2l2q', 10),
        #(base_mc, 'job_summer12_WZ_3lnu', 10),
        #(base_mc, 'job_summer12_ZZZ', 10),
        #(base_mc, 'job_summer12_ZZ_2e2mu', 10),
        #(base_mc, 'job_summer12_ZZ_2e2tau', 10),
        #(base_mc, 'job_summer12_ZZ_2l2nu', 10),
        #(base_mc, 'job_summer12_ZZ_2l2q', 10),
        #(base_mc, 'job_summer12_ZZ_2mu2tau', 10),
        #(base_mc, 'job_summer12_ZZ_2q2nu', 10),
        #(base_mc, 'job_summer12_ZZ_4e', 10),
        #(base_mc, 'job_summer12_ZZ_4mu', 10),
        #(base_mc, 'job_summer12_ZZ_4tau', 10),
        #(base_mc, 'job_summer12_diphoton_box_10to25', 10),
        #(base_mc, 'job_summer12_diphoton_box_250toInf', 10),
        #(base_mc, 'job_summer12_diphoton_box_25to250', 10),
        #(base_mc, 'job_summer12_ggZZ_2l2l', 10),
        #(base_mc, 'job_summer12_ggZZ_4l', 10),
        #(base_mc, 'job_summer12_t_s', 20),
        #(base_mc, 'job_summer12_t_t', 20),
        #(base_mc, 'job_summer12_t_tW', 20),
        #(base_mc, 'job_summer12_tbar_s', 20),
        #(base_mc, 'job_summer12_tbar_t', 20),
        #(base_mc, 'job_summer12_tbar_tW', 20),
        #(base_mc, 'job_summer12_ttW', 20),
        #(base_mc, 'job_summer12_ttZ', 20),
        #(base_mc, 'job_summer12_ttinclusive', 100),
        #(base_me, 'QCD_Pt-40_doubleEMEnriched', 20),
        #(base_me, 'job_summer12_WgPt50-130', 40),
        #(base_me, 'job_summer12_WgPt130', 40),
        #(base_me, 'job_summer12_WgPt30-50', 40),
        #(base_me, 'job_summer12_WgPt20-30', 40),


]

#command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s/ --fileKey tree.root --outputDir /tmp/jkunkle/%(base)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob %(nfiles)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --nproc %(nsplit)d --confFileName %(job)s '

#command_base = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob %(nfiles)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --nproc %(nproc)d --confFileName %(job)s.txt '

command_base = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/ConfWgamgamReco.py --enableKeepFilter --nproc %(nproc)s --confFileName %(job)s.txt --nsplit %(nsplit)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --exeName %(exename)s --moduleArgs "{ \'sampleFile\' : \'root://eoscms/%(base)s/%(job)s.root\'}"; python ../../Util/scripts/clean_conf_files.py --path /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s '

#command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s --fileKey tree.root --outputDir /tmp/jkunkle/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfWgamgamReco.py --enableKeepFilter --nFilesPerJob 1 --nproc %(nproc)s --confFileName %(job)s.txt '

output = 'RecoOutputNoEleVeto_2014_04_25'
nFilesPerJob = 1
nProc = 8
exename='RunAnalysisMC2'
treename='ggNtuplizer/EventTree'
#treename='tt'

for base, job, nsplit in jobs :
    command = command_base %{ 'base' : base, 'job' : job, 'nfiles' : nFilesPerJob, 'output' : output, 'nsplit': nsplit, 'nproc' : nProc, 'exename' : exename, 'treename' : treename }
    print command
    #os.system(command)
