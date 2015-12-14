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
base_yurii = 'root://eoscms//eos/cms/store/user/ymaravin/MC/LLAA/'


jobs_data = [
        #(base, base_orig, 'job_muon_2012a_Jan22rereco'),
        #(base, base_orig, 'job_muon_2012b_Jan22rereco'),
        #(base, base_orig, 'job_muon_2012c_Jan22rereco'),
        #(base, base_orig, 'job_muon_2012d_Jan22rereco'),
        #(base, base_orig, 'job_electron_2012a_Jan22rereco'),
        #(base, base_orig, 'job_electron_2012b_Jan22rereco'),
        #(base, base_orig, 'job_electron_2012c_Jan2012rereco'),
        #(base, base_orig, 'job_electron_2012d_Jan22rereco'),
]
jobs_mc = [
        #(base, base_chris, 'job_NLO_WAA_FSR_PtG500MeV'),
        #(base, base_chris, 'job_NLO_WAA_ISR_PtG500MeV'),
        (base, base_yurii, 'llaa_nlo_ggNtuple' ),
        #base,  base_orig_dy, 'job_summer12_DYJetsToLL'),
        #(base, base_orig, 'job_summer12_Wg'),
        #(base, base_orig, 'job_summer12_Zg'),
        #(base, base_orig, 'job_summer12_Zgg'),
        #(base, base_orig, 'job_summer12_Wjets'),
        #(base, base_orig, 'job_summer12_ttjets_1l'),
        #(base, base_orig, 'job_summer12_ttjets_2l'),

        #(base, base_orig, 'job_summer12_ttg'),
        #(base, base_orig, 'job_summer12_WH_ZH_125'),
        #(base, base_orig, 'job_summer12_WWW'),
        #(base, base_orig, 'job_summer12_WWZ'),
        #(base, base_orig, 'job_summer12_WW_2l2nu'),
        #(base, base_orig, 'job_summer12_WWg'),
        #(base, base_orig, 'job_summer12_WZZ'),
        #(base, base_orig, 'job_summer12_ZZZ'),
        #(base, base_orig, 'job_summer12_ZZ_2e2mu'),
        #(base, base_orig, 'job_summer12_ZZ_2e2tau'),
        #(base, base_orig, 'job_summer12_ZZ_2l2nu'),
        #(base, base_orig, 'job_summer12_ZZ_2l2q'),
        #(base, base_orig, 'job_summer12_ZZ_2mu2tau'),
        #(base, base_orig, 'job_summer12_ZZ_2q2nu'),
        #(base, base_orig, 'job_summer12_ZZ_4e'),
        #(base, base_orig, 'job_summer12_ZZ_4mu'),
        #(base, base_orig, 'job_summer12_ZZ_4tau'),
        #(base, base_orig, 'job_summer12_ggZZ_2l2l'),
        #(base, base_orig, 'job_summer12_ggZZ_4l'),
        #(base, base_orig, 'job_summer12_t_s'),
        #(base, base_orig, 'job_summer12_t_t'),
        #(base, base_orig, 'job_summer12_t_tW'),
        #(base, base_orig, 'job_summer12_tbar_s'),
        #(base, base_orig, 'job_summer12_tbar_t'),
        #(base, base_orig, 'job_summer12_tbar_tW'),
        #(base, base_orig, 'job_summer12_ttW'),
        #(base, base_orig, 'job_summer12_ttZ'),
        #(base, base_orig, 'job_jfaulkne_WZA'),

        #(base, base_orig, 'job_summer12_diphoton_box_10to25'),
        #(base, base_orig, 'job_summer12_diphoton_box_250toInf'),
        #(base, base_orig, 'job_summer12_diphoton_box_25to250'),

        ##(base, 'job_summer12_ttinclusive'),
        ##(base, 'QCD_Pt-40_doubleEMEnriched'),
        ##(base, 'job_summer12_WgPt50-130'),
        ##(base, 'job_summer12_WgPt130'),
        ##(base, 'job_summer12_WgPt30-50'),
        ##(base, 'job_summer12_WgPt20-30'),
        ##(base, 'job_summer12_DiPhotonBorn_Pt-10To25'),
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
    # 'args'        : {'functions' : 'vary_egamma_scale_dn' },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMediumPhotonIDSoftLepEGammaEScaleDN_2015_12_09',
    # 'tag'         : 'elFinalEGDN'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_egamma_scale_up' },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMediumPhotonIDSoftLepEGammaEScaleUP_2015_12_09',
    # 'tag'         : 'muFinalEGUP'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_egamma_scale_dn' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMediumPhotonIDSoftLepEGammaEScaleDN_2015_12_09',
    # 'tag'         : 'muFinalEGDN'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_egamma_scale_up' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMediumPhotonIDSoftLepEGammaEScaleUP_2015_12_09',
    # 'tag'         : 'muFinalEGUP'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_muon_scale_up' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMediumPhotonIDSoftLepMuonScaleUP_2015_12_09',
    # 'tag'         : 'muFinalMUUP'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_muon_scale_dn' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMediumPhotonIDSoftLepMuonScaleDN_2015_12_09',
    # 'tag'         : 'muFinalMUDN'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_met_uncert' },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'tag'         : 'muFinalMET'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_met_uncert' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'tag'         : 'elFinalMET'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : '' },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMediumPhotonIDSoftLepNOMINAL_2015_12_09',
    # 'tag'         : 'muFinalMET'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : '' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMediumPhotonIDSoftLepNOMINAL_2015_12_09',
    # 'tag'         : 'elFinalMET'
    #},
    ##---------------------------------------
    ## LepLepGammaGamma
    ##---------------------------------------
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_egamma_scale_dn' },
    # 'input_name'  : 'LepLepGammaGammaElMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaElMediumPhotonIDSoftLepEGammaEScaleDN_2015_12_09',
    # 'tag'         : 'elFinalEGDN'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_egamma_scale_up' },
    # 'input_name'  : 'LepLepGammaGammaElMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaElMediumPhotonIDSoftLepEGammaEScaleUP_2015_12_09',
    # 'tag'         : 'muFinalEGUP'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_egamma_scale_dn' },
    # 'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuMediumPhotonIDSoftLepEGammaEScaleDN_2015_12_09',
    # 'tag'         : 'muFinalEGDN'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_egamma_scale_up' },
    # 'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuMediumPhotonIDSoftLepEGammaEScaleUP_2015_12_09',
    # 'tag'         : 'muFinalEGUP'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_muon_scale_up' },
    # 'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuMediumPhotonIDSoftLepMuonScaleUP_2015_12_09',
    # 'tag'         : 'muFinalMUUP'
    #},
    #{   
    # 'module'      : 'Conf.py', 
    # 'args'        : {'functions' : 'vary_muon_scale_dn' },
    # 'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuMediumPhotonIDSoftLepMuonScaleDN_2015_12_09',
    # 'tag'         : 'muFinalMUDN'
    #},
    {   
     'module'      : 'Conf.py', 
     'args'        : {'functions' : '' },
     'input_name'  : 'LepLepGammaGammaElMediumPhotonIDSoftLep_2015_12_09',
     'output_name' : 'LepLepGammaGammaElMediumPhotonIDSoftLepNOMINAL_2015_12_09',
     'tag'         : 'elNom'
    },
    {   
     'module'      : 'Conf.py', 
     'args'        : {'functions' : '' },
     'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
     'output_name' : 'LepLepGammaGammaMuMediumPhotonIDSoftLepNOMINAL_2015_12_09',
     'tag'         : 'muNom'
    },
]

if options.run :
    for config in top_configs :
        first = True
        for base, base_orig, job in jobs_data :
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
                output = '%s/%s/%s' %(base,config['output_name'],job)
            else :
                output = '%s/%s/%s%s' %(base, config['input_name'], job, config['output_tag'])
            

            command = command_base %{ 'base' : base, 'job' : job, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : output, 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }

            if not first :
                command += ' --noCompileWithCheck '
            print command
            os.system(command)
            if first :
                first = False

        first = True
        for base, base_orig, job in jobs_mc :
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
                output = '%s/%s/%s' %(base,config['output_name'],job)
            else :
                output = '%s/%s/%s%s' %(base, config['input_name'], job, config['output_tag'])
            

            command = command_base %{ 'base' : base, 'job' : job, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : output, 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }
            if not first :
                command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first :
                first = False


