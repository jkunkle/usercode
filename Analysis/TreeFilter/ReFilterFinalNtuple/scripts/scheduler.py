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


jobs_data = [
        #(base, 'job_muon_2012a_Jan22rereco'),
        #(base, 'job_muon_2012b_Jan22rereco'),
        #(base, 'job_muon_2012c_Jan22rereco'),
        #(base, 'job_muon_2012d_Jan22rereco'),
        #(base, 'job_electron_2012a_Jan22rereco'),
        #(base, 'job_electron_2012b_Jan22rereco'),
        #(base, 'job_electron_2012c_Jan2012rereco'),
        #(base, 'job_electron_2012d_Jan22rereco'),
        (base, 'job_2muon_2012a_Jan22rereco'),
        (base, 'job_2muon_2012b_Jan22rereco'),
        (base, 'job_2muon_2012c_Jan22rereco'),
        (base, 'job_2muon_2012d_Jan22rereco'),
        (base, 'job_2electron_2012a_Jan22rereco'),
        (base, 'job_2electron_2012b_Jan22rereco'),
        (base, 'job_2electron_2012c_Jan22rereco'),
        (base, 'job_2electron_2012d_Jan22rereco'),
]
jobs_mc = [
        (base, 'job_NLO_WAA_FSR'),
        (base, 'job_NLO_WAA_ISR'),
        (base, 'job_summer12_Wgg_FSR'),
        (base, 'job_summer12_WAA_ISR'),
        (base, 'job_summer12_Zgg'),
        (base, 'job_summer12_DYJetsToLL'),
        (base, 'job_summer12_Wg'),
        (base, 'job_summer12_Zg'),
        (base, 'job_summer12_Wjets'),
        (base, 'job_summer12_ttjets_1lPhOlap'),
        (base, 'job_summer12_ttjets_2lPhOlap'),
        (base, 'job_summer12_WH_ZH_125'),
        (base, 'job_summer12_WW_2l2nu'),
        (base, 'job_summer12_WZ_2l2q'),
        (base, 'job_summer12_WZ_3lnu'),

        (base, 'job_summer12_DYJetsToLLPhOlap'),
        (base, 'job_summer12_WgPhOlap'),
        (base, 'job_summer12_WjetsPhOlap'),
        (base, 'job_summer12_ggZZ_2l2l'),
        (base, 'job_summer12_ggZZ_4l'),
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
        (base, 'job_summer12_WWg'),
        (base, 'job_summer12_WZZ'),
        (base, 'job_summer12_WWW'),
        (base, 'job_summer12_WWZ'),
        (base, 'job_summer12_ttg'),
        (base, 'job_summer12_t_s'),
        (base, 'job_summer12_t_t'),
        (base, 'job_summer12_t_tW'),
        (base, 'job_summer12_tbar_s'),
        (base, 'job_summer12_tbar_t'),
        (base, 'job_summer12_tbar_tW'),
        (base, 'job_summer12_ttW'),
        (base, 'job_summer12_ttZ'),
        (base, 'job_jfaulkne_WZA'),


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

if options.local :
    #--------------------
    # not batch
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --exeName %(exename)s  '
    
else :
    #--------------------
    # for batch submission
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --moduleArgs "%(moduleArgs)s"  --batch --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --exeName %(exename)s_%(job)s '

if options.resubmit :
    command_base += ' --resubmit '

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(input)s/%(job)s --filteredDS /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'

top_configs = [
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mtcut' : ' > 40 '},
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepGammaGammaFinalMuUnblindAll_2015_07_16',
    # 'tag'         : 'muFinal'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mtcut' : ' > 40 '},
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepGammaGammaFinalElUnblindAll_2015_07_16',
    # 'tag'         : 'elFinal'
    #},
    {   
     'module'      : 'ConfFilter.py', 
     'args'        : {'function' : 'make_final_mumu' },
     'input_name'  : 'LepLepGammaGammaNoPhID_2015_07_16',
     'output_name' : 'LepLepGammaGammaFinalMuMuUnblindForCutflow_2015_07_16',
     'tag'         : 'muFinal'
    },
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_elel' },
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepLepGammaGammaFinalElElUnblindAllNoPix_2015_07_13',
    # 'tag'         : 'elFinal'
    #},
    #{
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_looseID_bothEleVeto', 'blind_pt' : 'None'},
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepLepGammaGammaNoPhIDVetoPixSeedBoth_2015_07_16',
    # 'tag'         : 'vetoBoth'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_looseID_invEleVetoLead', 'blind_pt' : 'None'},
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepLepGammaGammaNoPhIDInvPixSeedLead_2015_07_16',
    # 'tag'         : 'invLead'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_looseID_invEleVetoSubl', 'blind_pt' : 'None'},
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LeplepGammaGammaNoPhIDInvPixSeedSubl_2015_07_16',
    # 'tag'         : 'invSubl'
    #},
    #{
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_looseID_bothEleVeto', 'blind_pt' : 'None'},
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepGammaGammaNoPhIDVetoPixSeedBoth_2015_07_16',
    # 'tag'         : 'vetoBoth'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_looseID_invEleVetoLead', 'blind_pt' : 'None'},
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepGammaGammaNoPhIDInvPixSeedLead_2015_07_16',
    # 'tag'         : 'invLead'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_looseID_invEleVetoSubl', 'blind_pt' : 'None'},
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepGammaGammaNoPhIDInvPixSeedSubl_2015_07_16',
    # 'tag'         : 'invSubl'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mtcut' : ' > 0 ', 'zmasscr' : True },
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_04_11',
    # 'output_name' : 'LepGammaGammaFinalElZCR_2015_07_02',
    # 'tag'         : 'elFinalInvPixLead'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mtcut' : ' > 0 ', 'nozmass' : True , 'invpixsubl' : True },
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepGammaGammaFinalElNoZCutInvPixSubl_2015_07_16',
    # 'tag'         : 'elFinalInvPixSubl'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mtcut' : ' > 0 ', 'nozmass' : True , 'invpixlead' : True },
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepGammaGammaFinalElNoZCutInvPixLead_2015_07_16',
    # 'tag'         : 'elFinalInvPixLead'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_elel', 'invpixsubl' : True },
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepLepGammaGammaFinalElInvPixSubl_2015_07_16',
    # 'tag'         : 'elFinalInvPixSubl'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_elel', 'invpixlead' : True },
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepLepGammaGammaFinalElInvPixLead_2015_07_16',
    # 'tag'         : 'elFinalInvPixLead'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mumu', 'invpixsubl' : True },
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepLepGammaGammaFinalMuInvPixSubl_2015_07_16',
    # 'tag'         : 'elFinalInvPixSubl'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mumu', 'invpixlead' : True },
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_07_16',
    # 'output_name' : 'LepLepGammaGammaFinalMuInvPixLead_2015_07_16',
    # 'tag'         : 'elFinalInvPixLead'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertMuonUP'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertMuonUPFinal_2015_06_29',
    # 'tag'         : 'muFinalMETMUUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertMuonDN'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertMuonDNFinal_2015_06_29',
    # 'tag'         : 'muFinalMETMUDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertEMUP'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertEMUPFinal_2015_06_29',
    # 'tag'         : 'muFinalMETEMUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertEMDN'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertEMDNFinal_2015_06_29',
    # 'tag'         : 'muFinalMETEMDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertJESUP'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertJESUPFinal_2015_06_29',
    # 'tag'         : 'muFinalMETJESUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertJESDN'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertJESDNFinal_2015_06_29',
    # 'tag'         : 'muFinalMETJESDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertJERUP'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertJERUPFinal_2015_06_29',
    # 'tag'         : 'muFinalMETJERUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertJERDN'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertJERDNFinal_2015_06_29',
    # 'tag'         : 'muFinalMETJERDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertUnClusUP'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertUnClusUPFinal_2015_06_29',
    # 'tag'         : 'muFinalMETUnClusUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertUnClusDN'},
    # 'input_name'  : 'LepGammaGammaFinalMuMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMetUncertUnClusDNFinal_2015_06_29',
    # 'tag'         : 'muFinalMETUnClusDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertMuonUP'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertMuonUPFinal_2015_06_29',
    # 'tag'         : 'elFinalMETMUUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertMuonDN'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertMuonDNFinal_2015_06_29',
    # 'tag'         : 'elFinalMETMUDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertEMUP'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertEMUPFinal_2015_06_29',
    # 'tag'         : 'elFinalMETEMUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertEMDN'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertEMDNFinal_2015_06_29',
    # 'tag'         : 'elFinalMETEMDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertJESUP'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertJESUPFinal_2015_06_29',
    # 'tag'         : 'elFinalMETJESUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertJESDN'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertJESDNFinal_2015_06_29',
    # 'tag'         : 'elFinalMETJESDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertJERUP'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertJERUPFinal_2015_06_29',
    # 'tag'         : 'elFinalMETJERUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertJERDN'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertJERDNFinal_2015_06_29',
    # 'tag'         : 'elFinalMETJERDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertUnClusUP'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertUnClusUPFinal_2015_06_29',
    # 'tag'         : 'elFinalMETUnClusUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_metUncertUnClusDN'},
    # 'input_name'  : 'LepGammaGammaFinalElMETUncert_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMetUncertUnClusDNFinal_2015_06_29',
    # 'tag'         : 'elFinalMETUnClusDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_met'},
    # 'input_name'  : 'LepGammaGammaFinalMuEGammaEScaleUP_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuEGammaEScaleUPFinal_2015_06_29',
    # 'tag'         : 'muFinalEGUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_met'},
    # 'input_name'  : 'LepGammaGammaFinalMuEGammaEScaleDN_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuEGammaEScaleDNFinal_2015_06_29',
    # 'tag'         : 'muFinalEGDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_met'},
    # 'input_name'  : 'LepGammaGammaFinalElEGammaEScaleUP_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElEGammaEScaleUPFinal_2015_06_29',
    # 'tag'         : 'elFinalEGUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_met'},
    # 'input_name'  : 'LepGammaGammaFinalElEGammaEScaleDN_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElEGammaEScaleDNFinal_2015_06_29',
    # 'tag'         : 'elFinalEGDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_met'},
    # 'input_name'  : 'LepGammaGammaFinalMuMuonEScaleUP_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMuonEScaleUPFinal_2015_06_29',
    # 'tag'         : 'muFinalMUUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_met'},
    # 'input_name'  : 'LepGammaGammaFinalMuMuonEScaleDN_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalMuMuonEScaleDNFinal_2015_06_29',
    # 'tag'         : 'muFinalMUDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_met'},
    # 'input_name'  : 'LepGammaGammaFinalElMuonEScaleUP_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMuonEScaleUPFinal_2015_06_29',
    # 'tag'         : 'elFinalMUUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : False, 'mt_var' : 'mt_lep_met'},
    # 'input_name'  : 'LepGammaGammaFinalElMuonEScaleDN_2015_06_29',
    # 'output_name' : 'LepGammaGammaFinalElMuonEScaleDNFinal_2015_06_29',
    # 'tag'         : 'elFinalMUDN'
    #},
    ##{   
    ## 'module'      : 'ConfFilter.py', 
    ## 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : False},
    ## 'input_name'  : 'LepGammaGammaNoPhID_2015_04_11',
    ## 'output_name' : 'LepGammaGammaFinalMuUnblindAll_2015_04_12',
    ## 'tag'         : 'muFinal'
    ##},
    ##{   
    ## 'module'      : 'ConfFilter.py', 
    ## 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'loose' : True, 'notrig' : True},
    ## 'input_name'  : 'LepGammaGammaNoPhIDSoft_2015_06_29',
    ## 'output_name' : 'LepGammaGammaFinalElLowPtLoose_2015_06_29',
    ## 'tag'         : 'elFinal'
    ##},
    ##{   
    ## 'module'      : 'ConfFilter.py', 
    ## 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'loose' : True, 'notrig' : True},
    ## 'input_name'  : 'LepGammaGammaNoPhIDSoft_2015_06_29',
    ## 'output_name' : 'LepGammaGammaFinalMuLowPtLoose_2015_06_29',
    ## 'tag'         : 'muFinal'
    ##},
    ##{   
    ## 'module'      : 'ConfFilter.py', 
    ## 'args'        : {'function' : 'make_nominal_unblind_noEleVeto', 'blind_pt' : 'None'},
    ## 'input_name'  : 'LepGammaGammaNoPhID_2015_04_11',
    ## 'output_name' : 'LepGammaGammaNomUnblindAllNoEleVeto_2015_04_12',
    ## 'tag'         : 'nomUnblind'
    ##},
    ##{   
    ## 'module'      : 'ConfFilter.py', 
    ## 'args'        : {'function' : 'make_looseID_bothEleVeto', 'blind_pt' : 'None'},
    ## 'input_name'  : 'LepGammaGammaNoPhID_2015_04_11',
    ## 'output_name' : 'LepGammaGammaNoPhIDVetoPixSeedBoth_2015_04_12',
    ## 'tag'         : 'vetoBoth'
    ##},
    ##{   
    ## 'module'      : 'ConfFilter.py', 
    ## 'args'        : {'function' : 'make_looseID_invEleVetoLead', 'blind_pt' : 'None'},
    ## 'input_name'  : 'LepGammaGammaNoPhID_2015_04_11',
    ## 'output_name' : 'LepGammaGammaNoPhIDInvPixSeedLead_2015_04_12',
    ## 'tag'         : 'invLead'
    ##},
    ##{   
    ## 'module'      : 'ConfFilter.py', 
    ## 'args'        : {'function' : 'make_looseID_invEleVetoSubl', 'blind_pt' : 'None'},
    ## 'input_name'  : 'LepGammaGammaNoPhID_2015_04_11',
    ## 'output_name' : 'LepGammaGammaNoPhIDInvPixSeedSubl_2015_04_12',
    ## 'tag'         : 'invSubl'
    ##},
    ##{   
    ## 'module'      : 'ConfFilter.py', 
    ## 'args'        : {'function' : 'make_wgjj'},
    ## 'input_name'  : 'LepGammaNoPhID_2015_04_11',
    ## 'output_name' : 'LepGammaJJNoPhID_2015_06_25',
    ## 'tag'         : 'wgjj'
    ##},
    ##{   
    ## 'module'      : 'ConfFilter.py', 
    ## 'args'        : {'function' : 'make_zgjj'},
    ## 'input_name'  : 'LepLepGammaNoPhID_2015_04_11',
    ## 'output_name' : 'LepLepGammaJJNoPhID_2015_05_05',
    ## 'tag'         : 'zgjj'
    ##},
]


module = 'ConfFilter.py'
nFilesPerJob = 1
nProc = 6
exename='RunAnalysis'
treename='ggNtuplizer/EventTree'

if options.run :
    for config in top_configs :
        first = True

        for base, job in jobs_data :
            job_exename = '%s_%s_Data' %(exename, config['tag'] )

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

            if not first :
                command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first :
                first = False

        first = True
        for base, job in jobs_mc :
            job_exename = '%s_%s_MC' %(exename, config['tag'] )

            module_arg = config['args']

            module_str = '{ '
            for key, val in module_arg.iteritems() :
                if isinstance( val, basestring ) :
                    module_str += '\'%s\' : \'%s\',' %( key, val)
                else :
                    module_str += '\'%s\' : %s,' %( key, val)

            module_str += '}'

            command = command_base %{ 'base' : base, 'job' : job, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : config['output_name'], 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }
            if not first :
                command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first :
                first = False

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





