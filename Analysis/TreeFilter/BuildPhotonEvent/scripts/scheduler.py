import os
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--run', dest='run', default=False, action='store_true', help='Run filtering' )
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local', dest='local', default=False, action='store_true', help='Run locally, not on batch' )
options = p.parse_args()

if not options.run and not options.check :
    options.run = True

out_prefix = '/data/users/jkunkle/RecoPhoton/'
base = r'/data/users/jkunkle/RecoPhoton/RecoOutput_2015_11_19/'
jobs_data = [

        (base, 'DoubleMuon'),
        (base, 'DoubleEG'),
        #(base, 'JetHT'),
        #(base, 'SinglePhoton'),
        #(base, 'SingleMuon'),
        #(base, 'SingleElectron'),

]

jobs_mc = [
        #(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'),
        #(base, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'),
        #(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'),
        #(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'),
        #(base, 'TT_TuneCUETP8M1_13TeV-powheg-pythia8' ),
        #(base, 'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1'   ),
        #(base, 'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1' ),
        #(base, 'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'     ),
        #(base, 'WWTo2L2Nu_13TeV-powheg'                                             ),
        #(base, 'WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                     ),
        #(base, 'WZ_TuneCUETP8M1_13TeV-pythia8'                                      ),
        #(base, 'ZZ_TuneCUETP8M1_13TeV-pythia8'                                      ),

        #(base, 'DiPhotonJetsBox_M40_80-Sherpa'             ),
        #(base, 'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa'             ),
        #(base, 'GJet_Pt-15ToInf_TuneCUETP8M1_13TeV-pythia8'             ),
        #(base, 'QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8'               ),
        #(base, 'QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8'  ),
        #(base, 'QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8'             ),
        #(base, 'QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8'    ),
        #(base, 'QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8'               ),
        #(base, 'QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8'  ),
        #(base, 'QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8'             ),
        #(base, 'QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8'    ),
        #(base, 'QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8'  ),
        #(base, 'QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8'    ),
        #(base, 'QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8'               ),
        #(base, 'QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8'    ),
        #(base, 'QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8'               ),
        #(base, 'QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8'   ),
        #(base, 'QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8'              ),
]

top_configs = [ 
                #{ 
                #  'module'      : 'Conf.py',
                #  'args_mc'     : '{ \'cut_nLep\' : \'> 0\', \'applyBlinding\' : True  }',
                #  'args_data'   : '{ \'cut_nLep\' : \'> 0\', \'applyBlinding\' : True } ',
                #  'output_name' : 'SingleLepNoPhIDNoTrig_2015_11_26',
                #  'tag'         : 'sl',
                #},
                { 
                  'module'      : 'Conf.py',
                  'args_mc'     : '{ \'cut_nLep\' : \'> 1\',\'cut_DiLepTrig\' : \' == True \', \'applyBlinding\' : True  }',
                  'args_data'   : '{ \'cut_nLep\' : \'> 1\',\'cut_DiLepTrig\' : \' == True \', \'applyBlinding\' : True } ',
                  'output_name' : 'LepLepNoPhID_2015_11_27',
                  'tag'         : 'll',
                },
                #{ 
                #  'module'      : 'Conf.py',
                #  'args_mc'     : '{ \'cut_nPh\' : \' > 0 \' , \'cut_nLep\' : \'> 1\',\'cut_DiLepTrig\' : \' == True \' }',
                #  'args_data'   : '{ \'cut_nPh\' : \' > 0 \' , \'cut_nLep\' : \'> 1\',\'cut_DiLepTrig\' : \' == True \' }',
                #  'output_name' : 'LepLepGammaMediumID_2015_11_17',
                #  'tag'         : 'llg',
                #},
                #{ 
                #  'module'      : 'Conf.py',
                #  'args_mc'     : '{ \'cut_nPh\' : \' > 0 \' , \'cut_nLep\' : \'> 1\' }',
                #  'args_data'   : '{ \'cut_nPh\' : \' > 0 \' , \'cut_nLep\' : \'> 1\' }',
                #  'output_name' : 'LepLepGammaMediumIDNoTrig_2015_11_17',
                #  'tag'         : 'llg',
                #},
                { 
                  'module'      : 'Conf.py',
                  'args_mc'     : '{ \'cut_nPh\' : \' > 0 \' }',
                  'args_data'   : '{ \'cut_nPh\' : \' > 0 \' }',
                  'output_name' : 'Photon_2015_11_23',
                  'tag'         : 'phot',
                },
]


if options.local :
    #--------------
    # not batch
    #--------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir %(out_prefix)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s --enableRemoveFilter'
else :
    #--------------
    # for batch
    #--------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir %(out_prefix)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --nFilesPerJob %(nFilesPerJob)d --condor --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s  --enableRemoveFilter '


if options.resubmit :
    command_base += ' --resubmit'

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(job)s --filteredDS %(out_prefix)s/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt tupel/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'


nFilesPerJob = 1
nproc=6
treename='tupel/EventTree'

if options.run :
    for config in top_configs :

        for base, job in jobs_data :
    
            command = command_base %{ 'base': base , 'job' : job, 'output' : config['output_name'], 'module' : config['module'], 'moduleArgs' : config['args_data'], 'tag' : config['tag'], 'nproc' : nproc, 'exe' : 'RunAnalysis%s%s' %(config['tag'], job), 'nFilesPerJob': nFilesPerJob, 'treename' : treename, 'out_prefix' : out_prefix}

            print command
            os.system(command)

        for base, job in jobs_mc :
            command = command_base %{ 'base': base , 'job' : job, 'output' : config['output_name'], 'module' : config['module'], 'moduleArgs' : config['args_mc'], 'tag' : config['tag'], 'nproc' : nproc, 'exe' : 'RunAnalysis%s%s' %(config['tag'], job), 'nFilesPerJob' : nFilesPerJob, 'treename' : treename, 'out_prefix' : out_prefix}
            print command
            os.system(command)


if options.check :
    for config in top_configs :
    
        for base, job in jobs_data :
    
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'treename' : treename, 'out_prefix' : out_prefix}
            print command
            os.system(command)
        
        for base, job in jobs_mc :
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'treename' : treename, 'out_prefix' : out_prefix}
            print command
            os.system(command)



