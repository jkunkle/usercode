import os
from argparse import ArgumentParser

import scheduler_base
from scheduler_base import JobConf

p = ArgumentParser()
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--clean', dest='clean', default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--batch', dest='batch', default=False, action='store_true', help='Run on batch' )
options = p.parse_args()

if not options.check :
    options.run = True
else :
    options.run = False

options.local = ( not options.batch )

base = '/data/users/jkunkle/Resonances/'

jobs = [
        #JobConf(base, 'DoubleMuon'),
        #JobConf(base, 'DoubleEG'),
        JobConf(base, 'SingleMuon', isData=True),
        JobConf(base, 'SingleElectron', isData=True),
        #JobConf(base, 'SinglePhoton'),
        #JobConf(base, 'JetHT'),
        #JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        #JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                         ),
        JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                         ),
        JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        ##JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'),
        #JobConf(base, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        ),
        #JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'     ),
        JobConf(base, 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'     ),
        JobConf(base, 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'     ),
        JobConf(base, 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'     ),
        JobConf(base, 'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8' ),
        JobConf(base, 'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'     ),
        ####JobConf(base, 'TT_TuneCUETP8M1_13TeV-powheg-pythia8'                   ),
        ###JobConf(base, 'DiPhotonJetsBox_M40_80-Sherpa'                         ),
        ###JobConf(base, 'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa'                         ),
        ##JobConf(base, 'GJet_Pt-15ToInf_TuneCUETP8M1_13TeV-pythia8'                         ),
        #JobConf(base, 'QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8'                           ),
        ###JobConf(base, 'QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8'              ),
        ###JobConf(base, 'QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8'                         ),
        #JobConf(base, 'QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                ),
        #JobConf(base, 'QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8'                           ),
        #JobConf(base, 'QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8'              ),
        #JobConf(base, 'QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8'                         ),
        #JobConf(base, 'QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                ),
        #JobConf(base, 'QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8'              ),
        ##JobConf(base, 'QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                ),
        ##JobConf(base, 'QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8'                           ),
        ##JobConf(base, 'QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                ),
        ##JobConf(base, 'QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8'                           ),
        ##JobConf(base, 'QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8'               ),
        ##JobConf(base, 'QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8'                          ),
        ##JobConf(base, 'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1'   ),
        ##JobConf(base, 'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1' ),
        ##JobConf(base, 'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'     ),
        ##JobConf(base, 'WWTo2L2Nu_13TeV-powheg'                                             ),
        ##JobConf(base, 'WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                     ),
        ##JobConf(base, 'WZ_TuneCUETP8M1_13TeV-pythia8'                                      ),
        ##JobConf(base, 'ZZ_TuneCUETP8M1_13TeV-pythia8'                                      ),
        ##JobConf(base, 'MadGraphChargedResonance_WGToLNu_M200_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M300_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M400_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M500_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M600_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M700_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M800_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M1000_width0p01'                         ),
        #JobConf(base, 'MadGraphChargedResonance_WGToLNu_M1200_width0p01'                         ),
]

options.nFilesPerJob = 2
options.nproc = 6
options.treename='tupel/EventTree'
options.exename='RunAnalysis'
options.copyInputFiles=True
options.enableKeepFilter=True

input_base = 'RecoOutput_2017_01_01'
input_base_new = 'RecoOutput_2017_01_03'

configs = [ 
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_mumu', 'mu_pt' : ' > 30 ' },
    #    'input'  : 'RecoOutput_2016_12_23',
    #    'output' : base+'TESTLepLep_mumu_2016_12_28',
    #    'tag'    : 'mumu',
    #},
    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'make_final_mumu', 'mu_pt' : ' > 30 ' },
        'input'  : input_base,
        'output' : base+'LepLep_mumu_2017_01_09',
        'tag'    : 'mumu',
    },
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_elel', 'el_pt' : ' > 30 ' },
    #    'input'  : input_base,
    #    'output' : base+'LepLep_elel_2017_01_09',
    #    'tag'    : 'elel',
    #},
    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ' },
        'input'  : input_base,
        'output' : base+'LepGamma_mug_2017_01_09',
        'tag'    : 'mug',
    },
    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ' },
        'input'  : input_base,
        'output' : base+'LepGamma_elg_2017_01_09',
        'tag'    : 'elg',
    },
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_el', 'el_pt' : ' > 30 ', 'ph_id_cut' : 'None' },
    #    'input'  : input_base,
    #    'output' : base+'SingleLepNoPhID_el_2017_01_09',
    #    'tag'    : 'el',
    #},
    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'make_final_mu', 'mu_pt' : ' > 30 ', 'ph_id_cut' : 'None'  },
        'input'  : input_base,
        'output' : base+'SingleLepNoPhID_mu_2017_01_09',
        'tag'    : 'mu',
    },
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_elgjj', 'el_pt' : ' > 30 ' },
    #    'input'  : input_base_new,
    #    'output' : base+'LepGammaDiJet_elgjj_2017_01_03',
    #    'tag'    : 'elgjj',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_mugjj', 'mu_pt' : ' > 30 ' },
    #    'input'  : input_base_new,
    #    'output' : base+'LepGammaDiJet_mugjj_2017_01_03',
    #    'tag'    : 'mugjj',
    #},

]

scheduler_base.RunJobs( jobs, configs, options)

