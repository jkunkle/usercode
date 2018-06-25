import os
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--run'     , dest='run'     , default=False, action='store_true', help='Run filtering'              )
p.add_argument( '--check'   , dest='check'   , default=False, action='store_true', help='Run check of completion'    )
p.add_argument( '--clean'   , dest='clean'   , default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local'   , dest='local'   , default=True , action='store_true', help='Run locally'                )
p.add_argument( '--batch'   , dest='batch'   , default=False , action='store_true', help='Run batch'                )
options = p.parse_args()

if not options.run and not options.check :
    options.run = True

base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output'


jobs_data = [
        #(base, 'job_muon_2012a_Jan22rereco'),
        #(base, 'job_muon_2012b_Jan22rereco'),
        #(base, 'job_muon_2012c_Jan22rereco'),
        #(base, 'job_muon_2012d_Jan22rereco'),
        (base, 'job_electron_2012a_Jan22rereco'),
        #(base, 'job_electron_2012b_Jan22rereco'),
        #(base, 'job_electron_2012c_Jan2012rereco'),
        #(base, 'job_electron_2012d_Jan22rereco'),
        #(base, 'job_2muon_2012a_Jan22rereco'),
        #(base, 'job_2muon_2012b_Jan22rereco'),
        #(base, 'job_2muon_2012c_Jan22rereco'),
        #(base, 'job_2muon_2012d_Jan22rereco'),
        #(base, 'job_2electron_2012a_Jan22rereco'),
        #(base, 'job_2electron_2012b_Jan22rereco'),
        #(base, 'job_2electron_2012c_Jan22rereco'),
        #(base, 'job_2electron_2012d_Jan22rereco'),
]
jobs_mc = [
        #(base, 'job_NLO_WAA_FSR'),
        #(base, 'job_NLO_WAA_ISR'),
        #(base, 'job_NLO_WAA_FSR_PtG500MeV'),
        #(base, 'job_NLO_WAA_ISR_PtG500MeV'),
        #(base, 'job_summer12_Wgg_FSR'),
        #(base, 'job_summer12_WAA_ISR'),
        #(base, 'job_summer12_DYJetsToLL_s10PhOlap'),
        #(base, 'job_summer12_Wg'),
        #(base, 'job_summer12_Zg_s10'),
        #(base, 'job_summer12_Wjets'),
        #(base, 'job_summer12_WH_ZH_125'),
        #(base, 'job_summer12_WW_2l2nu'),
        #(base, 'job_summer12_WZ_2l2q'),
        #(base, 'job_summer12_WZ_3lnu'),
        #(base, 'job_summer12_WZ_lljj'),
        #(base, 'llaa_nlo_ggNtuple' ),

        ####(base, 'job_summer12_ttjets_1lPhOlap'),
        ####(base, 'job_summer12_ttjets_2lPhOlap'),
        ####(base, 'job_summer12_ttjets_1l'),
        ####(base, 'job_summer12_ttjets_2l'),

        #(base, 'job_summer12_WgPhOlap'),
        #(base, 'job_summer12_WjetsPhOlap'),
        #(base, 'job_summer12_ggZZ_2l2l'),
        #(base, 'job_summer12_ggZZ_4l'),
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
        #(base, 'job_summer12_WWg'),
        #(base, 'job_summer12_WZZ'),
        #(base, 'job_summer12_WWW'),
        #(base, 'job_summer12_WWZ'),
        #(base, 'job_summer12_ttg'),
        #(base, 'job_summer12_t_s'),
        #(base, 'job_summer12_t_t'),
        #(base, 'job_summer12_t_tW'),
        #(base, 'job_summer12_tbar_s'),
        #(base, 'job_summer12_tbar_t'),
        #(base, 'job_summer12_tbar_tW'),
        #(base, 'job_summer12_ttW'),
        #(base, 'job_summer12_ttZ'),
        #(base, 'job_jfaulkne_WZA'),


        ###(base, 'job_summer12_diphoton_box_10to25'),
        ###(base, 'job_summer12_diphoton_box_250toInf'),
        ###(base, 'job_summer12_diphoton_box_25to250'),
        ###(base, 'job_summer12_ttinclusive'),
        ###(base, 'QCD_Pt-40_doubleEMEnriched'),
        ###(base, 'job_summer12_WgPt50-130'),
        ###(base, 'job_summer12_WgPt130'),
        ###(base, 'job_summer12_WgPt30-50'),
        ###(base, 'job_summer12_WgPt20-30'),
        ###(base, 'job_summer12_DiPhotonBorn_Pt-10To25'),
]

if options.batch :
    #--------------------
    # for batch submission
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --moduleArgs "%(moduleArgs)s"  --batch --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --exeName %(exename)s_%(job)s '

else :

    #--------------------
    # not batch
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --exeName %(exename)s  '
    
if options.resubmit :
    command_base += ' --resubmit '

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(input)s/%(job)s --filteredDS %(base)s/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'

top_configs = [
    {   
     'module'      : 'ConfFilter.py', 
     'args'        : {},
     'input_name'  : 'LepGammaNoPhIDNoTrigElOlapRm_2016_04_21',
     'output_name' : 'LepGammaNoPhIDExtraOlapRm_2016_05_03',
     'tag'         : 'muFinal'
    },
]


module = 'ConfFilter.py'
nFilesPerJob = 1
nProc = 6
exename='RunAnalysis'
treename='ggNtuplizer/EventTree'

if options.run :
    first_data = True
    first_mc = True
    for config in top_configs :

        for base, job in jobs_data :
            job_exename = '%s_Data' %(exename )

            module_arg = config['args']
            module_arg['isData'] = ' == True '

            module_str = '{ '
            for key, val in module_arg.iteritems() :
                if isinstance( val, basestring ) :
                    module_str += '\'%s\' : \'%s\',' %( key, val)
                else :
                    module_str += '\'%s\' : %s,' %( key, val)
            module_str += '}'

            command = command_base %{ 'base' : base, 'job' : job, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : config['output_name'], 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }

            if not first_data :
                command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first_data :
                first_data = False

        for base, job in jobs_mc :
            job_exename = '%s_MC' %(exename )

            module_arg = config['args']

            module_str = '{ '
            for key, val in module_arg.iteritems() :
                if isinstance( val, basestring ) :
                    module_str += '\'%s\' : \'%s\',' %( key, val)
                else :
                    module_str += '\'%s\' : %s,' %( key, val)

            module_str += '}'

            command = command_base %{ 'base' : base, 'job' : job, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : config['output_name'], 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }
            if not first_mc :
                command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first_mc :
                first_mc = False

if options.check :
    for config in top_configs :
    
        for base, job in jobs_data :
    
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'input' : config['input_name'], 'treename' : treename}
            print command                                                                               
            os.system(command)                                                                          
                                                                                                        
        for base, job in jobs_mc :                                                                      
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'input' : config['input_name'], 'treename' : treename}
            print command
            os.system(command)





