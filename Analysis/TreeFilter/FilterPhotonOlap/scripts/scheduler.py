import os

from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument( '--run', dest='run', default=False, action='store_true', help='Run filtering' )
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--batch', dest='batch', default=False, action='store_true', help='Run on batch, not locally ' )
options = p.parse_args()

if not options.run and not options.check :
    options.run = True

#base = '/eos/cms/store/user/jkunkle/Wgamgam/OutputS2TestNoPhJetOlap_2013_11_03'
#base = '/eos/cms/store/user/jkunkle/Wgamgam/RecoOutputOnlyDYNoTrigFilt_2014_02_03'
#base = '/eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2013_12_07'
#base = '/eos/cms/store/user/jkunkle/Wgamgam/GammaGammaMediumNoEleVetoNoEleIDOlapWithTrig_2014_07_31/'
#base_tmp = '/tmp/tEST/RecoOutputTESTNoCorr_2014_02_05/'
#base = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/'
base = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/'

# ----------------------------
# The suffix that appears on the 
# end of the output jobs
# ----------------------------

suffix='PhOlap'
#suffix='2PhFilt'

jobs = [
        (base, 'job_summer12_DYJetsToLL_s10'),
        #(base, 'job_summer12_Wjets'),
        #(base, 'job_summer12_ttjets_1l'),
        #(base, 'job_summer12_ttjets_2l'),

        #(base, 'job_summer12_Wg'),

        #(base, 'job_summer12_Zg'),
        #(base, 'job_summer12_ZgWithSF'),

        #(base, 'job_summer12_Zgg'),
        #(base, 'job_summer12_WgPt20-30'),
        #(base, 'job_summer12_WgPt30-50'),
        #(base, 'job_summer12_WgPt50-130'),
        #(base, 'job_summer12_WgPt130'),
        #(base, 'job_summer12_WW_2l2nu'),
        #(base, 'job_summer12_DiPhotonBorn_Pt-10To25'),
        #(base, 'job_summer12_WH_ZH_125'),
        #(base, 'job_summer12_WZ_3lnu'),
        #(base, 'job_summer12_ggZZ_2l2l'),
        #(base, 'job_summer12_ggZZ_4l'),

        #(base, 'job_summer12_WH_ZH_125'),
        #(base, 'job_summer12_t_s'),
        #(base, 'job_summer12_t_t'),
        #(base, 'job_summer12_t_tW'),
        #(base, 'job_summer12_tbar_s'),
        #(base, 'job_summer12_tbar_t'),
        #(base, 'job_summer12_tbar_tW'),
        #(base, 'job_summer12_WWW'),
        #(base, 'job_summer12_WWZ'),
        #(base, 'job_summer12_WWg'),
        #(base, 'job_summer12_WZZ'),
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
        #(base, 'job_summer12_ttg'),
        #(base, 'job_summer12_ttW'),
        #(base, 'job_summer12_ttZ'),
        #(base, 'job_jfaulkne_WZA'),

        #(base, 'job_summer12_WH_ZH_125WithSF'),
        #(base, 'job_summer12_t_sWithSF'),
        #(base, 'job_summer12_t_tWithSF'),
        #(base, 'job_summer12_t_tWWithSF'),
        #(base, 'job_summer12_tbar_sWithSF'),
        #(base, 'job_summer12_tbar_tWithSF'),
        #(base, 'job_summer12_tbar_tWWithSF'),
        #(base, 'job_summer12_WWWWithSF'),
        #(base, 'job_summer12_WWZWithSF'),
        #(base, 'job_summer12_WWgWithSF'),
        #(base, 'job_summer12_WZZWithSF'),
        #(base, 'job_summer12_ZZZWithSF'),
        #(base, 'job_summer12_ZZ_2e2muWithSF'),
        #(base, 'job_summer12_ZZ_2e2tauWithSF'),
        #(base, 'job_summer12_ZZ_2l2nuWithSF'),
        #(base, 'job_summer12_ZZ_2l2qWithSF'),
        #(base, 'job_summer12_ZZ_2mu2tauWithSF'),
        #(base, 'job_summer12_ZZ_2q2nuWithSF'),
        #(base, 'job_summer12_ZZ_4eWithSF'),
        #(base, 'job_summer12_ZZ_4muWithSF'),
        #(base, 'job_summer12_ZZ_4tauWithSF'),
        #(base, 'job_summer12_ttgWithSF'),
        #(base, 'job_summer12_ttWWithSF'),
        #(base, 'job_summer12_ttZWithSF'),
        #(base, 'job_summer12_WZ_3lnuWithSF'),
        #(base, 'job_summer12_WZ_2l2qWithSF'),
        #(base, 'job_jfaulkne_WZAWithSF'),

        #(base, 'job_summer12_Wgg_FSR'),
        #(base, 'job_summer12_WAA_ISR'),
        #(base, 'job_summer12_ttinclusive'),
        #(base, 'job_summer12_diphoton_box_10to25'),
        #(base, 'job_summer12_diphoton_box_250toInf'),
        #(base, 'job_summer12_diphoton_box_25to250'),
        ##(base_tmp, 'DYJetsToLLPhOlap' )
        ##(base_tmp, 'WjetsPhOlap' )
        ##(base_tmp, 'WgPhOlap' )
]

#module_mc   = 'ConfLepGammaFilter.py'
#module_data = 'ConfLepGammaFilter_Data.py'
#output_name = 'LepGamma_2013_11_04'
#sub_base = ['LepGammaGammaNoPhID_2015_11_09', 'LepGammaNoPhID_2015_11_09', 'LepLepGammaNoPhID_2015_11_09', 'LepGammaGammaFinalMuUnblindAllNoMtCut_2015_11_11', 'LepGammaGammaFinalElUnblindAllNoZCutNoMtCut_2015_11_11', 'LepGammaGammaNoPhIDInvPixSeedLead_2015_11_11', 'LepGammaGammaNoPhIDInvPixSeedSubl_2015_11_11', 'LepGammaGammaNoPhIDVetoPixSeedBoth_2015_11_11' ]
sub_base = [ 'LepGammaNoPhIDNoElOlapRm_2016_02_05']


check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(sub_base)s/%(job)s --filteredDS %(base)s/%(sub_base)s/%(job)s%(suffix)s --treeNameOrig ggNtuplizer/EventTree --histNameFilt ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'

if options.batch :
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(sub_base)s/%(job)s --fileKey tree.root --outputDir %(base)s/%(sub_base)s/%(job)s%(suffix)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --batch --nFilesPerJob 1'

else :
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(sub_base)s/%(job)s --fileKey tree.root --outputDir %(base)s/%(sub_base)s/%(job)s%(suffix)s --outputFile tree.root --treeName ggNtuplizer/EventTree --module scripts/%(module)s --nFilesPerJob 1 --nproc %(nproc)d '

if options.resubmit :
    command_base += ' --resubmit'

nproc=8
module = 'ConfFilter.py'
if options.run :
    for sb in sub_base :
    
        first = True
        for base, job in jobs :

            command = command_base %{ 'base': base , 'sub_base' : sb, 'job' : job, 'module' : module, 'nproc' : nproc, 'suffix': suffix}

            if not first :
                command += ' --noCompile'
            print command
            os.system(command)

            if first :
                first = False

if options.check :
    for sb in sub_base :
    
        for base, job in jobs :
    
            command = check_commands_base %{ 'base': base , 'sub_base' : sb, 'job' : job, 'module' : module, 'nproc' : nproc, 'suffix': suffix}
            print command
            os.system(command)

    

