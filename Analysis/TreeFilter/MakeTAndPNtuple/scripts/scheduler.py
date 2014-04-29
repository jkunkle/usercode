import os
base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/'


jobs_data = [
    #(base, 'job_electron_2012a_Jan22rereco'),
    #(base, 'job_electron_2012b_Jan22rereco'),
    #(base, 'job_electron_2012c_Jan2012rereco'),
    #(base, 'job_electron_2012d_Jan22rereco'),
    #(base, 'job_muon_2012a_Jan22rereco'),
    #(base, 'job_muon_2012b_Jan22rereco'),
    #(base, 'job_muon_2012c_Jan22rereco'),
    #(base, 'job_muon_2012d_Jan22rereco'),
]
jobs_mc = [
    #(base, 'job_summer12_DYJetsToLL'),
    (base, 'job_summer12_DYJetsToLLPhOlap'),
    #(base, 'job_summer12_WAA_ISR'),
    #(base, 'job_summer12_WH_ZH_125'),
    #(base, 'job_summer12_WWW'),
    #(base, 'job_summer12_WWZ'),
    #(base, 'job_summer12_WW_2l2nu'),
    #(base, 'job_summer12_WWg'),
    #(base, 'job_summer12_WZZ'),
    #(base, 'job_summer12_WZ_2l2q'),
    #(base, 'job_summer12_WZ_3lnu'),
    #(base, 'job_summer12_Wg'),
    #(base, 'job_summer12_WgPhOlap'),
    #(base, 'job_summer12_Wgg_FSR'),
    #(base, 'job_summer12_Wjets'),
    (base, 'job_summer12_WjetsPhOlap'),
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

second_base = ['DiLeptonTightPh_2014_02_12', 'LepGammaTightPh_2014_02_12']

#module_mc   = 'ConfLepGammaFilter.py'
#module_data = 'ConfLepGammaFilter_Data.py'
output_name = 'TAndPTightPh_2014_02_12'

command_base = 'python scripts/filter.py  --filesDir %(input)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/ConfTAndP.py --nFilesPerJob 1 --nproc 8 --enableRemoveFilter %(addtl)s'

addtl = ''
for base, job in jobs_data+jobs_mc :

    input_dirs = []
    for sb in second_base :
        input_dirs.append( '%s/%s/%s' %( base, sb, job ) )
    
    command = command_base %{ 'input' : ','.join(input_dirs), 'output' : output_name, 'job' : job, 'addtl' : addtl }
    print command
    os.system(command)
    
    if not addtl :
        addtl = ' --noCompile'
