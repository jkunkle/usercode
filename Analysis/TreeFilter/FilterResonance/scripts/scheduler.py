import os
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--run', dest='run', default=False, action='store_true', help='Run filtering' )
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--clean', dest='clean', default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local', dest='local', default=False, action='store_true', help='Run locally' )
options = p.parse_args()

if not options.run and not options.check and not options.clean :
    options.run = True

class JobConf( ) :

    def __init__( self, *kwargs) :
        self.base = kwargs[0]
        self.sample= kwargs[1]

base = '/data/users/jkunkle/Resonances/RecoOutput_2016_08_28'

jobs = [
        #JobConf(base, 'DoubleMuon'),
        #JobConf(base, 'DoubleEG'),
        #JobConf(base, 'SingleMuon'),
        #JobConf(base, 'SingleElectron'),
        #JobConf(base, 'SinglePhoton'),
        #JobConf(base, 'JetHT'),
        JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        #JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        ##JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'),
        #JobConf(base, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        ),
        #JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        ),
        #JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'     ),
        #JobConf(base, 'TT_TuneCUETP8M1_13TeV-powheg-pythia8'                   ),
        #JobConf(base, 'DiPhotonJetsBox_M40_80-Sherpa'                         ),
        #JobConf(base, 'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa'                         ),
        #JobConf(base, 'GJet_Pt-15ToInf_TuneCUETP8M1_13TeV-pythia8'                         ),
        #JobConf(base, 'QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8'                           ),
        #JobConf(base, 'QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8'              ),
        #JobConf(base, 'QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8'                         ),
        #JobConf(base, 'QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                ),
        #JobConf(base, 'QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8'                           ),
        #JobConf(base, 'QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8'              ),
        #JobConf(base, 'QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8'                         ),
        #JobConf(base, 'QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                ),
        #JobConf(base, 'QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8'              ),
        #JobConf(base, 'QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                ),
        #JobConf(base, 'QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8'                           ),
        #JobConf(base, 'QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8'                ),
        #JobConf(base, 'QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8'                           ),
        #JobConf(base, 'QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8'               ),
        #JobConf(base, 'QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8'                          ),
        #JobConf(base, 'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1'   ),
        #JobConf(base, 'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1' ),
        #JobConf(base, 'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'     ),
        #JobConf(base, 'WWTo2L2Nu_13TeV-powheg'                                             ),
        #JobConf(base, 'WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                     ),
        #JobConf(base, 'WZ_TuneCUETP8M1_13TeV-pythia8'                                      ),
        #JobConf(base, 'ZZ_TuneCUETP8M1_13TeV-pythia8'                                      ),
        JobConf(base, 'ChargedResonance_WGToLNu_M2000_width0p01'                         ),
        JobConf(base, 'ChargedResonance_WGToLNu_M2000_width20'                         ),
        JobConf(base, 'ChargedResonance_WGToLNu_M2000_width10'                         ),
        JobConf(base, 'ChargedResonance_WGToLNu_M2000_width5'                         ),
        JobConf(base, 'ChargedResonance_WGToLNu_M400_width1'                         ),
        JobConf(base, 'ChargedResonance_WGToLNu_M400_width10'                         ),
]

if options.local :
    #--------------------
    # not batch
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --outputDir /data/users/jkunkle/FinalResonances/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --enableKeepFilter --confFileName %(job)s.txt --nFilesPerJob 1 --nproc %(nproc)d --exeName %(exename)s_%(job)s --moduleArgs "%(module_args)s" '
    
else :
    #--------------------
    # for batch submission
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --outputDir /data/users/jkunkle/FinalResonances/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --enableKeepFilter --confFileName %(job)s.txt --nFilesPerJob 1 --exeName %(exename)s_%(job)s --condor  --moduleArgs "%(module_args)s" '

if options.resubmit :
    command_base += ' --resubmit '

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(job)s --filteredDS /data/users/jkunkle/FinalResonances/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt tupel/filter --fileKeyOrig ntuple --fileKeyFilt tree.root'

#module = 'ConfWgamgamReco.py'
#module = 'ConfWgamgamRecoJetTrig.py'
module = 'Conf.py'
#output = 'RecoOutput_2014_12_05'
#output = 'RecoOutputDiMuon_2014_11_27'
#output = 'LepGammaNoEleVetoNewVar_2014_05_02'
output = 'FinalOutput_2016_10_18'

nFilesPerJob = 1
nProc = 6
exename='RunAnalysis'
treename='tupel/EventTree'

if options.run :
    for job in jobs :

        module_str = '{ '
        module_str += '}'

        command = command_base %{ 'base' : job.base, 'job' : job.sample, 'nfiles' : nFilesPerJob, 'output' : output, 'nproc' : nProc, 'exename' : exename, 'treename' : treename, 'module' : module, 'module_args' : module_str }
        print command
        os.system(command)

if options.check :
    for job in jobs :
        command = check_commands_base%{ 'base' : job.base, 'job' : job.sample, 'output' : output,  'treename' : treename}
        print command
        os.system(command)

