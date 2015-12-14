import os
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--run'     , dest='run'     , default=False, action='store_true', help='Run filtering'              )
p.add_argument( '--check'   , dest='check'   , default=False, action='store_true', help='Run check of completion'    )
p.add_argument( '--clean'   , dest='clean'   , default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local'   , dest='local'   , default=True , action='store_true', help='Run locally'                )
p.add_argument( '--batch'   , dest='batch'   , default=False , action='store_true', help='Run batch'                )
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
        #(base, 'job_NLO_WAA_FSR'),
        #(base, 'job_NLO_WAA_ISR'),
        (base, 'job_NLO_WAA_FSR_PtG500MeV'),
        (base, 'job_NLO_WAA_ISR_PtG500MeV'),
        #(base, 'job_summer12_Wgg_FSR'),
        #(base, 'job_summer12_WAA_ISR'),
        (base, 'job_summer12_DYJetsToLL_s10PhOlap'),
        (base, 'job_summer12_Wg'),
        (base, 'job_summer12_Zg_s10'),
        (base, 'job_summer12_Wjets'),
        (base, 'job_summer12_WH_ZH_125'),
        (base, 'job_summer12_WW_2l2nu'),
        (base, 'job_summer12_WZ_2l2q'),
        (base, 'job_summer12_WZ_3lnu'),
        (base, 'llaa_nlo_ggNtuple' ),

        ####(base, 'job_summer12_ttjets_1lPhOlap'),
        ####(base, 'job_summer12_ttjets_2lPhOlap'),
        ####(base, 'job_summer12_ttjets_1l'),
        ####(base, 'job_summer12_ttjets_2l'),

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

if options.batch :
    #--------------------
    # for batch submission
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --moduleArgs "%(moduleArgs)s"  --batch --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --exeName %(exename)s_%(job)s '

else :

    #--------------------
    # not batch
    #--------------------
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --moduleArgs "%(moduleArgs)s" --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --exeName %(exename)s  '
    
if options.resubmit :
    command_base += ' --resubmit '

check_commands_base = 'python ../../Util/scripts/check_dataset_completion.py --originalDS %(base)s/%(input)s/%(job)s --filteredDS %(base)s/%(output)s/%(job)s --treeNameOrig %(treename)s --histNameFilt ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root'

top_configs = [
    #---------------------------------------
    # WGG nominal samples
    #---------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_trigmu_met', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaNoPhIDSoft3_2015_12_09',
    # 'output_name' : 'LepGammaGammaFinalMuUnblindAllTESTSoft_2015_12_09',
    # 'tag'         : 'muFinal'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_trigel_met', 'phpt' : ' > 25 ', 'csev' : False, 'mass_cut' : 5 },
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_11_09',
    # 'output_name' : 'LepGammaGammaFinalElPSVOldWindowUnblindAll_2015_12_11',
    # 'tag'         : 'elFinal'
    #},
    #---------------------------------------
    # ZGG nominal samples
    #---------------------------------------
    {   
     'module'      : 'ConfFilter.py', 
     'args'        : {'function' : 'make_final_mumu' },
     'input_name'  : 'LepLepGammaGammaNoPhID_2015_11_09',
     'output_name' : 'LepLepGammaGammaFinalMuMuUnblindAll_2015_12_12',
     'tag'         : 'mumuFinal'
    },
    {   
     'module'      : 'ConfFilter.py', 
     'args'        : {'function' : 'make_final_elel' },
     'input_name'  : 'LepLepGammaGammaNoPhID_2015_11_09',
     'output_name' : 'LepLepGammaGammaFinalElElUnblindAll_2015_12_12',
     'tag'         : 'elelFinal'
    },
    #---------------------------------------
    # WGG samples for jet fakes
    #---------------------------------------
    #{
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_looseID_bothVetoCSEV', 'blind_pt' : 'None'},
    # 'input_name'  : 'LepGammaGammaNoPhIDNoEleOlapRM_2015_11_30',
    # 'output_name' : 'LepGammaGammaNoPhIDNoEleOlapRMVetoCSEVSeedBoth_2015_11_30',
    # 'tag'         : 'vetoBothloose'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_looseID_invCSEVLead', 'blind_pt' : 'None'},
    # 'input_name'  : 'LepGammaGammaNoPhIDNoEleOlapRM_2015_11_30',
    # 'output_name' : 'LepGammaGammaNoPhIDNoEleOlapRMInvCSEVLead_2015_11_30',
    # 'tag'         : 'invLeadloose'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_looseID_invCSEVSubl', 'blind_pt' : 'None'},
    # 'input_name'  : 'LepGammaGammaNoPhIDNoEleOlapRM_2015_11_30',
    # 'output_name' : 'LepGammaGammaNoPhIDNoEleOlapRMInvCSEVSubl_2015_11_30',
    # 'tag'         : 'invSublloose'
    #},
    #---------------------------------------
    # WGG samples for final plots
    #---------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > -1 ', 'mtvar' : 'mt_trigmu_met', 'phpt' : ' > 15 ', 'csev' : True },
    # 'input_name'  : 'LepGammaGammaNoPhID_2015_11_09',
    # 'output_name' : 'LepGammaGammaFinalMuUnblindAllNoMtCutPt15_2015_11_11',
    # 'tag'         : 'muFinalloose'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > -1 ', 'nozmass' : True, 'phpt' : ' > 15 ', 'csev' : True },
    # 'input_name'  : 'LepGammaGammaNoPhIDNoEleOlapRM_2015_11_30',
    # 'output_name' : 'LepGammaGammaFinalElCSEVNoEleOlapRMNoZCutNoMtCutPt15_2015_11_11',
    # 'tag'         : 'elFinalLoose'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    #    'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > -1 ', 'nozmass' : True , 'invpixsubl' : True, 'phpt' : ' > 15 ', 'csev' : True, 'nelcut' : ' == 1 '  },
    # 'input_name'  : 'LepGammaGammaNoPhIDNoEleOlapRM_2015_11_30',
    # 'output_name' : 'LepGammaGammaFinalElCSEVNoEleOlapRMWithDRNoZCutNoMtCutInvPixSublPt15_2015_11_11',
    # 'tag'         : 'elFinalInvPixSubl'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > -1 ', 'nozmass' : True , 'invpixlead' : True, 'phpt' : ' > 15 ', 'csev' : True, 'nelcut' : ' > 0 '  },
    # 'input_name'  : 'LepGammaGammaNoPhIDNoEleOlapRM_2015_11_30',
    # 'output_name' : 'LepGammaGammaFinalElCSEVNoEleOlapRMWithDRNoZCutNoMtCutInvPixLeadPt15_2015_11_11',
    # 'tag'         : 'elFinalInvPixLead'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    #    'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > -1 ', 'nozmass' : True , 'invpixsubl' : True, 'phpt' : ' > 25 ', 'csev' : True, 'nelcut' : ' > 0 '  },
    # 'input_name'  : 'LepGammaGammaNoPhIDNoEleOlapRM_2015_11_30',
    # 'output_name' : 'LepGammaGammaFinalElCSEVNoEleOlapRMWithDRNoZCutNoMtCutInvPixSubl_2015_11_11',
    # 'tag'         : 'elFinalInvPixSubl'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > -1 ', 'nozmass' : True , 'invpixlead' : True, 'phpt' : ' > 25 ', 'csev' : True, 'nelcut' : ' > 0 '  },
    # 'input_name'  : 'LepGammaGammaNoPhIDNoEleOlapRM_2015_11_30',
    # 'output_name' : 'LepGammaGammaFinalElCSEVNoEleOlapRMWithDRNoZCutNoMtCutInvPixLead_2015_11_11',
    # 'tag'         : 'elFinalInvPixLead'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_lep_gamma', 'invpix' : True, 'eleOlap' : True },
    # 'input_name'  : 'LepGammaNoPhID_2015_10_01',
    # 'output_name' : 'LepGammaMediumPhIDWithOlapFailPixSeed_2015_10_01',
    # 'tag'         : 'mediumfailpix'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_lep_gamma', 'invpix' : False, 'eleOlap' : True },
    # 'input_name'  : 'LepGammaNoPhID_2015_10_01',
    # 'output_name' : 'LepGammaMediumPhIDWithOlapPassPixSeed_2015_10_01',
    # 'tag'         : 'mediumpaspix'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mumu' },
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_11_09',
    # 'output_name' : 'LepLepGammaGammaFinalMuMuUnblindAll_2015_11_25',
    # 'tag'         : 'mumuFinal'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_elel' },
    # 'input_name'  : 'LepLepGammaGammaNoPhID_2015_11_09',
    # 'output_name' : 'LepLepGammaGammaFinalElElUnblindAll_2015_11_25',
    # 'tag'         : 'elelFinal'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    #    'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'looseobj' : True, 'notrig' : True, 'phpt' : ' > 10 ', 'mtcut' : ' > -100 '},
    # 'input_name'  : 'LepGammaGammaNoPhIDSoft3_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'tag'         : 'muFinalSoft'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    #    'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'looseobj' : True, 'nozmass' : True, 'csev' : True, 'notrig' : True, 'phpt' : ' > 10 ', 'mtcut' : ' > -100 ' },
    # 'input_name'  : 'LepGammaGammaNoPhIDSoft3_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMediumPhotonIDSoftLep_2015_12_09',
    # 'tag'         : 'elFinalSoft'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mumu', 'looseobj' : True, 'notrig' : True},
    # 'input_name'  : 'LepLepGammaGammaNoPhIDSoft_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuMediumPhotonIDSoftLep_2015_12_09',
    # 'tag'         : 'mumuFinalSoft'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_elel', 'looseobj' : True, 'notrig' : True},
    # 'input_name'  : 'LepLepGammaGammaNoPhIDSoft_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaElMediumPhotonIDSoftLep_2015_12_09',
    # 'tag'         : 'elelFinalSoft'
    #},
    ##--------------------------------------------
    ## Wgg, Electron, NOMINAL
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_trigel_met', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepNOMINAL_2015_12_09',
    # 'output_name' : 'LepGammaGammaElNOMINAL_2015_12_09',
    # 'tag'         : 'elFinalEMUP'
    #},
    ##--------------------------------------------
    ## Wgg, Muon, NOMINAL
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_trigmu_met', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepNOMINAL_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuNOMINALFinal_2015_12_09',
    # 'tag'         : 'elFinalEMUP'
    #},
    ##--------------------------------------------
    ## Wgg, Electron, EG scale
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_met', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepEGammaEScaleUP_2015_12_09',
    # 'output_name' : 'LepGammaGammaElEGammaEScaleUPFinal_2015_12_09',
    # 'tag'         : 'elFinalEMUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_met', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepEGammaEScaleDN_2015_12_09',
    # 'output_name' : 'LepGammaGammaElEGammaEScaleDNFinal_2015_12_09',
    # 'tag'         : 'elFinalEMDN'
    #},
    ##--------------------------------------------
    ## Wgg, Muon, EG scale
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_met', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepEGammaEScaleUP_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuEGammaEScaleUPFinal_2015_12_09',
    # 'tag'         : 'muFinalEMUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_met', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepEGammaEScaleDN_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuEGammaEScaleDNFinal_2015_12_09',
    # 'tag'         : 'muFinalEMDN'
    #},
    ##--------------------------------------------
    ## Wgg, Muon, Muon scale
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_met', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMuonScaleUP_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMuonScaleUPFinal_2015_12_09',
    # 'tag'         : 'muFinalMUUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_met', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMuonScaleDN_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMuonScaleDNFinal_2015_12_09',
    # 'tag'         : 'muFinalMUDN'
    #},
    ##--------------------------------------------
    ## Wgg, Electron, MET uncertainties
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertEMUP', 'phpt' : ' > 25 ', 'csev' : True },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETEMScaleUPFinal_2015_12_09',
    # 'tag'         : 'elFinalMETEMUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertEMDN', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETEMScaleDNFinal_2015_12_09',
    # 'tag'         : 'elFinalMETEMDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertMuonUP', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETMuonScaleUPFinal_2015_12_09',
    # 'tag'         : 'elFinalMETMUUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertMuonDN', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETMuonScaleDNFinal_2015_12_09',
    # 'tag'         : 'elFinalMETMUDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertJESUP', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETJESUPFinal_2015_12_09',
    # 'tag'         : 'elFinalMETJESUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertJESDN', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETJESDNFinal_2015_12_09',
    # 'tag'         : 'elFinalMETJESDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertJERUP', 'phpt' : ' > 25 ' , 'csev' : True },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETJERUPFinal_2015_12_09',
    # 'tag'         : 'elFinalMETJERUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertJERDN', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETJERDNFinal_2015_12_09',
    # 'tag'         : 'elFinalMETJERDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertUnClusUP', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETUnClusUPFinal_2015_12_09',
    # 'tag'         : 'elFinalMETUnClusUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_el', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertUnClusDN', 'phpt' : ' > 25 ', 'csev' : True  },
    # 'input_name'  : 'LepGammaGammaElMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaElMETUnClusDNFinal_2015_12_09',
    # 'tag'         : 'elFinalMETUnClusDN'
    #},
    ##--------------------------------------------
    ## Wgg, Muon , MET uncertainties
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertEMUP', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETEMScaleUPFinal_2015_12_09',
    # 'tag'         : 'muFinalMETEMUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertEMDN', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETEMScaleDNFinal_2015_12_09',
    # 'tag'         : 'muFinalMETEMDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertMuonUP', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETMuonScaleUPFinal_2015_12_09',
    # 'tag'         : 'muFinalMETMUUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertMuonDN', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETMuonScaleDNFinal_2015_12_09',
    # 'tag'         : 'muFinalMETMUDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertJESUP', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETJESUPFinal_2015_12_09',
    # 'tag'         : 'muFinalMETJESUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertJESDN', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETJESDNFinal_2015_12_09',
    # 'tag'         : 'muFinalMETJESDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertJERUP', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETJERUPFinal_2015_12_09',
    # 'tag'         : 'muFinalMETJERUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertJERDN', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETJERDNFinal_2015_12_09',
    # 'tag'         : 'muFinalMetJERDN'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertUnClusUP', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETUnClusUPFinal_2015_12_09',
    # 'tag'         : 'muFinalMETUnClusUp'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mu', 'blind_pt' : 'None', 'mtcut' : ' > 40 ', 'mtvar' : 'mt_lep_metUncertUnClusDN', 'phpt' : ' > 25 ' },
    # 'input_name'  : 'LepGammaGammaMuMediumPhotonIDSoftLepMETUncert_2015_12_09',
    # 'output_name' : 'LepGammaGammaMuMETUnClusDNFinal_2015_12_09',
    # 'tag'         : 'muFinalMETUnClusDn'
    #},

    ##--------------------------------------------
    ## Zgg, Muon , NOMINAL
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mumu' },
    # 'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLepNOMINAL_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuNOMINALFinal_2015_12_09',
    # 'tag'         : 'muFinalNOM'
    #},
    ##--------------------------------------------
    ## Zgg, Electron , NOMINAL
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_elel' },
    # 'input_name'  : 'LepLepGammaGammaElMediumPhotonIDSoftLepNOMINAL_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaElNOMINALFinal_2015_12_09',
    # 'tag'         : 'elFinalNOM'
    #},
    ##--------------------------------------------
    ## Zgg, Electron, EG scale
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_elel' },
    # 'input_name'  : 'LepLepGammaGammaElMediumPhotonIDSoftLepEGammaEScaleUP_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaElEGammaEScaleUPFinal_2015_12_09',
    # 'tag'         : 'elelFinalEMUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_elel' },
    # 'input_name'  : 'LepLepGammaGammaElMediumPhotonIDSoftLepEGammaEScaleDN_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaElEGammaEScaleDNFinal_2015_12_09',
    # 'tag'         : 'elelFinalEMDN'
    #},
    ##--------------------------------------------
    ## Zgg, Muon, EG scale
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mumu' },
    # 'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLepEGammaEScaleUP_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuEGammaEScaleUPFinal_2015_12_09',
    # 'tag'         : 'mumuFinalEMUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mumu' },
    # 'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLepEGammaEScaleDN_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuEGammaEScaleDNFinal_2015_12_09',
    # 'tag'         : 'mumuFinalEMDN'
    #},
    ##--------------------------------------------
    ## Zgg, Muon, Muon scale
    ##--------------------------------------------
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mumu' },
    # 'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLepMuonScaleUP_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuMuonScaleUPFinal_2015_12_09',
    # 'tag'         : 'mumuFinalMUUP'
    #},
    #{   
    # 'module'      : 'ConfFilter.py', 
    # 'args'        : {'function' : 'make_final_mumu' },
    # 'input_name'  : 'LepLepGammaGammaMuMediumPhotonIDSoftLepMuonScaleDN_2015_12_09',
    # 'output_name' : 'LepLepGammaGammaMuMuonScaleDNFinal_2015_12_09',
    # 'tag'         : 'mumuFinalMUDN'
    #},
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
    first_data = True
    first_mc = True
    for config in top_configs :

        for base, job in jobs_data :
            job_exename = '%s_Data' %(exename )

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

            if not first_data :
                command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first_data :
                first_data = False

        for base, job in jobs_mc :
            job_exename = '%s_MC' %(exename )

            module_arg = config['args']

            module_str = '{ '
            for key, val in module_arg.iteritems() :
                if isinstance( val, basestring ) :
                    module_str += '\'%s\' : \'%s\',' %( key, val)
                else :
                    module_str += '\'%s\' : %s,' %( key, val)

            module_str += '}'

            command = command_base %{ 'base' : base, 'job' : job, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : config['output_name'], 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }
            if not first_mc :
                command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first_mc :
                first_mc = False

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





