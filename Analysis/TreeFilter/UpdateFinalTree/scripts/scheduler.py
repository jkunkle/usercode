import os
#base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaPt25_2013_12_05/'
base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/'
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--test', default=False, action='store_true', dest='test', help='do not run, just print commands' )

options = parser.parse_args()


jobs_data = [
        #(base, 'job_electron_2012a_Jan22rereco'),
        #(base, 'job_electron_2012b_Jan22rereco'),
        #(base, 'job_electron_2012c_Jan2012rereco'),
        #(base, 'job_electron_2012d_Jan22rereco'),
        (base, 'job_muon_2012a_Jan22rerecoTightBlind'),
        (base, 'job_muon_2012b_Jan22rerecoTightBlind'),
        (base, 'job_muon_2012c_Jan22rerecoTightBlind'),
        (base, 'job_muon_2012d_Jan22rerecoTightBlind'),
]
jobs_mc = [
        #(base, 'job_summer12_DYJetsToLL'),
        #(base, 'job_summer12_DiPhotonBorn_Pt-10To25'),
        #(base, 'job_summer12_WAA_ISR'),
        #(base, 'job_summer12_Wgg_FSR'),
        #(base, 'job_summer12_WH_ZH_125'),
        #(base, 'job_summer12_WWW'),
        #(base, 'job_summer12_WWZ'),
        #(base, 'job_summer12_WW_2l2nu'),
        #(base, 'job_summer12_WWg'),
        #(base, 'job_summer12_WZZ'),
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
        #(base, 'job_summer12_ttg'),
        #(base, 'job_summer12_ttinclusive'),
        #(base, 'job_summer12_ttjets_1l'),
        #(base, 'job_summer12_ttjets_2l'),
        #(base, 'job_summer12_DYJetsToLLPhOlap' ),
        #(base, 'job_summer12_WjetsPhOlap' ),
        #(base, 'job_summer12_WgPhOlap' ),

]

#module_mc   = 'ConfLepGammaFilter.py'
#module_data = 'ConfLepGammaFilter_Data.py'
#output_name = 'LepGamma_2013_11_04'

top_configs = [ 
                { 
                  'module_mc'   : 'ConfUpdate.py',
                  'module_data' : 'ConfUpdate.py',
                  'output_name' : 'LepGammaNoEleVetoNewVarPUBiasWt_2014_05_02',
                  'input_name'  : 'LepGammaNoEleVetoNewVar_2014_05_02',
                  'tag'         : 'll',
                },
                #{ 
                #  'module_mc'   : 'ConfUpdate.py',
                #  'module_data' : 'ConfUpdate.py',
                #  'output_name' : 'LepGammaLoosePhUpdate_2014_02_25',
                #  'input_name'  : 'LepGammaLoosePh_2014_02_24',
                #  'tag'         : 'll',
                #},
]

command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output_name)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --nFilesPerJob 1 --nproc 8 --confFileName %(tag)s_%(job)s.txt --sample %(job)s'
#command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output_name)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --nFilesPerJob 1 --nproc 8 --confFileName %(tag)s_%(job)s.txt '

first = True
for config in top_configs :

    for base, job in jobs_data :
    
        command = command_base %{ 'base' : base, 'job' : job, 'input' : config['input_name'], 'output_name' : config['output_name'], 'module' : config['module_data'], 'tag' : config['tag']  }
        #if not first :
        #    command += ' --noCompile '

        if options.test :
            print command
        else :
            os.system(command)
        first = False
    
    for base, job in jobs_mc :
    
        command = command_base %{ 'base' : base, 'job' : job, 'input' : config['input_name'], 'output_name' : config['output_name'], 'module' : config['module_mc'], 'tag' : config['tag']  }
        if not first :
            command += ' --noCompile '
    
        if options.test :
            print command
        else :
            os.system(command)
        first = False
