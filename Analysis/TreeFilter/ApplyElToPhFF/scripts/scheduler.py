import os
#base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaPt25_2013_12_05/'
base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/DiLeptonLoosePhLowPtTrigMatch_2014_02_07'
output_base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/'
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--test', default=False, action='store_true', dest='test', help='do not run, just print commands' )

options = parser.parse_args()


jobs_data = [
        #(base, 'job_1electron_2012b_Jul13rereco_run1'),
        #(base, 'job_1electron_2012b_Jul13rereco_run2'),
        #(base, 'job_1electron_2012c_Aug24rereco'),
        #(base, 'job_1electron_2012c_Dec11rereco'),
        #(base, 'job_1electron_2012c_PRv2_part1'),
        #(base, 'job_1electron_2012c_PRv2_part2'),
        #(base, 'job_1electron_2012c_PRv2_part3'),
        #(base, 'job_1electron_2012d_PRv1_part1'),
        #(base, 'job_1electron_2012d_PRv1_part2'),
        #(base, 'job_electron_2012a_Aug6rereco'),
        #(base, 'job_electron_2012a_Jul13rereco'),
        #(base, 'job_muon_2012a_Aug6rereco'),
        #(base, 'job_muon_2012a_Jul13rereco'),
        #(base, 'job_muon_2012b_Jul13rereco'),
        #(base, 'job_muon_2012c_Aug24rereco'),
        #(base, 'job_muon_2012c_Dec11rereco'),
        #(base, 'job_muon_2012c_PRv2'),
        #(base, 'job_muon_2012c_PRv21'),
        #(base, 'job_muon_2012d_PRv1'),
        #(base, 'job_muon_2012d_PRv11'),
]
jobs_mc = [
        (base, 'job_summer12_DYJetsToLL'),
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

top_configs = [ { 
                  'module_mc'   : 'Conf.py',
                  'module_data' : 'Conf.py',
                  'output_name' : 'DiLeptonFFUpdateEta1D_2014_02_10/',
                  'tag'         : 'll',
                },
]

command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir %(output_base)s/%(output_name)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --nFilesPerJob 1 --nproc 12 --confFileName %(tag)s_%(job)s.txt --sample %(job)s'
#command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output_name)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --nFilesPerJob 1 --nproc 8 --confFileName %(tag)s_%(job)s.txt '

first = True
for config in top_configs :

    for base, job in jobs_data :
    
        command = command_base %{ 'base' : base, 'job' : job, 'output_base' : output_base, 'output_name' : config['output_name'], 'module' : config['module_data'], 'tag' : config['tag']  }
        if not first :
            command += ' --noCompile '

        if options.test :
            print command
        else :
            os.system(command)
        first = False
    
    for base, job in jobs_mc :
    
        command = command_base %{ 'base' : base, 'job' : job, 'output_base' : output_base, 'output_name' : config['output_name'], 'module' : config['module_mc'], 'tag' : config['tag']  }
        if not first :
            command += ' --noCompile '
    
        if options.test :
            print command
        else :
            os.system(command)
        first = False

for config in top_configs :
    print 'Wrote output to %s/%s' %( output_base, config['output_name'] )
