import os

base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNom_2014_06_16'
jobs = [
        #(base, 'job_muon_2012a_Jan22rereco'),
        #(base, 'job_muon_2012b_Jan22rereco'),
        #(base, 'job_muon_2012c_Jan22rereco'),
        #(base, 'job_muon_2012d_Jan22rereco'),
        #(base, 'job_electron_2012a_Jan22rereco'),
        #(base, 'job_electron_2012b_Jan22rereco'),
        #(base, 'job_electron_2012c_Jan2012rereco'),
        #(base, 'job_electron_2012d_Jan22rereco'),
        #(base_mc, 'job_summer12_DiPhotonBorn_Pt-10To25', 10),
        #(base_mc2, 'job_summer12_DYJetsToLL', 50 ),
        #(base_mc, 'job_summer12_Wjets', 100),
        #(base_mc, 'job_summer12_Wg', 50),
        #(base, 'job_summer12_DYJetsToLL'),
        #(base, 'job_summer12_Zg'),
        (base, 'job_summer12_Wgg_FSR'),
        #(base, 'job_summer12_WAA_ISR'),
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

output = 'LepGammaGammaForZMva1EleVeto_2014_06_19'

#command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s/ --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s/ --module scripts/Conf.py  --treeName ggNtuplizer/EventTree --nFilesPerJob 1 --nproc %(nproc)d'
command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s/ --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s/ --module scripts/Conf.py  --treeName ggNtuplizer/EventTree '

nProc = 8

for base, job in jobs :
    command = command_base %{ 'base' : base, 'job' : job, 'output' : output, 'nproc' : nProc }
    print command
    os.system(command)
