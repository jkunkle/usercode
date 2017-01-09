{#Cross sections are in pb
 # Some are taken from 
 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV [1]
 # TTBar total cros section is 815.96 pb, taken from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
 'DYJetsToLL_M-50'               : { 'n_evt' : 49877138, 'cross_section' : 5765.4 , 'gen_eff' : 1.0 , 'k_factor' : 1.0 }, # NNLO cross section from [1]
 'TTJets_DiLept'                 : { 'n_evt' : 6094476, 'cross_section'  :  815.96*0.105, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # TTbar cross section times dilepton branching fraction
 'TTJets_SingleLeptFromT'        : { 'n_evt' : 11957043, 'cross_section' : 815.96*0.438*0.5, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # TTbar cross section times semileptonic branching fraction divided by 2 for charge
 'TTJets_SingleLeptFromTbar'     : { 'n_evt' : 48266353, 'cross_section' : 815.96*0.438*0.5, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # TTbar cross section times semileptonic branching fraction divided by 2 for charge
 'WGToLNuG-amcatnloFXFX'         : { 'n_evt' : 3235156, 'cross_section' : 489.0, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # cross section taken from McM.  #total events = 5048470
 'WGToLNuG_PtG-130-amcatnloFXFX' : { 'n_evt' : 841701, 'cross_section' : 1.161, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # cross section taken from McM # total events = 1561571
 'WWG'                           : { 'n_evt' : 827630, 'cross_section' : 0.2147, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # cross section taken from McM.  # total events = 999400
 'WJetsToLNu'                    : { 'n_evt' : 29705748, 'cross_section' : 20508.9*3, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },# NNLO cross section from [1]

                  'Zg'                     : { 'n_evt' : 3044343, 'cross_section' : 124.5 , 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'Wg'                     : { 'n_evt' : 2183649, 'cross_section' : 505.8 , 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'WgPt500'                : { 'n_evt' : 1393505, 'cross_section' : 0.0117887 , 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'TTbar'                  : { 'n_evt' : 96584653, 'cross_section' : 831.76, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'GJets'                  : { 'n_evt' : 1972730, 'cross_section' : 693300.0, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'WW'                     : { 'n_evt' : 1965200, 'cross_section' : 12.178, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'ZZ'                     : { 'n_evt' : 996944, 'cross_section' : 16.523, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'WZ3LNLO'                : { 'n_evt' : 8260201, 'cross_section' : 5.26, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'ST_TW'                  : { 'n_evt' : 995600, 'cross_section' : 35.6, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'ST_TbarW'               : { 'n_evt' : 988500, 'cross_section' : 35.6, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'STtCh'                  : { 'n_evt' : 1, 'cross_section' : 70.69, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'STsCh'                  : { 'n_evt' : 984400, 'cross_section' : 10.32, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'DiPhoton_M40_80'        : { 'n_evt' : 4878862, 'cross_section' : 84.0*2.5, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  'DiPhoton_M80toInf'        : { 'n_evt' : 13200226, 'cross_section' : 84.0, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  #'ResonanceMass400Width10' : {'n_evt' : 10000, 'cross_section' : 0.4, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },
                  #'ResonanceMass2000Width10' : {'n_evt' : 10000, 'cross_section' : 0.004, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },

}

