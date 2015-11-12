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

base_muon = '/eos/cms/store/user/abelloni/Wgamgam/FilteredSamplesDec13'
base_elec = '/eos/cms/store/user/jkunkle/Wgamgam/FilteredSamplesDec13'
base_data = '/eos/cms/store/group/phys_smp/ggNtuples/data'
base_mc2 = '/eos/cms/store/group/phys_smp/ggNtuples/mc'
base_mc = '/eos/cms/store/group/phys_egamma/cmkuo'
base_skim = '/eos/cms/store/group/phys_egamma/cmkuo/skim_gg'
base_me = '/eos/cms/store/user/jkunkle/Samples/ggNtuples'
base_jj = '/eos/cms/store/group/phys_egamma/kschen/'
base_nlo = '/eos/cms/store/user/cranelli/WGamGam/NLO_ggNtuples'
base_yurii = '/eos/cms/store/user/ymaravin/MC/LLAA/'

jobs = [
        #(base_data, 'job_muon_2012a_Jan22rereco', 50),
        #(base_data, 'job_muon_2012b_Jan22rereco', 100),
        #(base_data, 'job_muon_2012c_Jan22rereco', 200),
        #(base_data, 'job_muon_2012d_Jan22rereco', 200),
        #(base_data, 'job_electron_2012a_Jan22rereco', 100),
        #(base_data, 'job_electron_2012b_Jan22rereco', 200),
        #(base_data, 'job_electron_2012c_Jan2012rereco', 400),
        #(base_data, 'job_electron_2012d_Jan22rereco', 500),

        #(base_data, 'job_2muon_2012a_Jan22rereco', 50),
        #(base_data, 'job_2muon_2012b_Jan22rereco', 100),
        #(base_data, 'job_2muon_2012c_Jan22rereco', 100),
        #(base_data, 'job_2muon_2012d_Jan22rereco', 100),

        #(base_data, 'job_2electron_2012a_Jan22rereco', 50 ),
        #(base_data, 'job_2electron_2012b_Jan22rereco', 100 ),
        #(base_data, 'job_2electron_2012c_Jan22rereco', 100 ),
        #(base_data, 'job_2electron_2012d_Jan22rereco', 100 ),

        #(base_mc, 'job_summer12_DYJetsToLL_s10', 300 ),
        #(base_mc, 'job_summer12_Wg', 50),
        #(base_mc, 'job_summer12_ttjets_1l', 200),
        #(base_mc, 'job_summer12_ttjets_2l', 100),
        (base_mc, 'job_summer12_Wjets', 400),
        #(base_mc, 'job_summer12_Zg_s10', 200),

        #(base_nlo, 'job_NLO_WAA_ISR_PtG500MeV', 20),
        #(base_nlo, 'job_NLO_WAA_FSR_PtG500MeV', 20),
        #(base_yurii, 'llaa_nlo_ggNtuple', 10 ),
        #(base_mc, 'job_summer12_ttg', 20),
        #(base_mc, 'job_summer12_WH_ZH_125', 10),
        #(base_mc, 'job_summer12_WWW', 10),
        #(base_mc, 'job_summer12_WWZ', 10),
        #(base_mc, 'job_summer12_WW_2l2nu', 10),
        #(base_mc, 'job_summer12_WWg', 10),
        #(base_mc, 'job_summer12_WZZ', 10),
        #(base_mc, 'job_summer12_WZ_2l2q', 50),
        #(base_mc, 'job_summer12_WZ_3lnu', 10),
        #(base_mc, 'job_summer12_ZZZ', 10),
        #(base_mc, 'job_summer12_ZZ_2e2mu', 10),
        #(base_mc, 'job_summer12_ZZ_2e2tau', 10),
        #(base_mc, 'job_summer12_ZZ_2l2nu', 10),
        #(base_mc, 'job_summer12_ZZ_2l2q', 10),
        #(base_mc, 'job_summer12_ZZ_2mu2tau', 10),
        #(base_mc, 'job_summer12_ZZ_2q2nu', 10),
        #(base_mc, 'job_summer12_ZZ_4e', 10),
        #(base_mc, 'job_summer12_ZZ_4mu', 10),
        #(base_mc, 'job_summer12_ZZ_4tau', 10),
        #(base_mc, 'job_summer12_diphoton_box_10to25', 10),
        #(base_mc, 'job_summer12_diphoton_box_250toInf', 10),
        #(base_mc, 'job_summer12_diphoton_box_25to250', 10),
        #(base_mc, 'job_summer12_ggZZ_2l2l', 10),
        #(base_mc, 'job_summer12_ggZZ_4l', 10),
        #(base_mc, 'job_summer12_t_s', 20),
        #(base_mc, 'job_summer12_t_t', 20),
        #(base_mc, 'job_summer12_t_tW', 20),
        #(base_mc, 'job_summer12_tbar_s', 20),
        #(base_mc, 'job_summer12_tbar_t', 20),
        #(base_mc, 'job_summer12_tbar_tW', 20),
        #(base_mc, 'job_summer12_ttW', 20),
        #(base_mc, 'job_summer12_ttZ', 20),
        #(base_mc, 'job_jfaulkne_WZA', 20),

        #(base_mc2, 'job_summer12_DYJetsToLL', 300 ),
        #(base_me, 'job_summer12_Zgg', 5 ),
        #(base_nlo, 'job_NLO_WAA_ISR', 20),
        #(base_nlo, 'job_NLO_WAA_FSR', 20),
        #(base_mc, 'job_summer12_DiPhotonBorn_Pt-10To25', 10),
        #(base_me, 'job_summer12_WgPt50-130', 40),
        #(base_me, 'job_summer12_WgPt130', 40),
        #(base_me, 'job_summer12_WgPt30-50', 40),
        #(base_me, 'job_summer12_WgPt20-30', 40),
        #(base_me, 'job_jetmon_2012b_Jan22rereco', 100),
        #(base_me, 'job_jetmon_2012c_Jan22rereco', 100),
        #(base_me, 'job_jetmon_2012d_Jan22rereco', 100),

        #(base_mc, 'job_summer12_ttinclusive', 100),
        #(base_me, 'QCD_Pt-40_doubleEMEnriched', 20),

        #(base_me, 'job_mg2pythia8_Wgg_small', 1),


]

if options.local :
    #--------------------
    # not batch
    #--------------------
    command_base = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Temp_outputs/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --enableKeepFilter --confFileName %(job)s.txt --nsplit %(nsplit)d --nproc %(nproc)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --exeName %(exename)s_%(job)s --moduleArgs "{ \'sampleFile\' : \'root://eoscms/%(base)s/%(job)s.root\'}"'
    
else :
    #--------------------
    # for batch submission
    #--------------------
    command_base = 'python scripts/filter.py  --files root://eoscms/%(base)s/%(job)s.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Temp_outputs/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --module scripts/%(module)s --enableKeepFilter --batch --confFileName %(job)s.txt --nsplit %(nsplit)d --storagePath /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --exeName %(exename)s_%(job)s --moduleArgs "{ \'sampleFile\' : \'root://eoscms/%(base)s/%(job)s.root\'}"'

if options.resubmit :
    command_base += ' --resubmit '

clean_command_base = ' python ../../Util/scripts/clean_conf_files.py --path /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s '

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s --filteredDS /eos/cms/store/user/jkunkle/Wgamgam/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt ggNtuplizer/filter --fileKeyOrig %(job)s.root --fileKeyFilt tree.root'

#module = 'ConfWgamgamReco.py'
#module = 'ConfWgamgamRecoJetTrig.py'
module = 'ConfWgamgamReco.py'
#output = 'RecoOutput_2014_12_05'
#output = 'RecoOutputDiMuon_2014_11_27'
#output = 'LepGammaNoEleVetoNewVar_2014_05_02'
output = 'RecoOutput_2015_11_04'

nFilesPerJob = 1
nProc = 6
exename='RunAnalysisMC'
treename='ggNtuplizer/EventTree'

if options.run :
    for base, job, nsplit in jobs :
        command = command_base %{ 'base' : base, 'job' : job, 'nfiles' : nFilesPerJob, 'output' : output, 'nsplit': nsplit, 'nproc' : nProc, 'exename' : exename, 'treename' : treename, 'module' : module }
        print command
        os.system(command)

if options.check :
    for base, job, nsplit in jobs :
        command = check_commands_base%{ 'base' : base, 'job' : job, 'output' : output,  'treename' : treename}
        print command
        os.system(command)

if options.clean :
    for base, job, nsplit in jobs :
        command = clean_command_base %{'job' : job, 'output' : output}
        print command
        os.system(command)
