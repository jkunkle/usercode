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

#base = r'/eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2014_12_05'
base = r'/eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2015_04_05'
#base = r'/eos/cms/store/user/jkunkle/Wgamgam/RecoOutputNoTrig_2015_04_05'
#base = r'/eos/cms/store/user/jkunkle/Wgamgam/RecoOutputDiMuon_2014_11_27'
#base = r'/eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2014_10_30'
jobs_data = [
        (base, 'job_electron_2012a_Jan22rereco'),
        (base, 'job_electron_2012b_Jan22rereco'),
        (base, 'job_electron_2012c_Jan2012rereco'),
        (base, 'job_electron_2012d_Jan22rereco'),
        (base, 'job_muon_2012a_Jan22rereco'),
        (base, 'job_muon_2012b_Jan22rereco'),
        (base, 'job_muon_2012c_Jan22rereco'),
        (base, 'job_muon_2012d_Jan22rereco'),

        #(base, 'job_2muon_2012a_Jan22rereco'),
        #(base, 'job_2muon_2012b_Jan22rereco'),
        #(base, 'job_2muon_2012c_Jan22rereco'),
        #(base, 'job_2muon_2012d_Jan22rereco'),

        #(base, 'job_2photon_2012d_Jan22rereco_2of4'),
        #(base, 'job_2photon_2012d_Jan22rereco_3of4'),
        #(base, 'job_2photon_2012d_Jan22rereco_4of4'),
        #(base, 'job_2photon_2012d_Jan22rereco_5of5'),
        #(base, 'job_electron_2012a_Jan22rereco'),
        #(base, 'job_electron_2012b_Jan22rereco'),
        #(base, 'job_electron_2012c_Jan2012rereco'),
        #(base, 'job_electron_2012d_Jan22rereco'),
        #(base, 'job_fall13_photonRunB2012_1'),
        #(base, 'job_fall13_photonRunB2012_10'),
        #(base, 'job_fall13_photonRunB2012_11'),
        #(base, 'job_fall13_photonRunB2012_12'),
        #(base, 'job_fall13_photonRunB2012_13'),
        #(base, 'job_fall13_photonRunB2012_14'),
        #(base, 'job_fall13_photonRunB2012_15'),
        #(base, 'job_fall13_photonRunB2012_16'),
        #(base, 'job_fall13_photonRunB2012_17'),
        #(base, 'job_fall13_photonRunB2012_2'),
        #(base, 'job_fall13_photonRunB2012_3'),
        #(base, 'job_fall13_photonRunB2012_4'),
        #(base, 'job_fall13_photonRunB2012_5'),
        #(base, 'job_fall13_photonRunB2012_6'),
        #(base, 'job_fall13_photonRunB2012_7'),
        #(base, 'job_fall13_photonRunB2012_8'),
        #(base, 'job_fall13_photonRunB2012_9'),
        #(base, 'job_photon_2012a_Jan22rereco'),
        #(base, 'job_MultiJet_2012a_Jan22rereco'),
        #(base, 'job_jetmon_2012b_Jan22rereco'),
        #(base, 'job_jetmon_2012c_Jan22rereco'),
        #(base, 'job_jetmon_2012d_Jan22rereco'),
]

jobs_mc = [
        (base, 'job_summer12_DYJetsToLL'),
        (base, 'job_summer12_Zg'),
        (base, 'job_summer12_Wg'),
        (base, 'job_summer12_Wjets'),
        (base, 'job_summer12_ttjets_1l'),
        (base, 'job_summer12_ttjets_2l'),
        (base, 'job_summer12_Zgg'),
        (base, 'job_summer12_WAA_ISR'),
        (base, 'job_summer12_Wgg_FSR'),
        (base, 'job_summer12_ttg'),
        (base, 'job_summer12_WgPt130'),
        (base, 'job_summer12_WgPt50-130'),
        (base, 'job_summer12_WgPt30-50'),
        (base, 'job_summer12_WgPt20-30'),
        (base, 'job_summer12_DiPhotonBorn_Pt-10To25'),
        (base, 'job_summer12_WH_ZH_125'),
        (base, 'job_summer12_WWW'),
        (base, 'job_summer12_WWZ'),
        (base, 'job_summer12_WW_2l2nu'),
        (base, 'job_summer12_WWg'),
        (base, 'job_summer12_WZZ'),
        (base, 'job_summer12_WZ_3lnu'),
        (base, 'job_summer12_ZZZ'),
        (base, 'job_summer12_ZZ_2e2mu'),
        (base, 'job_summer12_ZZ_2e2tau'),
        (base, 'job_summer12_ZZ_2l2nu'),
        (base, 'job_summer12_ZZ_2l2q'),
        (base, 'job_summer12_ZZ_2mu2tau'),
        (base, 'job_summer12_ZZ_2q2nu'),
        (base, 'job_summer12_ZZ_4e'),
        (base, 'job_summer12_ZZ_4mu'),
        (base, 'job_summer12_ZZ_4tau'),
        (base, 'job_summer12_diphoton_box_10to25'),
        (base, 'job_summer12_diphoton_box_250toInf'),
        (base, 'job_summer12_diphoton_box_25to250'),
        (base, 'job_summer12_ggZZ_2l2l'),
        (base, 'job_summer12_ggZZ_4l'),
        (base, 'job_summer12_t_s'),
        (base, 'job_summer12_t_t'),
        (base, 'job_summer12_t_tW'),
        (base, 'job_summer12_tbar_s'),
        (base, 'job_summer12_tbar_t'),
        (base, 'job_summer12_tbar_tW'),
        (base, 'job_jfaulkne_WZA'),
        (base, 'job_summer12_ttZ'),
        (base, 'job_summer12_ttW'),
        (base, 'QCD_Pt-40_doubleEMEnriched')

        ##(base, 'job_summer12_ttinclusive'),
]

#module_mc   = 'ConfLepGammaFilter.py'
#module_data = 'ConfLepGammaFilter_Data.py'
#output_name = 'LepGamma_2013_11_04'

top_configs = [ 
                #{ 
                #  'module'      : 'ConfObjFilter.py',
                #  'args_mc'     : '{ \'cut_nLep\' : \' > 0 \' }',
                #  'args_data'   : '{ \'cut_nLep\' : \' > 0 \' }',
                #  'output_name' : 'SingleLeptonLoose_2015_04_11',
                #  'tag'         : 'singlLep',
                #},
                #{ 
                #  'module'      : 'ConfObjFilter.py',
                #  'args_mc'     : '{ \'cut_nLepTrigMatch\' : \' > 0 \', \'cut_nPh\' : \'> 1\' }',
                #  'args_data'   : '{ \'cut_nLepTrigMatch\' : \' > 0 \', \'cut_nPh\' : \'> 1\', \'isData\' : \' == True\' }',
                #  'output_name' : 'LepGammaGammaNoPhID_2015_04_11',
                #  'tag'         : 'lgg',
                #},
                #{ 
                #  'module'      : 'ConfObjFilter.py',
                #  'args_mc'     : '{ \'cut_nLepTrigMatch\' : \' > 0 \', \'cut_nPh\' : \'> 0\' }',
                #  'args_data'   : '{ \'cut_nLepTrigMatch\' : \' > 0 \', \'cut_nPh\' : \'> 0\', \'isData\' : \' == True\' }',
                #  'output_name' : 'LepGammaNoPhID_2015_04_11',
                #  'tag'         : 'lg',
                #},
                #{ 
                #  'module'      : 'ConfObjFilter.py',
                #  'args_mc'     : '{ \'cut_nLepTrigMatch\' : \' > 0 \', \'cut_nLep\' : \'> 1\', \'cut_nPh\' : \'> 0\' }',
                #  'args_data'   : '{ \'cut_nLepTrigMatch\' : \' > 0 \', \'cut_nLep\' : \'> 1\', \'cut_nPh\' : \'> 0\', \'isData\' : \' == True\' }',
                #  'output_name' : 'LepLepGammaNoPhID_2015_04_11',
                #  'tag'         : 'llg',
                #},
                { 
                  'module'      : 'ConfObjFilter.py',
                  'args_mc'     : '{ \'cut_nLep\' : \' > 0 \', \'cut_nPh\' : \'> 1\' }',
                  'args_data'   : '{ \'cut_nLep\' : \' > 0 \', \'cut_nPh\' : \'> 1\', \'isData\' : \' == True\' }',
                  'output_name' : 'LepGammaGammaNoPhIDLooseLep_2015_04_11',
                  'tag'         : 'lgg',
                },
                #{ 
                #  'module'      : 'ConfObjFilter.py',
                #  'args_mc'     : '{ \'cut_nLepTrigMatch\' : \' > 0 \', \'cut_nLep\' : \'> 1\', \'cut_m_leplep\' : \' > 110 \'}',
                #  'args_data'   : '{ \'cut_nLepTrigMatch\' : \' > 0 \', \'cut_nLep\' : \'> 1\', \'cut_m_leplep\' : \' > 110 \', \'isData\' : \' == True\' }',
                #  'output_name' : 'LepLepLoose_2015_04_08',
                #  'tag'         : 'll',
                #},
]


if options.local :
    #--------------
    # not batch
    #--------------
    command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s '
else :
    #--------------
    # for batch
    #--------------
    command_base = 'python scripts/filter.py  --filesDir root://eoscms/%(base)s/%(job)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --nFilesPerJob %(nFilesPerJob)d --batch --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s  '


if options.resubmit :
    command_base += ' --resubmit'

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(job)s --filteredDS /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'

#command_base = 'python scripts/filter.py  --filesDir %(base)s/%(job)s --fileKey tree.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --nFilesPerJob 5 --nproc %(nproc)d --confFileName %(tag)s_%(job)s.txt --exeName %(exe)s'

nFilesPerJob = 5
nproc=5
treename='ggNtuplizer/EventTree'

if options.run :
    for config in top_configs :
    
        for base, job in jobs_data :
    
            command = command_base %{ 'base': base , 'job' : job, 'output' : config['output_name'], 'module' : config['module'], 'moduleArgs' : config['args_data'], 'tag' : config['tag'], 'nproc' : nproc, 'exe' : 'RunAnalysis%s%s' %(config['tag'], job), 'nFilesPerJob': nFilesPerJob, 'treename' : treename}
            print command
            os.system(command)
        
        for base, job in jobs_mc :
            command = command_base %{ 'base': base , 'job' : job, 'output' : config['output_name'], 'module' : config['module'], 'moduleArgs' : config['args_mc'], 'tag' : config['tag'], 'nproc' : nproc, 'exe' : 'RunAnalysis%s%s' %(config['tag'], job), 'nFilesPerJob' : nFilesPerJob, 'treename' : treename}
            print command
            os.system(command)


if options.check :
    for config in top_configs :
    
        for base, job in jobs_data :
    
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'treename' : treename}
            print command
            os.system(command)
        
        for base, job in jobs_mc :
            command = check_commands_base%{ 'base': base , 'job' : job, 'output' : config['output_name'], 'treename' : treename}
            print command
            os.system(command)



