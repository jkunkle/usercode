import os
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--run'     , dest='run'     , default=False, action='store_true', help='Run filtering'              )
p.add_argument( '--check'   , dest='check'   , default=False, action='store_true', help='Run check of completion'    )
p.add_argument( '--clean'   , dest='clean'   , default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local'   , dest='local'   , default=True , action='store_true', help='Run locally'                )
options = p.parse_args()

if not options.run and not options.check :
    options.run = True

base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output'
base_orig_dy = 'root://eoscms//eos/cms/store/group/phys_smp/ggNtuples/mc'
base_orig = 'root://eoscms//eos/cms/store/group/phys_egamma/cmkuo/'
base_chris = 'root://eoscms//eos/cms/store/user/cranelli/WGamGam/NLO_ggNtuples/'
base_me = 'root://eoscms//eos/cms/store/user/jkunkle/Samples/ggNtuples'
base_yurii = 'root://eoscms//eos/cms/store/user/ymaravin/MC/LLAA'

class JobConf( ) :

    def __init__( self, base, pu_base, name, suffix='') :
        self.base = base
        self.pu_base = pu_base
        self.name = name
        self.suffix = suffix

jobs_data = [
        #JobConf(base, base_orig, 'job_muon_2012a_Jan22rereco'),
        #JobConf(base, base_orig, 'job_muon_2012b_Jan22rereco'),
        #JobConf(base, base_orig, 'job_muon_2012c_Jan22rereco'),
        #JobConf(base, base_orig, 'job_muon_2012d_Jan22rereco'),
        #JobConf(base, base_orig, 'job_electron_2012a_Jan22rereco'),
        #JobConf(base, base_orig, 'job_electron_2012b_Jan22rereco'),
        #JobConf(base, base_orig, 'job_electron_2012c_Jan2012rereco'),
        #JobConf(base, base_orig, 'job_electron_2012d_Jan22rereco'),
]
jobs_mc = [
        #JobConf(base, base_chris, 'job_NLO_WAA_FSR'),
        #JobConf(base, base_chris, 'job_NLO_WAA_ISR'),
        #JobConf(base, base_chris, 'job_NLO_WAA_ISR_PtG500MeV'),
        #JobConf(base, base_chris, 'job_NLO_WAA_ISR_PtG500MeV'),
        JobConf(base, base_chris, 'job_LNuAA_LT_Reweight'),
        ##JobConf(base, base_me, 'job_summer12_Zgg'),
        #JobConf(base, base_yurii, 'llaa_nlo_ggNtuple'),

        ##JobConf(base,  base_orig_dy, 'job_summer12_DYJetsToLL'),
        #JobConf(base,  base_orig_dy, 'job_summer12_DYJetsToLL', 'PhOlap'),
        ##JobConf(base, base_orig, 'job_summer12_Wg'),
        ##JobConf(base, base_orig, 'job_summer12_Wg', 'PhOlap'),
        #JobConf(base, base_orig, 'job_summer12_Zg'),
        ##JobConf(base, base_orig, 'job_summer12_Zg'),
        ##JobConf(base, base_orig, 'job_summer12_Wjets'),
        ##JobConf(base, base_orig, 'job_summer12_ttjets_1l'),
        ##JobConf(base, base_orig, 'job_summer12_ttjets_2l'),
        ##JobConf(base, base_orig, 'job_summer12_ttjets_1l', 'PhOlap'),
        ##JobConf(base, base_orig, 'job_summer12_ttjets_2l', 'PhOlap'),

        #JobConf(base, base_orig, 'job_summer12_ttg'),
        #JobConf(base, base_orig, 'job_summer12_WH_ZH_125'),
        #JobConf(base, base_orig, 'job_summer12_WWW'),
        #JobConf(base, base_orig, 'job_summer12_WWZ'),
        #JobConf(base, base_orig, 'job_summer12_WW_2l2nu'),
        #JobConf(base, base_orig, 'job_summer12_WWg'),
        #JobConf(base, base_orig, 'job_summer12_WZZ'),
        #JobConf(base, base_orig, 'job_summer12_ZZZ'),
        #JobConf(base, base_orig, 'job_summer12_ZZ_2e2mu'),
        #JobConf(base, base_orig, 'job_summer12_ZZ_2e2tau'),
        #JobConf(base, base_orig, 'job_summer12_ZZ_2l2nu'),
        #JobConf(base, base_orig, 'job_summer12_ZZ_2l2q'),
        #JobConf(base, base_orig, 'job_summer12_ZZ_2mu2tau'),
        #JobConf(base, base_orig, 'job_summer12_ZZ_2q2nu'),
        #JobConf(base, base_orig, 'job_summer12_ZZ_4e'),
        #JobConf(base, base_orig, 'job_summer12_ZZ_4mu'),
        #JobConf(base, base_orig, 'job_summer12_ZZ_4tau'),
        #JobConf(base, base_orig, 'job_summer12_ggZZ_2l2l'),
        #JobConf(base, base_orig, 'job_summer12_ggZZ_4l'),
        #JobConf(base, base_orig, 'job_summer12_t_s'),
        #JobConf(base, base_orig, 'job_summer12_t_t'),
        #JobConf(base, base_orig, 'job_summer12_t_tW'),
        #JobConf(base, base_orig, 'job_summer12_tbar_s'),
        #JobConf(base, base_orig, 'job_summer12_tbar_t'),
        #JobConf(base, base_orig, 'job_summer12_tbar_tW'),
        #JobConf(base, base_orig, 'job_summer12_ttW'),
        #JobConf(base, base_orig, 'job_summer12_ttZ'),
        #JobConf(base, base_orig, 'job_jfaulkne_WZA'),

        #JobConf(base, base_orig, 'job_summer12_diphoton_box_10to25'),
        #JobConf(base, base_orig, 'job_summer12_diphoton_box_250toInf'),
        #JobConf(base, base_orig, 'job_summer12_diphoton_box_25to250'),

        ##JobConf(base, 'job_summer12_ttinclusive'),
        ##JobConf(base, 'QCD_Pt-40_doubleEMEnriched'),
        ##JobConf(base, 'job_summer12_WgPt50-130'),
        ##JobConf(base, 'job_summer12_WgPt130'),
        ##JobConf(base, 'job_summer12_WgPt30-50'),
        ##JobConf(base, 'job_summer12_WgPt20-30'),
        ##JobConf(base, 'job_summer12_DiPhotonBorn_Pt-10To25'),
]

if options.local :
    #--------------------
    # not batch
    #--------------------
    #command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --exeName %(exename)s --moduleArgs "%(moduleArgs)s" '
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(output)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --exeName %(exename)s --moduleArgs "%(moduleArgs)s" '
    
else :
    #--------------------
    # for batch submission
    #--------------------
    #command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --batch --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --exeName %(exename)s_%(job)s  --moduleArgs "%(moduleArgs)s"'
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(output)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --batch --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --exeName %(exename)s_%(job)s  --moduleArgs "%(moduleArgs)s"'

if options.resubmit :
    command_base += ' --resubmit '

input = 'LepGammaGammaTest_2015_06_17'
output = 'TEST'

module = 'Conf.py'
nFilesPerJob = 1
nProc = 6
exename='RunAnalysis'
treename='ggNtuplizer/EventTree'

top_configs = [
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'get_muon_sf,get_electron_sf,get_photon_sf,get_pileup_sf' },
    # 'input_name'  : 'LepGammaGammaFinalElUnblindAll_2015_10_27',
    # 'output_tag'  : 'WithSF',
    # 'tag'         : 'muFinalSF'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'get_muon_sf,get_electron_sf,get_photon_sf,get_pileup_sf' },
    # 'input_name'  : 'LepGammaGammaFinalMuUnblindAll_2015_10_27',
    # 'output_tag'  : 'WithSF',
    # 'tag'         : 'elFinalSF'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'get_muon_sf,get_electron_sf,get_photon_sf,get_pileup_sf' },
    # 'input_name'  : 'LepLepGammaGammaFinalMuMuUnblindAll_2015_10_01',
    # 'output_tag'  : 'WithSF',
    # 'tag'         : 'mumuFinalSF'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'get_muon_sf,get_electron_sf,get_photon_sf,get_pileup_sf' },
    # 'input_name'  : 'LepLepGammaGammaFinalElElUnblindAll_2015_10_01',
    # 'output_tag'  : 'WithSF',
    # 'tag'         : 'elelFinalSF'
    #},
    {   
     'module'      : 'Conf.py', 
     'args'        : {'functions' : 'get_muon_sf,get_electron_sf,get_photon_sf,get_pileup_sf' },
     'input_name'  : 'LepGammaGammaFinalMuWithOlapUnblindAllNoMtCut_2015_10_01',
     'output_tag'  : 'WithSF',
     'tag'         : 'muFinalSF'
    },
    {   
     'module'      : 'Conf.py', 
     'args'        : {'functions' : 'get_muon_sf,get_electron_sf,get_photon_sf,get_pileup_sf' },
     'input_name'  : 'LepGammaGammaFinalElUnblindAllWithOlapNoZCutNoMtCut_2015_10_01',
     'output_tag'  : 'WithSF',
     'tag'         : 'elFinalSF'
    },
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'get_muon_sf,get_electron_sf,get_photon_sf,get_pileup_sf,vary_met_uncert' },
    # 'input_name'  : 'LepGammaGammaFinalElLowPtLoose_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'tag'         : 'xeluFinalMET'
    #},
]

if options.run :
    for config in top_configs :
        first = True
        for job_conf in jobs_data :
            base      = job_conf.base
            base_orig = job_conf.pu_base
            job       = job_conf.name
            suffix    = job_conf.suffix

            if options.local :
                job_exename = exename+'Data'
            else :
                job_exename = exename

            module_arg = config['args']
            module_arg['isData'] = ' == True '

            module_str = '{ '
            for key, val in module_arg.iteritems() :
                module_str += '\'%s\' : \'%s\',' %( key, val)
            module_str += '}'

            if 'output_name' in config :
                output = '%s/%s/%s%s' %(base,config['output_name'],job, suffix)
            else :
                output = '%s/%s/%s%s%s' %(base, config['input_name'], job, suffix,config['output_tag'])
            

            command = command_base %{ 'base' : base, 'job' : job+suffix, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : output, 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }

            if not first :
                command += ' --noCompileWithCheck '
            print command
            os.system(command)
            if first :
                first = False

        first = True
        for job_conf in jobs_mc :

            base      = job_conf.base
            base_orig = job_conf.pu_base
            job       = job_conf.name
            suffix    = job_conf.suffix

            if options.local :
                job_exename = exename+'MC'
            else :
                job_exename = exename

            module_arg = config['args']

            module_str = '{ '
            for key, val in module_arg.iteritems() :
                module_str += '\'%s\' : \'%s\',' %( key, val)

            module_str += ' \'args\' : { \'PUDistMCFile\' : \'%s/%s.root\'  } ' %( base_orig, job) 
            module_str += '}'

            if 'output_name' in config :
                output = '%s/%s/%s%s' %(base,config['output_name'],job, suffix)
            else :
                output = '%s/%s/%s%s%s' %(base, config['input_name'], job, suffix, config['output_tag'])
            

            command = command_base %{ 'base' : base, 'job' : job+suffix, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : output, 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }
            if not first :
                command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first :
                first = False


