import os
#base = '/eos/cms/store/user/jkunkle/Wgamgam/OutputS2TestNoPhJetOlap_2013_11_03'
#base = '/eos/cms/store/user/jkunkle/Wgamgam/RecoOutputOnlyDYNoTrigFilt_2014_02_03'
#base = '/eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2013_12_07'
#base_tmp = '/tmp/tEST/RecoOutputTESTNoCorr_2014_02_05/'
base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_04_28'

jobs = [
        #(base, 'job_summer12_Wg'),
        #(base, 'job_summer12_WgPhOlap'),
        (base, 'job_summer12_WAA_ISR'),
        (base, 'job_summer12_Wgg_FSR'),
        #(base, 'job_summer12_DYJetsToLL'),
        #(base, 'job_summer12_DYJetsToLLPhOlap'),
        #(base, 'job_summer12_Wjets'),
        #(base, 'job_summer12_WjetsPhOlap'),
        (base, 'job_summer12_Zg'),
        #(base, 'job_summer12_ttjets_1l'),
        #(base, 'job_summer12_ttjets_2l'),
        #(base, 'job_summer12_ttjets_1lPhOlap'),
        #(base, 'job_summer12_ttjets_2lPhOlap'),
        #(base, 'job_summer12_ttg'),
        #(base, 'job_summer12_WgPt20-30'),
        #(base, 'job_summer12_WgPt30-50'),
        #(base, 'job_summer12_WgPt50-130'),
        #(base, 'job_summer12_WgPt130'),
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
        #(base, 'job_summer12_ttinclusive'),
        ##(base_tmp, 'DYJetsToLLPhOlap' )
        ##(base_tmp, 'WjetsPhOlap' )
        ##(base_tmp, 'WgPhOlap' )
]

output = 'LepGammaNoEleVetoNewVarZMVA_2014_04_28'

command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --nFilesPerJob 1 --nproc %(nproc)d '

nproc=8
module = 'ConfEval.py'

for base, job in jobs :

    command = command_base %{ 'base': base ,  'job' : job, 'module' : module, 'nproc' : nproc, 'output' : output}
    print command
    os.system(command)
    

