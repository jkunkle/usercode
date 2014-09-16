import os
#base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaPt25_2013_12_05/'
base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNom_2014_06_16/'

jobs= [
        (base, 'job_electron_2012a_Jan22rereco'),
        (base, 'job_electron_2012b_Jan22rereco'),
        (base, 'job_electron_2012c_Jan2012rereco'),
        (base, 'job_electron_2012d_Jan22rereco'),
        #(base, 'job_summer12_DYJetsToLL'),
        #(base, 'job_summer12_LNuGG_FSR'),
        #(base, 'job_summer12_LNuGG_ISR'),
        #(base, 'job_summer12_WJetsToLNu1'),
        #(base, 'job_summer12_WJetsToLNu2'),
        #(base, 'job_summer12_WWW'),
        #(base, 'job_summer12_WWZ'),
        #(base, 'job_summer12_WW_2l2nu'),
        #(base, 'job_summer12_WZZ'),
        #(base, 'job_summer12_WZ_2l2q'),
        #(base, 'job_summer12_WZ_3lnu'),
        #(base, 'job_summer12_Wg'),
        #(base, 'job_summer12_ZZZ'),
        #(base, 'job_summer12_ZZ_2e2mu'),
        #(base, 'job_summer12_ZZ_2e2tau'),
        #(base, 'job_summer12_ZZ_2l2q'),
        #(base, 'job_summer12_ZZ_2mu2tau'),
        #(base, 'job_summer12_ZZ_4e'),
        #(base, 'job_summer12_ZZ_4mu'),
        #(base, 'job_summer12_ZZ_4tau'),
        #(base, 'job_summer12_Zg'),
        #(base, 'job_summer12_gjet_pt20to40_doubleEM'),
        #(base, 'job_summer12_gjet_pt40_doubleEM'),
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

#module_mc   = 'ConfLepGammaFilter.py'
#module_data = 'ConfLepGammaFilter_Data.py'
#output_name = 'LepGamma_2013_11_04'

top_configs = [ 
                { 
                  'module' : 'Conf.py',
                  'output_name' : 'LeadWeight',
                  'args'        : '{ \'DoLeadWeight\' : True, \'DoSublWeight\' : False } '
                },
                { 
                  'module' : 'Conf.py',
                  'output_name' : 'SublWeight',
                  'args'        : '{ \'DoLeadWeight\' : False, \'DoSublWeight\' : True } '
                },
]

command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir %(base)s/%(job)s_%(output_name)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --nsplit 1 --moduleArgs "%(args)s" '

for config in top_configs :

    for base, job in jobs :
    
        command = command_base %{ 'base' : base, 'job' : job, 'output_name' : config['output_name'], 'module' : config['module'], 'args' : config['args'] }
        print command
        os.system(command)


