import os
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--run', dest='run', default=False, action='store_true', help='Run filtering' )
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--clean', dest='clean', default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local', dest='local', default=False, action='store_true', help='Run locally' )
p.add_argument( '--test', dest='test', default=False, action='store_true', help='Run a local test job' )
options = p.parse_args()

if not options.run and not options.check and not options.clean :
    options.run = True

class JobConf( ) :

    def __init__( self, *kwargs) :
        self.base = kwargs[0]
        self.version = kwargs[1]
        self.sample= kwargs[2]
        self.neg_weights =  kwargs[3]

#base = '/data/users/jkunkle/Baobabs/'
base = '/store/user/jkunkle/'
base_signal = '/data/users/jkunkle/Samples/Signal/'
version = 'Resonances_v1'
version_sig = 'Resonances_v2'

jobs = [
        #JobConf(base, version_sig, 'DoubleMuon', False ),
        #JobConf(base, version_sig, 'DoubleEG', False ),
        #JobConf(base, version_sig, 'SingleMuon', False ),
        #JobConf(base, version_sig, 'SingleElectron', False ),
        #JobConf(base, version_sig, 'SinglePhoton', False ),
        #JobConf(base, version_sig, 'JetHT', False ),
        JobConf(base, version, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         , False ),
        JobConf(base, version_sig, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         , False ),
        #JobConf(base, version, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         , False ),
        #JobConf(base, version, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         , False ),
        #JobConf(base, version, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', True),
        #JobConf(base, version, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        , True),
        #JobConf(base, version, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        , True),
        #JobConf(base, version, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'     , True),
        #JobConf(base, version, 'TT_TuneCUETP8M1_13TeV-powheg-pythia8'                   , False),
        #JobConf(base, version, 'DiPhotonJetsBox_M40_80-Sherpa'                         , False ),
        #JobConf(base, version, 'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa'                         , False ),
        #JobConf(base, version, 'GJet_Pt-15ToInf_TuneCUETP8M1_13TeV-pythia8'                         , False ),
        #JobConf(base, version, 'QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8'                           , False ),
        #JobConf(base, version, 'QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8'              , False ),
        #JobConf(base, version, 'QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8'                         , False ),
        #JobConf(base, version, 'QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                , False ),
        #JobConf(base, version, 'QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8'                           , False ),
        #JobConf(base, version, 'QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8'              , False ),
        #JobConf(base, version, 'QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8'                         , False ),
        #JobConf(base, version, 'QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                , False ),
        #JobConf(base, version, 'QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8'              , False ),
        #JobConf(base, version, 'QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                , False ),
        #JobConf(base, version, 'QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8'                           , False ),
        #JobConf(base, version, 'QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                , False ),
        #JobConf(base, version, 'QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8'                           , False ),
        #JobConf(base, version, 'QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8'               , False ),
        #JobConf(base, version, 'QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8'                          , False ),
        #JobConf(base, version, 'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1'   , False ),
        #JobConf(base, version, 'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1' , False ),
        #JobConf(base, version, 'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'     , False ),
        #JobConf(base, version, 'WWTo2L2Nu_13TeV-powheg'                                             , False ),
        #JobConf(base, version, 'WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                     , True  ),
        #JobConf(base, version, 'WZ_TuneCUETP8M1_13TeV-pythia8'                                      , False ),
        #JobConf(base, version, 'ZZ_TuneCUETP8M1_13TeV-pythia8'                                      , False ),
        #JobConf(base_signal, version_sig, 'ChargedResonance_WGToLNu_M2000_width0p01'                         , False ),
        #JobConf(base_signal, version_sig, 'ChargedResonance_WGToLNu_M2000_width20'                         , False ),
        #JobConf(base_signal, version_sig, 'ChargedResonance_WGToLNu_M2000_width10'                         , False ),
        #JobConf(base_signal, version_sig, 'ChargedResonance_WGToLNu_M2000_width5'                         , False ),
        #JobConf(base_signal, version_sig, 'ChargedResonance_WGToLNu_M400_width1'                         , False ),
        #JobConf(base_signal, version, 'ChargedResonance_WGToLNu_M400_width10'                         , False ),
]

#module = 'ConfPhotonReco.py'
module = 'ConfTruthPhotonReco.py'
output = 'RecoOutputTruth_2016_10_18'

nFilesPerJob = 1
nProc = 4
exename='RunAnalysis'
treename='tupel/EventTree'


if options.local :
    #--------------------
    # not batch
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s/%(version)s --outputDir /data/users/jkunkle/Resonances/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --enableKeepFilter --confFileName %(job)s.txt --nFilesPerJob 1 --nproc %(nproc)d --exeName %(exename)s_%(job)s --moduleArgs "%(module_args)s" '
    
elif options.test :
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s/%(version)s --outputDir /data/users/jkunkle/Resonances/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --enableKeepFilter --confFileName %(job)s.txt --nFilesPerJob 1 --nJobs 1  --exeName %(exename)s_%(job)s --moduleArgs "%(module_args)s" '

else :
    #--------------------
    # for batch submission
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s/%(version)s --outputDir /data/users/jkunkle/Resonances/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --enableKeepFilter --confFileName %(job)s.txt --nFilesPerJob 1 --exeName %(exename)s_%(job)s --condor  --moduleArgs "%(module_args)s" '

if options.resubmit :
    command_base += ' --resubmit '

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(job)s/%(version)s --filteredDS /data/users/jkunkle/Resonances/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt tupel/filter --fileKeyOrig ntuple --fileKeyFilt tree.root'

if options.run :
    for job in jobs :

        if job.neg_weights :
            weight_str = 'true'
        else :  
            weight_str = 'false'

        module_str = '{ '
        module_str += '\'ApplyNLOWeight\' : \'%s\',' %( weight_str)
        module_str += '}'

        command = command_base %{ 'base' : job.base, 'job' : job.sample, 'version' : job.version, 'nfiles' : nFilesPerJob, 'output' : output, 'nproc' : nProc, 'exename' : exename, 'treename' : treename, 'module' : module, 'module_args' : module_str }
        print command
        os.system(command)

if options.check :
    for job in jobs :
        command = check_commands_base%{ 'base' : job.base, 'job' : job.sample, 'version' : job.version, 'output' : output,  'treename' : treename}
        print command
        os.system(command)

