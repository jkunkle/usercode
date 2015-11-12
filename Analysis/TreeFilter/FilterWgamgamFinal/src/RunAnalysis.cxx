#include "include/RunAnalysis.h"

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <boost/foreach.hpp>
#include <boost/algorithm/string.hpp>
#include <sys/types.h>
#include <sys/stat.h>
#include <math.h>
#include <stdlib.h>

#include "include/BranchDefs.h"
#include "include/BranchInit.h"
#include "CalcWggEventVars.h"

#include "Core/Util.h"

#include "TFile.h"



int main(int argc, char **argv)
{

    //TH1::AddDirectory(kFALSE);
    CmdOptions options = ParseOptions( argc, argv );

    // Parse the text file and form the configuration object
    AnaConfig ana_config = ParseConfig( options.config_file, options );
    std::cout << "Configured " << ana_config.size() << " analysis modules " << std::endl;

    RunModule runmod;
    ana_config.Run(runmod, options);

    std::cout << "^_^ Finished ^_^" << std::endl;


}

void RunModule::initialize( TChain * chain, TTree * outtree, TFile *outfile,
                            const CmdOptions & options, std::vector<ModuleConfig> &configs ) {

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Set defaults for added output variables
    // *************************
    OUT::isBlinded = 0;

    OUT::dphi_met_phot                           = 0;
    OUT::m_leadLep_phot                          = 0;
    OUT::m_sublLep_phot                          = 0;
    OUT::m_trigEl_phot                           = 0;
    OUT::m_trigMu_phot                           = 0;
    OUT::dr_leadLep_phot                         = 0;
    OUT::dr_sublLep_phot                         = 0;
    OUT::dr_trigEl_phot                          = 0;
    OUT::dr_trigMu_phot                          = 0;
    OUT::dphi_leadLep_phot                       = 0;
    OUT::dphi_sublLep_phot                       = 0;
    OUT::dphi_trigEl_phot                        = 0;
    OUT::dphi_trigMu_phot                        = 0;
    OUT::mt_met_trigEl_phot                      = 0;
    OUT::mt_met_trigMu_phot                      = 0;
    OUT::m_leplep_phot                           = 0;
    OUT::m_diphot                                = 0;
    OUT::dr_diphot                               = 0;
    OUT::dphi_diphot                             = 0;
    OUT::pt_diphot                               = 0;
    OUT::m_leplep_diphot                         = 0;
    OUT::m_trigEl_diphot                         = 0;
    OUT::m_trigMu_diphot                         = 0;
    OUT::mt_met_trigEl_diphot                    = 0;
    OUT::mt_met_trigMu_diphot                    = 0;


    OUT::ptSorted_ph_noSIEIEiso533_idx           = 0;
    OUT::ptSorted_ph_noSIEIEiso855_idx           = 0;
    OUT::ptSorted_ph_noSIEIEiso1077_idx          = 0;
    OUT::ptSorted_ph_noSIEIEiso1299_idx          = 0;
    OUT::ptSorted_ph_noSIEIEiso151111_idx        = 0;
    OUT::ptSorted_ph_noSIEIEiso201616_idx        = 0;
    OUT::ptSorted_ph_passSIEIEiso53None_idx      = 0;
    OUT::ptSorted_ph_passSIEIEiso85None_idx      = 0;
    OUT::ptSorted_ph_passSIEIEiso107None_idx     = 0;
    OUT::ptSorted_ph_passSIEIEiso129None_idx     = 0;
    OUT::ptSorted_ph_passSIEIEiso1511None_idx    = 0;
    OUT::ptSorted_ph_passSIEIEiso2016None_idx    = 0;
    OUT::ptSorted_ph_passSIEIEiso5None3_idx      = 0;
    OUT::ptSorted_ph_passSIEIEiso8None5_idx      = 0;
    OUT::ptSorted_ph_passSIEIEiso10None7_idx     = 0;
    OUT::ptSorted_ph_passSIEIEiso12None9_idx     = 0;
    OUT::ptSorted_ph_passSIEIEiso15None11_idx    = 0;
    OUT::ptSorted_ph_passSIEIEiso20None16_idx    = 0;
    OUT::ptSorted_ph_passSIEIEisoNone33_idx      = 0;
    OUT::ptSorted_ph_passSIEIEisoNone55_idx      = 0;
    OUT::ptSorted_ph_passSIEIEisoNone77_idx      = 0;
    OUT::ptSorted_ph_passSIEIEisoNone99_idx      = 0;
    OUT::ptSorted_ph_passSIEIEisoNone1111_idx    = 0;
    OUT::ptSorted_ph_passSIEIEisoNone1616_idx    = 0;
    OUT::ptSorted_ph_failSIEIEiso53None_idx      = 0;
    OUT::ptSorted_ph_failSIEIEiso85None_idx      = 0;
    OUT::ptSorted_ph_failSIEIEiso107None_idx     = 0;
    OUT::ptSorted_ph_failSIEIEiso129None_idx     = 0;
    OUT::ptSorted_ph_failSIEIEiso1511None_idx    = 0;
    OUT::ptSorted_ph_failSIEIEiso2016None_idx    = 0;
    OUT::ptSorted_ph_failSIEIEiso5None3_idx      = 0;
    OUT::ptSorted_ph_failSIEIEiso8None5_idx      = 0;
    OUT::ptSorted_ph_failSIEIEiso10None7_idx     = 0;
    OUT::ptSorted_ph_failSIEIEiso12None9_idx     = 0;
    OUT::ptSorted_ph_failSIEIEiso15None11_idx    = 0;
    OUT::ptSorted_ph_failSIEIEiso20None16_idx    = 0;
    OUT::ptSorted_ph_failSIEIEisoNone33_idx      = 0;
    OUT::ptSorted_ph_failSIEIEisoNone55_idx      = 0;
    OUT::ptSorted_ph_failSIEIEisoNone77_idx      = 0;
    OUT::ptSorted_ph_failSIEIEisoNone99_idx      = 0;
    OUT::ptSorted_ph_failSIEIEisoNone1111_idx    = 0;
    OUT::ptSorted_ph_failSIEIEisoNone1616_idx    = 0;
    OUT::ptSorted_ph_mediumNoNeuIsoNoPhoIso_idx  = 0;
    OUT::ptSorted_ph_mediumNoChIsoNoPhoIso_idx   = 0;
    OUT::ptSorted_ph_mediumNoChIsoNoNeuIso_idx   = 0;
    OUT::ptSorted_ph_mediumNoSIEIENoPhoIso_idx   = 0;
    OUT::ptSorted_ph_mediumNoSIEIENoNeuIso_idx   = 0;
    OUT::ptSorted_ph_mediumNoSIEIENoChIso_idx    = 0;
    OUT::ptSorted_ph_mediumNoSIEIENoEleVeto_idx  = 0;
    OUT::ptSorted_ph_mediumNoSIEIEPassPSV_idx    = 0;
    OUT::ptSorted_ph_mediumNoSIEIEFailPSV_idx    = 0;
    OUT::ptSorted_ph_mediumNoSIEIEPassCSEV_idx   = 0;
    OUT::ptSorted_ph_mediumNoSIEIEFailCSEV_idx   = 0;
    OUT::ptSorted_ph_mediumNoEleVeto_idx         = 0;
    OUT::ptSorted_ph_mediumPassPSV_idx           = 0;
    OUT::ptSorted_ph_mediumFailPSV_idx           = 0;
    OUT::ptSorted_ph_mediumPassCSEV_idx          = 0;
    OUT::ptSorted_ph_mediumFailCSEV_idx          = 0;
    OUT::ptSorted_ph_mediumNoChIsoNoEleVeto_idx  = 0;
    OUT::ptSorted_ph_mediumNoChIsoPassPSV_idx    = 0;
    OUT::ptSorted_ph_mediumNoChIsoFailPSV_idx    = 0;
    OUT::ptSorted_ph_mediumNoChIsoPassCSEV_idx   = 0;
    OUT::ptSorted_ph_mediumNoChIsoFailCSEV_idx   = 0;
    OUT::ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx = 0;
    OUT::ptSorted_ph_mediumNoNeuIsoPassPSV_idx   = 0;
    OUT::ptSorted_ph_mediumNoNeuIsoFailPSV_idx   = 0;
    OUT::ptSorted_ph_mediumNoNeuIsoPassCSEV_idx  = 0;
    OUT::ptSorted_ph_mediumNoNeuIsoFailCSEV_idx  = 0;
    OUT::ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx = 0;
    OUT::ptSorted_ph_mediumNoPhoIsoPassPSV_idx   = 0;
    OUT::ptSorted_ph_mediumNoPhoIsoFailPSV_idx   = 0;
    OUT::ptSorted_ph_mediumNoPhoIsoPassCSEV_idx  = 0;
    OUT::ptSorted_ph_mediumNoPhoIsoFailCSEV_idx  = 0;

    // *************************
    // Declare Branches
    // *************************
    outtree->Branch("isBlinded", &OUT::isBlinded );
    outtree->Branch("EventWeight", &OUT::EventWeight, "EventWeight/F" );

    outtree->Branch("mu_pt25_n"                    , &OUT::mu_pt25_n                    , "mu_pt25_n/I"                    );
    outtree->Branch("mu_passtrig_n"                , &OUT::mu_passtrig_n                , "mu_passtrig_n/I"                );
    outtree->Branch("mu_passtrig25_n"              , &OUT::mu_passtrig25_n              , "mu_passtrig25_n/I"              );
    outtree->Branch("el_pt25_n"                    , &OUT::el_pt25_n                    , "el_pt25_n/I"                    );
    outtree->Branch("el_passtrig_n"                , &OUT::el_passtrig_n                , "el_passtrig_n/I"                );
    outtree->Branch("el_passtrigL_n"               , &OUT::el_passtrigL_n               , "el_passtrigL_n/I"               );
    outtree->Branch("el_passtrig28_n"              , &OUT::el_passtrig28_n              , "el_passtrig28_n/I"              );
    outtree->Branch("ph_mediumNoEleVeto_n"         , &OUT::ph_mediumNoEleVeto_n         , "ph_mediumNoEleVeto_n/I"         );
    outtree->Branch("ph_noSIEIEiso533_n"           , &OUT::ph_noSIEIEiso533_n           , "ph_noSIEIEiso533_n/I"           );
    outtree->Branch("ph_noSIEIEiso855_n"           , &OUT::ph_noSIEIEiso855_n           , "ph_noSIEIEiso855_n/I"           );
    outtree->Branch("ph_noSIEIEiso1077_n"          , &OUT::ph_noSIEIEiso1077_n          , "ph_noSIEIEiso1077_n/I"          );
    outtree->Branch("ph_noSIEIEiso1299_n"          , &OUT::ph_noSIEIEiso1299_n          , "ph_noSIEIEiso1299_n/I"          );
    outtree->Branch("ph_noSIEIEiso151111_n"        , &OUT::ph_noSIEIEiso151111_n        , "ph_noSIEIEiso151111_n/I"        );
    outtree->Branch("ph_noSIEIEiso201616_n"        , &OUT::ph_noSIEIEiso201616_n        , "ph_noSIEIEiso201616_n/I"        );
    outtree->Branch("ph_passSIEIEiso53None_n"      , &OUT::ph_passSIEIEiso53None_n      , "ph_passSIEIEiso53None_n/I"      );
    outtree->Branch("ph_passSIEIEiso85None_n"      , &OUT::ph_passSIEIEiso85None_n      , "ph_passSIEIEiso85None_n/I"      );
    outtree->Branch("ph_passSIEIEiso107None_n"     , &OUT::ph_passSIEIEiso107None_n     , "ph_passSIEIEiso107None_n/I"     );
    outtree->Branch("ph_passSIEIEiso129None_n"     , &OUT::ph_passSIEIEiso129None_n     , "ph_passSIEIEiso129None_n/I"     );
    outtree->Branch("ph_passSIEIEiso1511None_n"    , &OUT::ph_passSIEIEiso1511None_n    , "ph_passSIEIEiso1511None_n/I"    );
    outtree->Branch("ph_passSIEIEiso2016None_n"    , &OUT::ph_passSIEIEiso2016None_n    , "ph_passSIEIEiso2016None_n/I"    );
    outtree->Branch("ph_passSIEIEiso5None3_n"      , &OUT::ph_passSIEIEiso5None3_n      , "ph_passSIEIEiso5None3_n/I"      );
    outtree->Branch("ph_passSIEIEiso8None5_n"      , &OUT::ph_passSIEIEiso8None5_n      , "ph_passSIEIEiso8None5_n/I"      );
    outtree->Branch("ph_passSIEIEiso10None7_n"     , &OUT::ph_passSIEIEiso10None7_n     , "ph_passSIEIEiso10None7_n/I"     );
    outtree->Branch("ph_passSIEIEiso12None9_n"     , &OUT::ph_passSIEIEiso12None9_n     , "ph_passSIEIEiso12None9_n/I"     );
    outtree->Branch("ph_passSIEIEiso15None11_n"    , &OUT::ph_passSIEIEiso15None11_n    , "ph_passSIEIEiso15None11_n/I"    );
    outtree->Branch("ph_passSIEIEiso20None16_n"    , &OUT::ph_passSIEIEiso20None16_n    , "ph_passSIEIEiso20None16_n/I"    );
    outtree->Branch("ph_passSIEIEisoNone33_n"      , &OUT::ph_passSIEIEisoNone33_n      , "ph_passSIEIEisoNone33_n/I"      );
    outtree->Branch("ph_passSIEIEisoNone55_n"      , &OUT::ph_passSIEIEisoNone55_n      , "ph_passSIEIEisoNone55_n/I"      );
    outtree->Branch("ph_passSIEIEisoNone77_n"      , &OUT::ph_passSIEIEisoNone77_n      , "ph_passSIEIEisoNone77_n/I"      );
    outtree->Branch("ph_passSIEIEisoNone99_n"      , &OUT::ph_passSIEIEisoNone99_n      , "ph_passSIEIEisoNone99_n/I"      );
    outtree->Branch("ph_passSIEIEisoNone1111_n"    , &OUT::ph_passSIEIEisoNone1111_n    , "ph_passSIEIEisoNone1111_n/I"    );
    outtree->Branch("ph_passSIEIEisoNone1616_n"    , &OUT::ph_passSIEIEisoNone1616_n    , "ph_passSIEIEisoNone1616_n/I"    );
    outtree->Branch("ph_failSIEIEiso53None_n"      , &OUT::ph_failSIEIEiso53None_n      , "ph_failSIEIEiso53None_n/I"      );
    outtree->Branch("ph_failSIEIEiso85None_n"      , &OUT::ph_failSIEIEiso85None_n      , "ph_failSIEIEiso85None_n/I"      );
    outtree->Branch("ph_failSIEIEiso107None_n"     , &OUT::ph_failSIEIEiso107None_n     , "ph_failSIEIEiso107None_n/I"     );
    outtree->Branch("ph_failSIEIEiso129None_n"     , &OUT::ph_failSIEIEiso129None_n     , "ph_failSIEIEiso129None_n/I"     );
    outtree->Branch("ph_failSIEIEiso1511None_n"    , &OUT::ph_failSIEIEiso1511None_n    , "ph_failSIEIEiso1511None_n/I"    );
    outtree->Branch("ph_failSIEIEiso2016None_n"    , &OUT::ph_failSIEIEiso2016None_n    , "ph_failSIEIEiso2016None_n/I"    );
    outtree->Branch("ph_failSIEIEiso5None3_n"      , &OUT::ph_failSIEIEiso5None3_n      , "ph_failSIEIEiso5None3_n/I"      );
    outtree->Branch("ph_failSIEIEiso8None5_n"      , &OUT::ph_failSIEIEiso8None5_n      , "ph_failSIEIEiso8None5_n/I"      );
    outtree->Branch("ph_failSIEIEiso10None7_n"     , &OUT::ph_failSIEIEiso10None7_n     , "ph_failSIEIEiso10None7_n/I"     );
    outtree->Branch("ph_failSIEIEiso12None9_n"     , &OUT::ph_failSIEIEiso12None9_n     , "ph_failSIEIEiso12None9_n/I"     );
    outtree->Branch("ph_failSIEIEiso15None11_n"    , &OUT::ph_failSIEIEiso15None11_n    , "ph_failSIEIEiso15None11_n/I"    );
    outtree->Branch("ph_failSIEIEiso20None16_n"    , &OUT::ph_failSIEIEiso20None16_n    , "ph_failSIEIEiso20None16_n/I"    );
    outtree->Branch("ph_failSIEIEisoNone33_n"      , &OUT::ph_failSIEIEisoNone33_n      , "ph_failSIEIEisoNone33_n/I"      );
    outtree->Branch("ph_failSIEIEisoNone55_n"      , &OUT::ph_failSIEIEisoNone55_n      , "ph_failSIEIEisoNone55_n/I"      );
    outtree->Branch("ph_failSIEIEisoNone77_n"      , &OUT::ph_failSIEIEisoNone77_n      , "ph_failSIEIEisoNone77_n/I"      );
    outtree->Branch("ph_failSIEIEisoNone99_n"      , &OUT::ph_failSIEIEisoNone99_n      , "ph_failSIEIEisoNone99_n/I"      );
    outtree->Branch("ph_failSIEIEisoNone1111_n"    , &OUT::ph_failSIEIEisoNone1111_n    , "ph_failSIEIEisoNone1111_n/I"    );
    outtree->Branch("ph_failSIEIEisoNone1616_n"    , &OUT::ph_failSIEIEisoNone1616_n    , "ph_failSIEIEisoNone1616_n/I"    );
    outtree->Branch("ph_mediumNoNeuIsoNoPhoIso_n"  , &OUT::ph_mediumNoNeuIsoNoPhoIso_n  , "ph_mediumNoNeuIsoNoPhoIso_n/I"  );
    outtree->Branch("ph_mediumNoChIsoNoPhoIso_n"   , &OUT::ph_mediumNoChIsoNoPhoIso_n   , "ph_mediumNoChIsoNoPhoIso_n/I"   );
    outtree->Branch("ph_mediumNoChIsoNoNeuIso_n"   , &OUT::ph_mediumNoChIsoNoNeuIso_n   , "ph_mediumNoChIsoNoNeuIso_n/I"   );
    outtree->Branch("ph_mediumNoSIEIENoPhoIso_n"   , &OUT::ph_mediumNoSIEIENoPhoIso_n   , "ph_mediumNoSIEIENoPhoIso_n/I"  );
    outtree->Branch("ph_mediumNoSIEIENoNeuIso_n"   , &OUT::ph_mediumNoSIEIENoNeuIso_n   , "ph_mediumNoSIEIENoNeuIso_n/I"  );
    outtree->Branch("ph_mediumNoSIEIENoChIso_n"    , &OUT::ph_mediumNoSIEIENoChIso_n    , "ph_mediumNoSIEIENoChIso_n/I"  );
    outtree->Branch("ph_mediumNoSIEIENoEleVeto_n"  , &OUT::ph_mediumNoSIEIENoEleVeto_n  , "ph_mediumNoSIEIENoEleVeto_n/I"  );
    outtree->Branch("ph_mediumNoSIEIEPassPSV_n"    , &OUT::ph_mediumNoSIEIEPassPSV_n    , "ph_mediumNoSIEIEPassPSV_n/I"    );
    outtree->Branch("ph_mediumNoSIEIEFailPSV_n"    , &OUT::ph_mediumNoSIEIEFailPSV_n    , "ph_mediumNoSIEIEFailPSV_n/I"    );
    outtree->Branch("ph_mediumNoSIEIEPassCSEV_n"   , &OUT::ph_mediumNoSIEIEPassCSEV_n   , "ph_mediumNoSIEIEPassCSEV_n/I"   );
    outtree->Branch("ph_mediumNoSIEIEFailCSEV_n"   , &OUT::ph_mediumNoSIEIEFailCSEV_n   , "ph_mediumNoSIEIEFailCSEV_n/I"   );
    outtree->Branch("ph_mediumPassPSV_n"           , &OUT::ph_mediumPassPSV_n           , "ph_mediumPassPSV_n/I"           );
    outtree->Branch("ph_mediumFailPSV_n"           , &OUT::ph_mediumFailPSV_n           , "ph_mediumFailPSV_n/I"           );
    outtree->Branch("ph_mediumPassCSEV_n"          , &OUT::ph_mediumPassCSEV_n          , "ph_mediumPassCSEV_n/I"          );
    outtree->Branch("ph_mediumFailCSEV_n"          , &OUT::ph_mediumFailCSEV_n          , "ph_mediumFailCSEV_n/I"          );
    outtree->Branch("ph_mediumNoChIsoNoEleVeto_n"  , &OUT::ph_mediumNoChIsoNoEleVeto_n  , "ph_mediumNoChIsoNoEleVeto_n/I"  );
    outtree->Branch("ph_mediumNoChIsoPassPSV_n"    , &OUT::ph_mediumNoChIsoPassPSV_n    , "ph_mediumNoChIsoPassPSV_n/I"    );
    outtree->Branch("ph_mediumNoChIsoFailPSV_n"    , &OUT::ph_mediumNoChIsoFailPSV_n    , "ph_mediumNoChIsoFailPSV_n/I"    );
    outtree->Branch("ph_mediumNoChIsoPassCSEV_n"   , &OUT::ph_mediumNoChIsoPassCSEV_n   , "ph_mediumNoChIsoPassCSEV_n/I"   );
    outtree->Branch("ph_mediumNoChIsoFailCSEV_n"   , &OUT::ph_mediumNoChIsoFailCSEV_n   , "ph_mediumNoChIsoFailCSEV_n/I"   );
    outtree->Branch("ph_mediumNoNeuIsoNoEleVeto_n" , &OUT::ph_mediumNoNeuIsoNoEleVeto_n , "ph_mediumNoNeuIsoNoEleVeto_n/I" );
    outtree->Branch("ph_mediumNoNeuIsoPassPSV_n"   , &OUT::ph_mediumNoNeuIsoPassPSV_n   , "ph_mediumNoNeuIsoPassPSV_n/I"   );
    outtree->Branch("ph_mediumNoNeuIsoFailPSV_n"   , &OUT::ph_mediumNoNeuIsoFailPSV_n   , "ph_mediumNoNeuIsoFailPSV_n/I"   );
    outtree->Branch("ph_mediumNoNeuIsoPassCSEV_n"  , &OUT::ph_mediumNoNeuIsoPassCSEV_n  , "ph_mediumNoNeuIsoPassCSEV_n/I"  );
    outtree->Branch("ph_mediumNoNeuIsoFailCSEV_n"  , &OUT::ph_mediumNoNeuIsoFailCSEV_n  , "ph_mediumNoNeuIsoFailCSEV_n/I"  );
    outtree->Branch("ph_mediumNoPhoIsoNoEleVeto_n" , &OUT::ph_mediumNoPhoIsoNoEleVeto_n , "ph_mediumNoPhoIsoNoEleVeto_n/I" );
    outtree->Branch("ph_mediumNoPhoIsoPassPSV_n"   , &OUT::ph_mediumNoPhoIsoPassPSV_n   , "ph_mediumNoPhoIsoPassPSV_n/I"   );
    outtree->Branch("ph_mediumNoPhoIsoFailPSV_n"   , &OUT::ph_mediumNoPhoIsoFailPSV_n   , "ph_mediumNoPhoIsoFailPSV_n/I"   );
    outtree->Branch("ph_mediumNoPhoIsoPassCSEV_n"  , &OUT::ph_mediumNoPhoIsoPassCSEV_n  , "ph_mediumNoPhoIsoPassCSEV_n/I"  );
    outtree->Branch("ph_mediumNoPhoIsoFailCSEV_n"  , &OUT::ph_mediumNoPhoIsoFailCSEV_n  , "ph_mediumNoPhoIsoFailCSEV_n/I"  );

    outtree->Branch("ph_trigMatch_el"              , &OUT::ph_trigMatch_el             );
    outtree->Branch("ph_elMinDR"                   , &OUT::ph_elMinDR                  );
    
    outtree->Branch("leadPhot_sublPhotDR"             , &OUT::leadPhot_sublPhotDR            , "leadPhot_sublPhotDR/F"            );
    outtree->Branch("leadPhot_sublPhotDPhi"           , &OUT::leadPhot_sublPhotDPhi          , "leadPhot_sublPhotDPhi/F"          );
    outtree->Branch("dphi_met_leadPhot"        , &OUT::dphi_met_leadPhot       , "dphi_met_leadPhot/F"       );
    outtree->Branch("dphi_met_sublPhot"        , &OUT::dphi_met_sublPhot       , "dphi_met_sublPhot/F"       );
    outtree->Branch("dphi_met_lep1"       , &OUT::dphi_met_lep1      , "dphi_met_lep1/F"      );
    outtree->Branch("dphi_met_lep2"       , &OUT::dphi_met_lep2      , "dphi_met_lep2/F"      );
    outtree->Branch("dphi_met_ph1"        , &OUT::dphi_met_ph1       , "dphi_met_ph1/F"       );
    outtree->Branch("dphi_met_ph2"        , &OUT::dphi_met_ph2       , "dphi_met_ph2/F"       );
    outtree->Branch("mt_lep_met"          , &OUT::mt_lep_met         , "mt_lep_met/F"         );
    outtree->Branch("mt_lepph1_met"       , &OUT::mt_lepph1_met      , "mt_lepph1_met/F"      );
    outtree->Branch("mt_lepph2_met"       , &OUT::mt_lepph2_met      , "mt_lepph2_met/F"      );
    outtree->Branch("mt_lepphph_met"      , &OUT::mt_lepphph_met     , "mt_lepphph_met/F"     );
    outtree->Branch("mt_trigel_met"          , &OUT::mt_trigel_met         , "mt_trigel_met/F"         );
    outtree->Branch("mt_trigmu_met"          , &OUT::mt_trigmu_met         , "mt_trigmu_met/F"         );
    outtree->Branch("m_leplep"            , &OUT::m_leplep           , "m_leplep/F"           );
    outtree->Branch("m_mumu"            , &OUT::m_mumu           , "m_mumu/F"           );
    outtree->Branch("m_elel"            , &OUT::m_elel           , "m_elel/F"           );
    outtree->Branch("m_leplep_uncorr"     , &OUT::m_leplep_uncorr    , "m_leplep_uncorr/F"    );
    outtree->Branch("m_trigelph1"         , &OUT::m_trigelph1        , "m_trigelph1/F"           );
    outtree->Branch("m_trigelph2"         , &OUT::m_trigelph2        , "m_trigelph2/F"           );
    outtree->Branch("m_lepph1"            , &OUT::m_lepph1           , "m_lepph1/F"           );
    outtree->Branch("m_lepph2"            , &OUT::m_lepph2           , "m_lepph2/F"           );
    outtree->Branch("m_lepphlead"            , &OUT::m_lepphlead           , "m_lepphlead/F"           );
    outtree->Branch("m_lepphsubl"            , &OUT::m_lepphsubl           , "m_lepphsubl/F"           );
    outtree->Branch("m_lep2phlead"            , &OUT::m_lep2phlead           , "m_lep2phlead/F"           );
    outtree->Branch("m_lep2phsubl"            , &OUT::m_lep2phsubl           , "m_lep2phsubl/F"           );
    outtree->Branch("m_leplepph"          , &OUT::m_leplepph         , "m_leplepph/F"         );
    outtree->Branch("m_leplepphph"        , &OUT::m_leplepphph       , "m_leplepphph/F"         );
    outtree->Branch("m_leplepph1"         , &OUT::m_leplepph1        , "m_leplepph1/F"         );
    outtree->Branch("m_leplepph2"         , &OUT::m_leplepph2        , "m_leplepph2/F"         );
    outtree->Branch("m_lepphph"           , &OUT::m_lepphph          , "m_lepphph/F"          );
    outtree->Branch("m_trigelphph"        , &OUT::m_trigelphph       , "m_trigelphph/F"          );
    outtree->Branch("m_3lep"              , &OUT::m_3lep             , "m_3lep/F"             );
    outtree->Branch("m_4lep"              , &OUT::m_4lep             , "m_4lep/F"             );
    outtree->Branch("pt_leplep"           , &OUT::pt_leplep          , "pt_leplep/F"          );
    outtree->Branch("pt_lepph1"           , &OUT::pt_lepph1          , "pt_lepph1/F"          );
    outtree->Branch("pt_lepph2"           , &OUT::pt_lepph2          , "pt_lepph2/F"          );
    outtree->Branch("pt_lepphph"          , &OUT::pt_lepphph         , "pt_lepphph/F"         );
    outtree->Branch("pt_leplepph"         , &OUT::pt_leplepph        , "pt_leplepph/F"        );
    outtree->Branch("pt_secondLepton"     , &OUT::pt_secondLepton    , "pt_secondLepton/F"    );
    outtree->Branch("pt_thirdLepton"      , &OUT::pt_thirdLepton     , "pt_thirdLepton/F"     );
    outtree->Branch("leadPhot_leadLepDR"  , &OUT::leadPhot_leadLepDR , "leadPhot_leadLepDR/F" );
    outtree->Branch("leadPhot_sublLepDR"  , &OUT::leadPhot_sublLepDR , "leadPhot_sublLepDR/F" );
    outtree->Branch("sublPhot_leadLepDR"  , &OUT::sublPhot_leadLepDR , "sublPhot_leadLepDR/F" );
    outtree->Branch("sublPhot_sublLepDR"  , &OUT::sublPhot_sublLepDR , "sublPhot_sublLepDR/F" );
    outtree->Branch("leadPhot_trigElDR"  , &OUT::leadPhot_trigElDR , "leadPhot_trigElDR/F" );
    outtree->Branch("sublPhot_trigElDR"  , &OUT::sublPhot_trigElDR , "sublPhot_trigElDR/F" );
    outtree->Branch("leadPhot_trigMuDR"  , &OUT::leadPhot_trigMuDR , "leadPhot_trigMuDR/F" );
    outtree->Branch("sublPhot_trigMuDR"  , &OUT::sublPhot_trigMuDR , "sublPhot_trigMuDR/F" );
    outtree->Branch("m_leadPhot_leadLep"  , &OUT::m_leadPhot_leadLep , "m_leadPhot_leadLep/F" );
    outtree->Branch("m_leadPhot_trigEl"   , &OUT::m_leadPhot_trigEl  , "m_leadPhot_trigEl/F" );
    outtree->Branch("m_sublPhot_leadLep"  , &OUT::m_sublPhot_leadLep , "m_sublPhot_leadLep/F" );
    outtree->Branch("m_sublPhot_trigEl"   , &OUT::m_sublPhot_trigEl  , "m_sublPhot_trigEl/F" );
    outtree->Branch("m_leadPhot_sublPhot_trigEl"   , &OUT::m_leadPhot_sublPhot_trigEl  , "m_leadPhot_sublPhot_trigEl/F" );
    outtree->Branch("dr_ph1_leadLep"      , &OUT::dr_ph1_leadLep     , "dr_ph1_leadLep/F"     );
    outtree->Branch("dr_ph1_sublLep"      , &OUT::dr_ph1_sublLep     , "dr_ph1_sublLep/F"     );
    outtree->Branch("dr_ph2_leadLep"      , &OUT::dr_ph2_leadLep     , "dr_ph2_leadLep/F"     );
    outtree->Branch("dr_ph2_sublLep"      , &OUT::dr_ph2_sublLep     , "dr_ph2_sublLep/F"     );
    outtree->Branch("dr_ph1_trigEle"      , &OUT::dr_ph1_trigEle     , "dr_ph1_trigEle/F"     );
    outtree->Branch("dr_ph2_trigEle"      , &OUT::dr_ph2_trigEle     , "dr_ph2_trigEle/F"     );
    outtree->Branch("dr_ph1_trigMu"      , &OUT::dr_ph1_trigMu     , "dr_ph1_trigMu/F"     );
    outtree->Branch("dr_ph2_trigMu"      , &OUT::dr_ph2_trigMu     , "dr_ph2_trigMu/F"     );
    outtree->Branch("dphi_ph1_leadLep"      , &OUT::dphi_ph1_leadLep     , "dphi_ph1_leadLep/F"     );
    outtree->Branch("dphi_ph1_sublLep"      , &OUT::dphi_ph1_sublLep     , "dphi_ph1_sublLep/F"     );
    outtree->Branch("dphi_ph2_leadLep"      , &OUT::dphi_ph2_leadLep     , "dphi_ph2_leadLep/F"     );
    outtree->Branch("dphi_ph2_sublLep"      , &OUT::dphi_ph2_sublLep     , "dphi_ph2_sublLep/F"     );
    outtree->Branch("m_ph1_ph2"           , &OUT::m_ph1_ph2          , "m_ph1_ph2/F"          );
    outtree->Branch("dr_ph1_ph2"          , &OUT::dr_ph1_ph2         , "dr_ph1_ph2/F"         );
    outtree->Branch("dphi_ph1_ph2"        , &OUT::dphi_ph1_ph2       , "dphi_ph1_ph2/F"       );
    outtree->Branch("pt_ph1_ph2"          , &OUT::pt_ph1_ph2         , "pt_ph1_ph2/F"         );
    outtree->Branch("m_leadLep_ph1_ph2"   , &OUT::m_leadLep_ph1_ph2  , "m_leadLep_ph1_ph2/F"  );
    outtree->Branch("m_leadLep_ph1"       , &OUT::m_leadLep_ph1      , "m_leadLep_ph1/F"      );
    outtree->Branch("m_leadLep_ph2"       , &OUT::m_leadLep_ph2      , "m_leadLep_ph2/F"      );
    outtree->Branch("m_sublLep_ph1"       , &OUT::m_sublLep_ph1      , "m_sublLep_ph1/F"      );
    outtree->Branch("m_sublLep_ph2"       , &OUT::m_sublLep_ph2      , "m_sublLep_ph2/F"      );
    outtree->Branch("pt_leadph12"         , &OUT::pt_leadph12        , "pt_leadph12/F"        );
    outtree->Branch("pt_sublph12"         , &OUT::pt_sublph12        , "pt_sublph12/F"        );
    outtree->Branch("eta_leadph12"        , &OUT::eta_leadph12       , "eta_leadph12/F"       );
    outtree->Branch("eta_sublph12"        , &OUT::eta_sublph12       , "eta_sublph12/F"       );
    outtree->Branch("hasPixSeed_leadph12" , &OUT::hasPixSeed_leadph12, "hasPixSeed_leadph12/F");
    outtree->Branch("hasPixSeed_sublph12" , &OUT::hasPixSeed_sublph12, "hasPixSeed_sublph12/F");
    outtree->Branch("sieie_leadph12"      , &OUT::sieie_leadph12     , "sieie_leadph12/F"     );
    outtree->Branch("sieie_sublph12"      , &OUT::sieie_sublph12     , "sieie_sublph12/F"     );
    outtree->Branch("chIsoCorr_leadph12"  , &OUT::chIsoCorr_leadph12 , "chIsoCorr_leadph12/F" );
    outtree->Branch("chIsoCorr_sublph12"  , &OUT::chIsoCorr_sublph12 , "chIsoCorr_sublph12/F" );
    outtree->Branch("neuIsoCorr_leadph12" , &OUT::neuIsoCorr_leadph12, "neuIsoCorr_leadph12/F");
    outtree->Branch("neuIsoCorr_sublph12" , &OUT::neuIsoCorr_sublph12, "neuIsoCorr_sublph12/F");
    outtree->Branch("phoIsoCorr_leadph12" , &OUT::phoIsoCorr_leadph12, "phoIsoCorr_leadph12/F");
    outtree->Branch("phoIsoCorr_sublph12" , &OUT::phoIsoCorr_sublph12, "phoIsoCorr_sublph12/F");
    outtree->Branch("isEB_leadph12", &OUT::isEB_leadph12, "isEB_leadph12/O" );
    outtree->Branch("isEB_sublph12", &OUT::isEB_sublph12, "isEB_sublph12/O" );
    outtree->Branch("isEE_leadph12", &OUT::isEE_leadph12, "isEE_leadph12/O" );
    outtree->Branch("isEE_sublph12", &OUT::isEE_sublph12, "isEE_sublph12/O" );
    outtree->Branch("truthMatchPh_leadph12", &OUT::truthMatchPh_leadph12, "truthMatchPh_leadph12/O" );
    outtree->Branch("truthMatchPh_sublph12", &OUT::truthMatchPh_sublph12, "truthMatchPh_sublph12/O" );
    outtree->Branch("truthMatchPhMomPID_leadph12", &OUT::truthMatchPhMomPID_leadph12, "truthMatchPhMomPID_leadph12/O" );
    outtree->Branch("truthMatchPhMomPID_sublph12", &OUT::truthMatchPhMomPID_sublph12, "truthMatchPhMomPID_sublph12/O" );

    outtree->Branch("dphi_met_phot"        , &OUT::dphi_met_phot        );
    outtree->Branch("m_leadLep_phot"       , &OUT::m_leadLep_phot       );
    outtree->Branch("m_sublLep_phot"       , &OUT::m_sublLep_phot       );
    outtree->Branch("m_trigEl_phot"        , &OUT::m_trigEl_phot        );
    outtree->Branch("m_trigMu_phot"        , &OUT::m_trigMu_phot        );
    outtree->Branch("dr_leadLep_phot"      , &OUT::dr_leadLep_phot      );
    outtree->Branch("dr_sublLep_phot"      , &OUT::dr_sublLep_phot      );
    outtree->Branch("dr_trigEl_phot"       , &OUT::dr_trigEl_phot       );
    outtree->Branch("dr_trigMu_phot"       , &OUT::dr_trigMu_phot       );
    outtree->Branch("dphi_leadLep_phot"    , &OUT::dphi_leadLep_phot    );
    outtree->Branch("dphi_sublLep_phot"    , &OUT::dphi_sublLep_phot    );
    outtree->Branch("dphi_trigEl_phot"     , &OUT::dphi_trigEl_phot     );
    outtree->Branch("dphi_trigMu_phot"     , &OUT::dphi_trigMu_phot     );
    outtree->Branch("mt_met_trigEl_phot"   , &OUT::mt_met_trigEl_phot   );
    outtree->Branch("mt_met_trigMu_phot"   , &OUT::mt_met_trigMu_phot   );
    outtree->Branch("m_leplep_phot"        , &OUT::m_leplep_phot        );
    outtree->Branch("m_diphot"             , &OUT::m_diphot             );
    outtree->Branch("dr_diphot"            , &OUT::dr_diphot            );
    outtree->Branch("dphi_diphot"          , &OUT::dphi_diphot          );
    outtree->Branch("pt_diphot"            , &OUT::pt_diphot            );
    outtree->Branch("m_leplep_diphot"      , &OUT::m_leplep_diphot      );
    outtree->Branch("m_trigEl_diphot"      , &OUT::m_trigEl_diphot      );
    outtree->Branch("m_trigMu_diphot"      , &OUT::m_trigMu_diphot      );
    outtree->Branch("mt_met_trigEl_diphot" , &OUT::mt_met_trigEl_diphot );
    outtree->Branch("mt_met_trigMu_diphot" , &OUT::mt_met_trigMu_diphot );

    outtree->Branch("ptSorted_ph_noSIEIEiso533_idx"           , &OUT::ptSorted_ph_noSIEIEiso533_idx );
    outtree->Branch("ptSorted_ph_noSIEIEiso855_idx"           , &OUT::ptSorted_ph_noSIEIEiso855_idx );
    outtree->Branch("ptSorted_ph_noSIEIEiso1077_idx"          , &OUT::ptSorted_ph_noSIEIEiso1077_idx );
    outtree->Branch("ptSorted_ph_noSIEIEiso1299_idx"          , &OUT::ptSorted_ph_noSIEIEiso1299_idx );
    outtree->Branch("ptSorted_ph_noSIEIEiso151111_idx"        , &OUT::ptSorted_ph_noSIEIEiso151111_idx );
    outtree->Branch("ptSorted_ph_noSIEIEiso201616_idx"        , &OUT::ptSorted_ph_noSIEIEiso201616_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso53None_idx"      , &OUT::ptSorted_ph_passSIEIEiso53None_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso85None_idx"      , &OUT::ptSorted_ph_passSIEIEiso85None_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso107None_idx"     , &OUT::ptSorted_ph_passSIEIEiso107None_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso129None_idx"     , &OUT::ptSorted_ph_passSIEIEiso129None_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso1511None_idx"    , &OUT::ptSorted_ph_passSIEIEiso1511None_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso2016None_idx"    , &OUT::ptSorted_ph_passSIEIEiso2016None_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso5None3_idx"      , &OUT::ptSorted_ph_passSIEIEiso5None3_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso8None5_idx"      , &OUT::ptSorted_ph_passSIEIEiso8None5_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso10None7_idx"     , &OUT::ptSorted_ph_passSIEIEiso10None7_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso12None9_idx"     , &OUT::ptSorted_ph_passSIEIEiso12None9_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso15None11_idx"    , &OUT::ptSorted_ph_passSIEIEiso15None11_idx );
    outtree->Branch("ptSorted_ph_passSIEIEiso20None16_idx"    , &OUT::ptSorted_ph_passSIEIEiso20None16_idx );
    outtree->Branch("ptSorted_ph_passSIEIEisoNone33_idx"      , &OUT::ptSorted_ph_passSIEIEisoNone33_idx );
    outtree->Branch("ptSorted_ph_passSIEIEisoNone55_idx"      , &OUT::ptSorted_ph_passSIEIEisoNone55_idx );
    outtree->Branch("ptSorted_ph_passSIEIEisoNone77_idx"      , &OUT::ptSorted_ph_passSIEIEisoNone77_idx );
    outtree->Branch("ptSorted_ph_passSIEIEisoNone99_idx"      , &OUT::ptSorted_ph_passSIEIEisoNone99_idx );
    outtree->Branch("ptSorted_ph_passSIEIEisoNone1111_idx"    , &OUT::ptSorted_ph_passSIEIEisoNone1111_idx );
    outtree->Branch("ptSorted_ph_passSIEIEisoNone1616_idx"    , &OUT::ptSorted_ph_passSIEIEisoNone1616_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso53None_idx"      , &OUT::ptSorted_ph_failSIEIEiso53None_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso85None_idx"      , &OUT::ptSorted_ph_failSIEIEiso85None_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso107None_idx"     , &OUT::ptSorted_ph_failSIEIEiso107None_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso129None_idx"     , &OUT::ptSorted_ph_failSIEIEiso129None_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso1511None_idx"    , &OUT::ptSorted_ph_failSIEIEiso1511None_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso2016None_idx"    , &OUT::ptSorted_ph_failSIEIEiso2016None_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso5None3_idx"      , &OUT::ptSorted_ph_failSIEIEiso5None3_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso8None5_idx"      , &OUT::ptSorted_ph_failSIEIEiso8None5_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso10None7_idx"     , &OUT::ptSorted_ph_failSIEIEiso10None7_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso12None9_idx"     , &OUT::ptSorted_ph_failSIEIEiso12None9_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso15None11_idx"    , &OUT::ptSorted_ph_failSIEIEiso15None11_idx );
    outtree->Branch("ptSorted_ph_failSIEIEiso20None16_idx"    , &OUT::ptSorted_ph_failSIEIEiso20None16_idx );
    outtree->Branch("ptSorted_ph_failSIEIEisoNone33_idx"      , &OUT::ptSorted_ph_failSIEIEisoNone33_idx );
    outtree->Branch("ptSorted_ph_failSIEIEisoNone55_idx"      , &OUT::ptSorted_ph_failSIEIEisoNone55_idx );
    outtree->Branch("ptSorted_ph_failSIEIEisoNone77_idx"      , &OUT::ptSorted_ph_failSIEIEisoNone77_idx );
    outtree->Branch("ptSorted_ph_failSIEIEisoNone99_idx"      , &OUT::ptSorted_ph_failSIEIEisoNone99_idx );
    outtree->Branch("ptSorted_ph_failSIEIEisoNone1111_idx"    , &OUT::ptSorted_ph_failSIEIEisoNone1111_idx );
    outtree->Branch("ptSorted_ph_failSIEIEisoNone1616_idx"    , &OUT::ptSorted_ph_failSIEIEisoNone1616_idx );
    outtree->Branch("ptSorted_ph_mediumNoNeuIsoNoPhoIso_idx"  , &OUT::ptSorted_ph_mediumNoNeuIsoNoPhoIso_idx );
    outtree->Branch("ptSorted_ph_mediumNoChIsoNoPhoIso_idx"   , &OUT::ptSorted_ph_mediumNoChIsoNoPhoIso_idx );
    outtree->Branch("ptSorted_ph_mediumNoChIsoNoNeuIso_idx"   , &OUT::ptSorted_ph_mediumNoChIsoNoNeuIso_idx );
    outtree->Branch("ptSorted_ph_mediumNoSIEIENoPhoIso_idx"   , &OUT::ptSorted_ph_mediumNoSIEIENoPhoIso_idx);
    outtree->Branch("ptSorted_ph_mediumNoSIEIENoNeuIso_idx"   , &OUT::ptSorted_ph_mediumNoSIEIENoNeuIso_idx);
    outtree->Branch("ptSorted_ph_mediumNoSIEIENoChIso_idx"   , &OUT::ptSorted_ph_mediumNoSIEIENoChIso_idx);
    outtree->Branch("ptSorted_ph_mediumNoSIEIENoEleVeto_idx"  , &OUT::ptSorted_ph_mediumNoSIEIENoEleVeto_idx );
    outtree->Branch("ptSorted_ph_mediumNoSIEIEPassPSV_idx"    , &OUT::ptSorted_ph_mediumNoSIEIEPassPSV_idx );
    outtree->Branch("ptSorted_ph_mediumNoSIEIEFailPSV_idx"    , &OUT::ptSorted_ph_mediumNoSIEIEFailPSV_idx );
    outtree->Branch("ptSorted_ph_mediumNoSIEIEPassCSEV_idx"   , &OUT::ptSorted_ph_mediumNoSIEIEPassCSEV_idx );
    outtree->Branch("ptSorted_ph_mediumNoSIEIEFailCSEV_idx"   , &OUT::ptSorted_ph_mediumNoSIEIEFailCSEV_idx );
    outtree->Branch("ptSorted_ph_mediumNoEleVeto_idx"         , &OUT::ptSorted_ph_mediumNoEleVeto_idx );
    outtree->Branch("ptSorted_ph_mediumPassPSV_idx"           , &OUT::ptSorted_ph_mediumPassPSV_idx );
    outtree->Branch("ptSorted_ph_mediumFailPSV_idx"           , &OUT::ptSorted_ph_mediumFailPSV_idx );
    outtree->Branch("ptSorted_ph_mediumPassCSEV_idx"          , &OUT::ptSorted_ph_mediumPassCSEV_idx );
    outtree->Branch("ptSorted_ph_mediumFailCSEV_idx"          , &OUT::ptSorted_ph_mediumFailCSEV_idx );
    outtree->Branch("ptSorted_ph_mediumNoChIsoNoEleVeto_idx"  , &OUT::ptSorted_ph_mediumNoChIsoNoEleVeto_idx );
    outtree->Branch("ptSorted_ph_mediumNoChIsoPassPSV_idx"    , &OUT::ptSorted_ph_mediumNoChIsoPassPSV_idx );
    outtree->Branch("ptSorted_ph_mediumNoChIsoFailPSV_idx"    , &OUT::ptSorted_ph_mediumNoChIsoFailPSV_idx );
    outtree->Branch("ptSorted_ph_mediumNoChIsoPassCSEV_idx"   , &OUT::ptSorted_ph_mediumNoChIsoPassCSEV_idx );
    outtree->Branch("ptSorted_ph_mediumNoChIsoFailCSEV_idx"   , &OUT::ptSorted_ph_mediumNoChIsoFailCSEV_idx );
    outtree->Branch("ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx" , &OUT::ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx );
    outtree->Branch("ptSorted_ph_mediumNoNeuIsoPassPSV_idx"   , &OUT::ptSorted_ph_mediumNoNeuIsoPassPSV_idx );
    outtree->Branch("ptSorted_ph_mediumNoNeuIsoFailPSV_idx"   , &OUT::ptSorted_ph_mediumNoNeuIsoFailPSV_idx );
    outtree->Branch("ptSorted_ph_mediumNoNeuIsoPassCSEV_idx"  , &OUT::ptSorted_ph_mediumNoNeuIsoPassCSEV_idx );
    outtree->Branch("ptSorted_ph_mediumNoNeuIsoFailCSEV_idx"  , &OUT::ptSorted_ph_mediumNoNeuIsoFailCSEV_idx );
    outtree->Branch("ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx" , &OUT::ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx );
    outtree->Branch("ptSorted_ph_mediumNoPhoIsoPassPSV_idx"   , &OUT::ptSorted_ph_mediumNoPhoIsoPassPSV_idx );
    outtree->Branch("ptSorted_ph_mediumNoPhoIsoFailPSV_idx"   , &OUT::ptSorted_ph_mediumNoPhoIsoFailPSV_idx );
    outtree->Branch("ptSorted_ph_mediumNoPhoIsoPassCSEV_idx"  , &OUT::ptSorted_ph_mediumNoPhoIsoPassCSEV_idx );
    outtree->Branch("ptSorted_ph_mediumNoPhoIsoFailCSEV_idx"  , &OUT::ptSorted_ph_mediumNoPhoIsoFailCSEV_idx );

    outtree->Branch("truelep_n", &OUT::truelep_n, "truelep_n/I" );
    outtree->Branch("trueph_n", &OUT::trueph_n, "tureph_n/I"  );
    outtree->Branch("trueph_wmother_n", &OUT::trueph_wmother_n, "trueph_wmother_n/I"  );
    outtree->Branch("truegenph_n", &OUT::truegenph_n, "truegenph_n/I"  );
    outtree->Branch("truegenphpt15_n", &OUT::truegenphpt15_n, "truegenphpt15_n/I"  );
    outtree->Branch("truegenphpt15WZMom", &OUT::truegenphpt15WZMom_n, "truegenphpt15WZMom_n/I"  );
    outtree->Branch("truegenphpt15LepMom_n", &OUT::truegenphpt15LepMom_n, "truegenphpt15LepMom_n/I"  );
    outtree->Branch("truegenphpt15QMom_n", &OUT::truegenphpt15QMom_n, "truegenphpt15QMom_n/I"  );

    outtree->Branch("truelep_pt", &OUT::truelep_pt );
    outtree->Branch("truelep_eta", &OUT::truelep_eta );
    outtree->Branch("truelep_phi", &OUT::truelep_phi );
    outtree->Branch("truelep_e", &OUT::truelep_e );
    outtree->Branch("truelep_isElec", &OUT::truelep_isElec );
    outtree->Branch("truelep_isMuon", &OUT::truelep_isMuon );
    outtree->Branch("truelep_motherPID", &OUT::truelep_motherPID );
    outtree->Branch("trueph_pt", &OUT::trueph_pt );
    outtree->Branch("trueph_eta", &OUT::trueph_eta );
    outtree->Branch("trueph_phi", &OUT::trueph_phi);
    outtree->Branch("trueph_motherPID", &OUT::trueph_motherPID );
    outtree->Branch("trueph_parentage", &OUT::trueph_parentage);
    outtree->Branch("trueph_nearestLepDR", &OUT::trueph_nearestLepDR);
    outtree->Branch("trueph_nearestQrkDR", &OUT::trueph_nearestQrkDR);

    outtree->Branch("trueW_pt"  , &OUT::trueW_pt  );
    outtree->Branch("trueW_eta" , &OUT::trueW_eta );
    outtree->Branch("trueW_phi" , &OUT::trueW_phi );
    outtree->Branch("trueW_e"   , &OUT::trueW_e   );

    outtree->Branch("trueleadlep_pt"  , &OUT::trueleadlep_pt  , "trueleadlep_pt/F"    );
    outtree->Branch("truesubllep_pt"   , &OUT::truesubllep_pt   , "truesubllep_pt/F"     );
    outtree->Branch("true_m_leplep"   , &OUT::true_m_leplep, "true_m_leplep/F"     );
    outtree->Branch("trueleadlep_leadPhotDR"   , &OUT::trueleadlep_leadPhotDR, "trueleadlep_leadPhotDR/F"     );
    outtree->Branch("trueleadlep_sublPhotDR"   , &OUT::trueleadlep_sublPhotDR, "trueleadlep_sublPhotDR/F"     );
    outtree->Branch("truesubllep_leadPhotDR"   , &OUT::truesubllep_leadPhotDR, "truesubllep_leadPhotDR/F"     );
    outtree->Branch("truesubllep_sublPhotDR"   , &OUT::truesubllep_sublPhotDR, "truesubllep_sublPhotDR/F"     );

    outtree->Branch("truephph_dr"   , &OUT::truephph_dr   , "truephph_dr/F"     );
    outtree->Branch("truephph_dphi" , &OUT::truephph_dphi , "truephph_dphi/F"     );
    outtree->Branch("truephph_m"    , &OUT::truephph_m    , "truephph_m/F"     );
    outtree->Branch("truelepphph_m"    , &OUT::truelepphph_m    , "truelepphph_m/F"     );

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
    
        if( mod_conf.GetName() == "FilterBlind" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "isData" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string data = eitr->second;
                std::transform(data.begin(), data.end(), data.begin(), ::tolower);
                if( data=="true") _isData=true;
                else              _isData=false;
            }
        }

        if( mod_conf.GetName() == "FilterElectron" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "PtScaleDownBarrel" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _elPtScaleDownBarrel) {
                    _doElPtScaleDown = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "PtScaleDownEndcap" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _elPtScaleDownEndcap) {
                    _doElPtScaleDown = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "PtScaleUpBarrel" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _elPtScaleUpBarrel) {
                    _doElPtScaleUp = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "PtScaleUpEndcap" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _elPtScaleUpEndcap) {
                    _doElPtScaleUp = true;
                }
            }
        }
        if( mod_conf.GetName() == "FilterPhoton" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "sort_by_id" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string data = eitr->second;
                std::transform(data.begin(), data.end(), data.begin(), ::tolower);
                if( data=="true") sort_photons_by_id=true;
                else              sort_photons_by_id=false;
            }
            eitr = mod_conf.GetInitData().find( "PtScaleDownBarrel" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _phPtScaleDownBarrel) {
                    _doPhPtScaleDown = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "PtScaleDownEndcap" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _phPtScaleDownEndcap) {
                    _doPhPtScaleDown = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "PtScaleUpBarrel" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _phPtScaleUpBarrel) {
                    _doPhPtScaleUp = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "PtScaleUpEndcap" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _phPtScaleUpEndcap) {
                    _doPhPtScaleUp = true;
                }
            }
        }

        if( mod_conf.GetName() == "FilterMuon" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "PtScaleDownBarrel" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _muPtScaleDownBarrel) {
                    _doMuPtScaleDown = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "PtScaleDownEndcap" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _muPtScaleDownEndcap) {
                    _doMuPtScaleDown = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "PtScaleUpBarrel" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _muPtScaleUpBarrel) {
                    _doMuPtScaleUp = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "PtScaleUpEndcap" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::stringstream ss(eitr->second);
                if(ss >> _muPtScaleUpEndcap) {
                    _doMuPtScaleUp = true;
                }
            }
        }
    }

    if( _doMuPtScaleUp && (_muPtScaleUpEndcap < 0 || _muPtScaleUpBarrel < 0) ) {
        std::cout << "ERROR -- Mu scale variations not properly set" << std::endl;
    }
    if( _doMuPtScaleDown && (_muPtScaleDownEndcap < 0 || _muPtScaleDownBarrel < 0) ) {
        std::cout << "ERROR -- Mu scale variations not properly set" << std::endl;
    }

    if( _doElPtScaleUp && (_elPtScaleUpEndcap < 0 || _elPtScaleUpBarrel < 0) ) {
        std::cout << "ERROR -- El scale variations not properly set" << std::endl;
    }
    if( _doElPtScaleDown && (_elPtScaleDownEndcap < 0 || _elPtScaleDownBarrel < 0) ) {
        std::cout << "ERROR -- El scale variations not properly set" << std::endl;
    }

    if( _doPhPtScaleUp && (_phPtScaleUpEndcap < 0 || _phPtScaleUpBarrel < 0) ) {
        std::cout << "ERROR -- Ph scale variations not properly set" << std::endl;
    }
    if( _doPhPtScaleDown && (_phPtScaleDownEndcap < 0 || _phPtScaleDownBarrel < 0) ) {
        std::cout << "ERROR -- Ph scale variations not properly set" << std::endl;
    }

}
   

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    CopyInputVarsToOutput();

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        save_event &= ApplyModule( mod_conf );
    }

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    // This bool is used for filtering
    // If a module implements an event filter
    // update this variable and return it
    // to apply the filter
    bool keep_evt = true;

    // This part is a bit hacked.  For each module that
    // you write below, you have to put a call to that
    // function with a matching name here.
    // The name is used to match the name used
    // in the python configuration.
    // There are fancy ways to do this, but it
    // would require the code to be much more complicated
    //
    if( config.GetName() == "FilterElectron" ) {
        FilterElectron( config );
    }
    if( config.GetName() == "FilterMuon" ) {
        FilterMuon( config );
    }

    //----------------------------------
    // Reorder the photons 
    // if requested.  Only one
    // module should be used otherwise
    // one will override the other
    if( config.GetName() == "SortPhotonByMVAScore" ) {
        SortPhotonByMVAScore( config );
    }
    //----------------------------------
    // Now select photons
    if( config.GetName() == "FilterPhoton" ) {
        FilterPhoton( config );
    }
    //----------------------------------

    if( config.GetName() == "FilterJet" ) {
        FilterJet( config );
    }
    if( config.GetName() == "BuildTruth" ) {
        BuildTruth( config );
    }
    // If the module applies a filter the filter decision
    // is passed back to here.  There is no requirement
    // that a function returns a bool, but
    // if you want the filter to work you need to do this
    //
    // Example :
    if( config.GetName() == "CalcEventVars" ) {
        CalcEventVars( config );
    }

    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }
    if( config.GetName() == "FilterBlind" ) {
        keep_evt &= FilterBlind( config );
    }
    if( config.GetName() == "FilterTruth" ) {
        keep_evt &= FilterTruth( config );
    }

    return keep_evt;

}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//
// Examples :

// This is an example of a module that applies an
// event filter.  Note that it returns a bool instead
// of a void.  In principle the modules can return any
// type of variable, you just have to handle it
// in the ApplyModule function

void RunModule::FilterElectron( ModuleConfig & config ) const {

    #ifdef EXISTS_el_n
    OUT::el_n = 0;
    ClearOutputPrefix("el_");

    // save which photon overlaps with 
    // electrons
    std::vector<Bool_t> ph_matches_ele( OUT::ph_n, 0 );
    for( int idx = 0; idx < IN::el_n; idx++ ) {

        float elPt = IN::el_pt->at(idx);
        if( _doElPtScaleUp ) {
            if( fabs(IN::el_eta->at(idx)) < 1.44 ) {
                elPt = elPt*_elPtScaleUpBarrel;
            }
            else {
                elPt = elPt*_elPtScaleUpEndcap;
            }
        }
        if( _doElPtScaleDown ) {
            if( fabs(IN::el_eta->at(idx)) < 1.44 ) {
                elPt = elPt*_elPtScaleDownBarrel;
            }
            else {
                elPt = elPt*_elPtScaleDownEndcap;
            }
        }


        if( !config.PassFloat( "cut_el_pt", elPt) ) continue;

        if( !config.PassBool( "cut_el_loose", IN::el_passLoose->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_medium", IN::el_passMedium->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_tight", IN::el_passTight->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_tightTrig", IN::el_passTightTrig->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_mvaTrig", IN::el_passMvaTrig->at(idx)) ) continue;

        // before making the mvaNonTrigCut, first check
        // that the electron is not a triggered electron
        if( ! ( IN::el_triggerMatch->at(idx) && IN::el_passMvaTrig->at(idx) ) ) {
            if( !config.PassBool( "cut_el_mvaNonTrig", IN::el_passMvaNonTrig->at(idx)) ) continue;
        }

        TLorentzVector el;
        el.SetPtEtaPhiE( IN::el_pt->at(idx), IN::el_eta->at(idx), IN::el_phi->at(idx), IN::el_e->at(idx ) );
        // remove electrons that overlap with photons
        float mindr = 100.;
        for( int pidx = 0 ; pidx < OUT::ph_n; pidx++ ) {

            TLorentzVector phlv;
            phlv.SetPtEtaPhiM( OUT::ph_pt->at(pidx), 
                               OUT::ph_eta->at(pidx),
                               OUT::ph_phi->at(pidx),
                               0.0 );
        
            float dr = phlv.DeltaR(el);
            if( dr < mindr ) {
                mindr = dr;
            }
            if( dr < 0.4 ) {
                ph_matches_ele[pidx] = 1;
            }
        }


        if( !config.PassFloat( "cut_ph_el_dr", mindr ) ) continue;


        mindr = 100.;
        // Remove electrons that overlap with muons
        for( int muidx = 0 ; muidx < OUT::mu_n; muidx++ ) {
            TLorentzVector mu;
            mu.SetPtEtaPhiE( OUT::mu_pt->at(muidx), OUT::mu_eta->at(muidx), OUT::mu_phi->at(muidx), OUT::mu_e->at(muidx ) );
            float dr = el.DeltaR(mu);
            if( dr < mindr ) {
                mindr = dr;
            }
        }

        if( !config.PassFloat( "cut_mu_el_dr", mindr ) ) continue;
        
        CopyPrefixIndexBranchesInToOut( "el_", idx );
        OUT::el_pt->pop_back();
        OUT::el_pt->push_back(elPt);

        OUT::el_n++;

    }

    // store if the photon matched an 
    // electron
            
    #endif

}

void RunModule::FilterPhoton( ModuleConfig & config ) const {

    #ifdef EXISTS_ph_n

    OUT::ph_n = 0;
    ClearOutputPrefix("ph_");

    std::vector<int> ph_order;
    if( sort_photons_by_id ) {
        ph_order = get_ph_sorted_by_id( );
    }
    else {
        for( int idx = 0; idx < IN::ph_n; idx++ ) {
            ph_order.push_back(idx);
        }
    }

    BOOST_FOREACH( int idx, ph_order )  {

        float phPt = IN::ph_pt->at(idx);
        if( _doPhPtScaleUp ) {
            if( fabs(IN::ph_sceta->at(idx)) < 1.47 ) {
                phPt = phPt*_phPtScaleUpBarrel;
            }
            else {
                phPt = phPt*_phPtScaleUpEndcap;
            }
        }
        if( _doPhPtScaleDown ) {
            if( fabs(IN::ph_eta->at(idx)) < 1.47 ) {
                phPt = phPt*_phPtScaleDownBarrel;
            }
            else {
                phPt = phPt*_phPtScaleDownEndcap;
            }
        }

        float ph_sceta = fabs( IN::ph_sceta->at(idx) );

        if( !config.PassFloat( "cut_ph_pt", phPt) ) continue;
        if( !config.PassFloat( "cut_ph_abseta", ph_sceta) ) continue;
        if( !config.PassFloat( "cut_ph_abseta_crack", ph_sceta) ) continue;
        if( !config.PassBool( "cut_ph_eleVeto", IN::ph_eleVeto->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_hasPixSeed", IN::ph_hasPixSeed->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_loose", IN::ph_passLoose->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_looseNoSIEIE", IN::ph_passLooseNoSIEIE->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_medium", IN::ph_passMedium->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_tight", IN::ph_passTight->at(idx)) ) continue;

        //if( IN::ph_hasSLConv->at(idx) ) {
        //    if( !config.PassBool( "cut_ph_eleVetoSLConv", IN::ph_eleVeto->at(idx) ) ) continue;
        //}
        //else {
        //    if( !config.PassBool( "cut_ph_eleVetoNotSLConv", IN::ph_eleVeto->at(idx) ) ) continue;
        //}


        // electron overlap removal
        TLorentzVector phlv;
        phlv.SetPtEtaPhiE( IN::ph_pt->at(idx), 
                           IN::ph_eta->at(idx), 
                           IN::ph_phi->at(idx), 
                           IN::ph_e->at(idx) );

        float min_el_dr = 100.0;
        float min_trigel_dr = 100.0;
        bool found_trigel = false;

        for( int eidx = 0; eidx < OUT::el_n; eidx++ ) {
            TLorentzVector ellv;
            ellv.SetPtEtaPhiE( OUT::el_pt->at(eidx), 
                               OUT::el_eta->at(eidx), 
                               OUT::el_phi->at(eidx), 
                               OUT::el_e->at(eidx) );

            float dr = phlv.DeltaR( ellv );
            if( dr < min_el_dr ) {
                min_el_dr = dr;
            }

            // count the leading trigger
            // matched electron which
            // will be the first in the list
            if( OUT::el_triggerMatch->at(eidx) && OUT::el_passMvaTrig->at(eidx) && ellv.Pt() > 30 && dr < min_trigel_dr ) {
                if( !found_trigel ) {
                    min_trigel_dr = dr;
                    found_trigel = true;
                }
            }
        }

        float min_mu_dr = 100.0;
        for( int midx = 0; midx < OUT::mu_n; midx++ ) {
            TLorentzVector mulv;
            mulv.SetPtEtaPhiM( OUT::mu_pt->at(midx), 
                               OUT::mu_eta->at(midx), 
                               OUT::mu_phi->at(midx), 
                               0.106 );

            float dr = phlv.DeltaR( mulv );
            if( dr < min_mu_dr ) {
                min_mu_dr = dr;
            }
        }

        float min_ph_dr = 100.0;
        BOOST_FOREACH( int pidx2, ph_order )  {
            if( pidx2 == idx ) continue;
            TLorentzVector phlv2;
            phlv2.SetPtEtaPhiE( IN::ph_pt->at(pidx2), 
                                IN::ph_eta->at(pidx2),
                                IN::ph_phi->at(pidx2),
                                IN::ph_e->at(pidx2)
                               );

            float dr = phlv.DeltaR( phlv2 );
            if( dr < min_ph_dr && phlv2.Pt() > phlv.Pt() ) {
                min_ph_dr = dr;
            }
        }

        if( !config.PassFloat( "cut_el_ph_dr", min_el_dr ) ) continue;
        if( !config.PassFloat( "cut_trigel_ph_dr", min_trigel_dr) ) continue;
        if( !config.PassFloat( "cut_mu_ph_dr", min_mu_dr ) ) continue;
        if( !config.PassFloat( "cut_ph_ph_dr", min_ph_dr ) ) continue;

        CopyPrefixIndexBranchesInToOut( "ph_", idx );
        OUT::ph_pt->pop_back();
        OUT::ph_pt->push_back(phPt);

        OUT::ph_n++;

    }
    #endif
}

//------------------------------------------
// DEPRICATED, sort iside of Filter Photon
void RunModule::SortPhotonByMVAScore( ModuleConfig & config ) const {

    #ifdef EXISTS_ph_n

    // clear all
    OUT::ph_n = 0;
    ClearOutputPrefix("ph_");

    std::vector<std::pair<float, int> > sorted_photons;
    for( int idx = 0; idx < IN::ph_n; idx++ ) {

        sorted_photons.push_back( std::make_pair( IN::ph_mvascore->at(idx), idx ) );

    }

    std::sort(sorted_photons.rbegin(), sorted_photons.rend());

    for( unsigned int idx = 0; idx < sorted_photons.size(); idx++ ) {

        int sidx = sorted_photons[idx].second;

        CopyPrefixIndexBranchesInToOut( "ph_", sidx );
        OUT::ph_n++;

    }
    #endif

}

std::vector<int> RunModule::get_ph_sorted_by_id( ) const {

    std::vector<std::pair<int, int> > sorted_photons;
    for( int idx = 0; idx < IN::ph_n; idx++ ) {

        int sort_val = 0;
        if( IN::ph_passMedium->at(idx) ) {
            sort_val = 7;
        }
        else if( IN::ph_chIsoCorr->at(idx) < 5  && IN::ph_neuIsoCorr->at(idx) < 3  && IN::ph_phoIsoCorr->at(idx) < 3 ) {
            sort_val = 6;
        }
        else if( IN::ph_chIsoCorr->at(idx) < 8  && IN::ph_neuIsoCorr->at(idx) < 5  && IN::ph_phoIsoCorr->at(idx) < 5 ) {
            sort_val = 5;
        }
        else if( IN::ph_chIsoCorr->at(idx) < 10 && IN::ph_neuIsoCorr->at(idx) < 7  && IN::ph_phoIsoCorr->at(idx) < 7 ) {
            sort_val = 4;
        }
        else if( IN::ph_chIsoCorr->at(idx) < 12 && IN::ph_neuIsoCorr->at(idx) < 9  && IN::ph_phoIsoCorr->at(idx) < 9 ) {
            sort_val = 3;
        }
        else if( IN::ph_chIsoCorr->at(idx) < 15 && IN::ph_neuIsoCorr->at(idx) < 11 && IN::ph_phoIsoCorr->at(idx) < 11 ) {
            sort_val = 2;
        }
        else if( IN::ph_chIsoCorr->at(idx) < 20 && IN::ph_neuIsoCorr->at(idx) < 16 && IN::ph_phoIsoCorr->at(idx) < 16 ) {
            sort_val = 1;
        }

        sorted_photons.push_back( std::make_pair( sort_val, idx ) );
    }

    std::sort(sorted_photons.rbegin(), sorted_photons.rend());

    std::vector<int> sorted_idx;
    for( std::vector<std::pair<int,int> >::const_iterator itr = sorted_photons.begin() ; itr != sorted_photons.end(); ++itr) {
        sorted_idx.push_back( itr->second );
    }
    
    return sorted_idx;


}


void RunModule::FilterMuon( ModuleConfig & config ) const {

    #ifdef EXISTS_mu_n
    OUT::mu_n = 0;
    ClearOutputPrefix("mu_");

    for( int idx = 0; idx < IN::mu_n; idx++ ) {


        float muPt = IN::mu_pt->at(idx);
        if( _doMuPtScaleUp ) {
            if( fabs(IN::mu_eta->at(idx)) < 1.0 ) {
                muPt = muPt*_muPtScaleUpBarrel;
            }
            else {
                muPt = muPt*_muPtScaleUpEndcap;
            }
        }
        if( _doMuPtScaleDown ) {
            if( fabs(IN::mu_eta->at(idx)) < 1.0 ) {
                muPt = muPt*_muPtScaleDownBarrel;
            }
            else {
                muPt = muPt*_muPtScaleDownEndcap;
            }
        }

        if( !config.PassFloat( "cut_mu_pt", muPt) ) continue;
        if( !config.PassFloat( "cut_mu_eta", fabs(IN::mu_eta->at(idx) ) ) ) continue;
        if( !config.PassFloat( "cut_mu_corriso", IN::mu_corrIso->at(idx)/IN::mu_pt->at(idx)) ) continue;
        if( !config.PassBool( "cut_mu_passTight", IN::mu_passTight->at(idx)) ) continue;
        if( !config.PassBool( "cut_mu_passTightNoIso", IN::mu_passTightNoIso->at(idx)) ) continue;
        if( !config.PassBool( "cut_mu_passTightNoD0", IN::mu_passTightNoD0->at(idx)) ) continue;
        if( !config.PassBool( "cut_mu_passTightNoIsoNoD0", IN::mu_passTightNoIsoNoD0->at(idx)) ) continue;

        CopyPrefixIndexBranchesInToOut( "mu_", idx );
        OUT::mu_pt->pop_back();
        OUT::mu_pt->push_back(muPt);
        OUT::mu_n++;

    }

    #endif
}

void RunModule::BuildTruth( ModuleConfig & config ) const {

    OUT::truelep_n        = 0;
    OUT::trueph_n         = 0;
    OUT::trueW_n         = 0;
    OUT::trueph_wmother_n = 0;
    OUT::truegenph_n = 0;
    OUT::truegenphpt15_n = 0;
    OUT::truegenphpt15WZMom_n= 0;
    OUT::truegenphpt15LepMom_n= 0;
    OUT::truegenphpt15QMom_n= 0;

    OUT::truelep_pt        -> clear();
    OUT::truelep_eta       -> clear();
    OUT::truelep_phi       -> clear();
    OUT::truelep_e         -> clear();
    OUT::truelep_isElec    -> clear();
    OUT::truelep_isMuon    -> clear();
    OUT::truelep_motherPID -> clear();

    OUT::trueph_pt         -> clear();
    OUT::trueph_eta        -> clear();
    OUT::trueph_phi        -> clear();
    OUT::trueph_motherPID  -> clear();
    OUT::trueph_parentage  -> clear();
    OUT::trueph_nearestLepDR   -> clear();
    OUT::trueph_nearestQrkDR   -> clear();

    OUT::trueW_pt           -> clear();
    OUT::trueW_eta          -> clear();
    OUT::trueW_phi          -> clear();
    OUT::trueW_e            -> clear();
    
    OUT::trueleadlep_pt    = 0;
    OUT::truesubllep_pt    = 0;
    OUT::true_m_leplep    = 0;

    OUT::trueleadlep_leadPhotDR    = 0;
    OUT::trueleadlep_sublPhotDR    = 0;
    OUT::truesubllep_leadPhotDR    = 0;
    OUT::truesubllep_sublPhotDR    = 0;

    OUT::truephph_dr = 0;
    OUT::truephph_dphi = 0;
    OUT::truephph_m = 0;
    OUT::truelepphph_m= 0;

    std::vector<int> accept_pid_lep;
    std::vector<int> accept_MotherPid_lep;
    std::vector<int> accept_pid_tau;
    std::vector<int> accept_pid_ph;
    accept_pid_lep.push_back(11);
    accept_pid_lep.push_back(13);
    accept_MotherPid_lep.push_back(15);
    accept_MotherPid_lep.push_back(23);
    accept_MotherPid_lep.push_back(24);
    accept_pid_tau.push_back(15);
    accept_pid_ph.push_back(22);
    #ifdef EXISTS_nMC
    std::vector< std::pair<float, int> > sorted_leptons;
    std::vector< std::pair<float, int> > sorted_photons;
    std::vector< std::pair<float, int> > sorted_genphotons;
    std::vector< TLorentzVector > leptons;
    std::vector< TLorentzVector > photons;
    std::vector< TLorentzVector > genphotons;
    int lepidx = 0;
    int phidx = 0;
    int genphidx = 0;

    for( int idx = 0; idx < IN::nMC; ++idx ) {

        if( IN::mcStatus->at(idx) == 1 && std::find(accept_pid_lep.begin(), accept_pid_lep.end(), abs(IN::mcPID->at(idx)) ) != accept_pid_lep.end() && std::find(accept_MotherPid_lep.begin(), accept_MotherPid_lep.end(), abs(IN::mcMomPID->at(idx)) ) != accept_MotherPid_lep.end() ) {

            float pt  = IN::mcPt->at(idx);
            float eta = IN::mcEta->at(idx);
            float phi = IN::mcPhi->at(idx);
            float en  = IN::mcE->at(idx);

            TLorentzVector leplv;
            leplv.SetPtEtaPhiE( pt, eta, phi, en);
            leptons.push_back(leplv);
            sorted_leptons.push_back( std::make_pair( pt, lepidx ) );
            lepidx++;

            OUT::truelep_pt        -> push_back( pt    );
            OUT::truelep_eta       -> push_back( eta   );
            OUT::truelep_phi       -> push_back( phi   );
            OUT::truelep_e         -> push_back( en   );
            OUT::truelep_motherPID -> push_back(IN::mcMomPID->at(idx) );


            if( abs(IN::mcPID->at(idx)) == 11 ) {
                OUT::truelep_isElec->push_back(true);
            }
            else {                           
                OUT::truelep_isElec->push_back(false);
            }

            if( abs(IN::mcPID->at(idx)) == 13 ) {
                OUT::truelep_isMuon->push_back(true);
            }
            else {                           
                OUT::truelep_isMuon->push_back(false);
            }

            OUT::truelep_n++;
        }
        else if( IN::mcStatus->at(idx) == 3 && std::find(accept_pid_tau.begin(), accept_pid_tau.end(), abs(IN::mcPID->at(idx)) ) != accept_pid_tau.end() ) {

            OUT::truelep_pt        -> push_back(IN::mcPt->at(idx)     );
            OUT::truelep_eta       -> push_back(IN::mcEta->at(idx)    );
            OUT::truelep_phi       -> push_back( IN::mcPhi->at(idx)   );
            OUT::truelep_e         -> push_back( IN::mcE->at(idx)   );
            OUT::truelep_motherPID -> push_back(IN::mcMomPID->at(idx) );

            OUT::truelep_isElec->push_back(false);
            OUT::truelep_isMuon->push_back(false);

            OUT::truelep_n++;

        }
            
    }

    //now build photons
    for( int idx = 0; idx < IN::nMC; ++idx ) {

        if( IN::mcStatus->at(idx) == 1 &&  std::find(accept_pid_ph.begin(), accept_pid_ph.end(), abs(IN::mcPID->at(idx)) ) != accept_pid_ph.end() ) {

            float pt  = IN::mcPt->at(idx);
            float eta = IN::mcEta->at(idx);
            float phi = IN::mcPhi->at(idx);

            TLorentzVector phlv;
            phlv.SetPtEtaPhiM( pt, eta, phi, 0);
            photons.push_back(phlv);
            sorted_photons.push_back( std::make_pair( pt, phidx ) );
            phidx++;

            if( abs(IN::mcMomPID->at(idx)) == 24 ) OUT::trueph_wmother_n++;
            if( abs(IN::mcMomPID->at(idx)) < 25  ) {
                OUT::truegenph_n++;
                genphotons.push_back( phlv );
                sorted_genphotons.push_back( std::make_pair( pt, genphidx ) );
                genphidx++;
            }
            if( abs(IN::mcMomPID->at(idx)) < 25 && IN::mcPt->at(idx)>15 ) { 
                OUT::truegenphpt15_n++;
                if( abs(IN::mcMomPID->at(idx)) == 24 || abs(IN::mcMomPID->at(idx)) == 23 ) {
                    OUT::truegenphpt15WZMom_n++;
                }
                else if( abs(IN::mcMomPID->at(idx)) > 10 && abs(IN::mcMomPID->at(idx)) < 14 ) {
                    OUT::truegenphpt15LepMom_n++;
                }
                else if( abs(IN::mcMomPID->at(idx)) < 6 ) {
                    OUT::truegenphpt15QMom_n++;
                }

            }

            if( abs(IN::mcMomPID->at(idx)) < 25 && IN::mcPt->at(idx)>15 ) { 
                OUT::trueph_pt        -> push_back(pt    );
                OUT::trueph_eta       -> push_back(eta    );
                OUT::trueph_phi       -> push_back(phi    );
                OUT::trueph_motherPID -> push_back(IN::mcMomPID->at(idx) );
                OUT::trueph_parentage -> push_back(IN::mcParentage->at(idx) );

                float lepminDR = 100;
                for( int lidx = 0; lidx < OUT::truelep_n; lidx++ ) {

                    TLorentzVector leplv;
                    leplv.SetPtEtaPhiE( OUT::truelep_pt->at(lidx), 
                                        OUT::truelep_eta->at(lidx),
                                        OUT::truelep_phi->at(lidx),
                                        OUT::truelep_e->at(lidx) );

                    float dr = leplv.DeltaR( phlv );
                    if( dr < lepminDR ) {
                        lepminDR = dr;
                    }
                }

                OUT::trueph_nearestLepDR-> push_back( lepminDR );

                float qrkminDR = 100;

                for( int mcidx = 0; mcidx < IN::nMC; mcidx++ ) {

                    if( fabs( IN::mcPID->at(mcidx) ) > 5 ) continue;

                    TLorentzVector qrklv;
                    qrklv.SetPtEtaPhiE( IN::mcPt->at(mcidx), 
                                        IN::mcEta->at(mcidx),
                                        IN::mcPhi->at(mcidx),
                                        IN::mcE->at(mcidx) );

                    if( qrklv.Pt() < 0.001 ) continue;

                    float dr = qrklv.DeltaR( phlv );
                    if( dr < qrkminDR ) {
                        qrkminDR = dr;
                    }
                }

                OUT::trueph_nearestQrkDR-> push_back( qrkminDR );

                OUT::trueph_n++;
            }
        }
        if( IN::mcStatus->at(idx) == 3 && abs(IN::mcPID->at(idx)) == 24 ) {
            OUT::trueW_pt  ->push_back( IN::mcPt->at(idx) );
            OUT::trueW_eta ->push_back( IN::mcEta->at(idx) );
            OUT::trueW_phi ->push_back( IN::mcPhi->at(idx) );
            OUT::trueW_e   ->push_back( IN::mcE->at(idx) );

            OUT::trueW_n++;
        }

    } //end loop over all MC particles

    std::sort(sorted_leptons.rbegin(), sorted_leptons.rend());
    std::sort(sorted_photons.rbegin(), sorted_photons.rend());
    std::sort(sorted_genphotons.rbegin(), sorted_genphotons.rend());


    // calculate event variables
    if( leptons.size() > 0 ) {
        OUT::trueleadlep_pt = sorted_leptons[0].first;

        if( genphotons.size() > 0 ) {
            OUT::trueleadlep_leadPhotDR = leptons[sorted_leptons[0].second].DeltaR(genphotons[sorted_genphotons[0].second]);
        }
        if( genphotons.size() > 1 ) {
            OUT::trueleadlep_sublPhotDR = leptons[sorted_leptons[0].second].DeltaR(genphotons[sorted_genphotons[1].second]);
        }
        if( leptons.size() > 1 ) {
            OUT::truesubllep_pt = sorted_leptons[1].first;
            OUT::true_m_leplep = (leptons[sorted_leptons[0].second] + leptons[sorted_leptons[1].second]).M();
            if( genphotons.size() > 0 ) {
                OUT::truesubllep_leadPhotDR = leptons[sorted_leptons[1].second].DeltaR(genphotons[sorted_genphotons[0].second]);
            }
            if( genphotons.size() > 1 ) {
                OUT::truesubllep_sublPhotDR = leptons[sorted_leptons[1].second].DeltaR(genphotons[sorted_genphotons[1].second]);
            }
        }
    }
    if( genphotons.size() > 1 ) {

        OUT::truephph_dr = genphotons[0].DeltaR( genphotons[1] );
        OUT::truephph_dphi = genphotons[0].DeltaPhi( genphotons[1] );
        OUT::truephph_m = (genphotons[0] + genphotons[1] ).M();
        if( leptons.size() > 0 ) {
            OUT::truelepphph_m = (genphotons[0] + genphotons[1] + leptons[sorted_leptons[0].second]).M();
        }
    }

    #endif


}

bool RunModule::FilterTruth( ModuleConfig & config ) const {

    int nEl = 0;
    int nMu = 0;
    int nTau = 0;

    bool keep_evt = true;

    for(int idx = 0; idx < OUT::truelep_n; ++idx) {
        if( OUT::truelep_isElec->at(idx) ) nEl++;
        else if( OUT::truelep_isMuon->at(idx) ) nMu++;
        else nTau++;
    }

    if( !config.PassInt( "cut_nTrueEl", nEl ) )  keep_evt = false;
    if( !config.PassInt( "cut_nTrueMu", nEl ) )  keep_evt = false;
    if( !config.PassInt( "cut_nTrueTau", nEl ) ) keep_evt = false;

    return keep_evt;

}



void RunModule::CalcEventVars( ModuleConfig & config ) const {

    OUT::mu_pt25_n                    = 0;
    OUT::mu_passtrig_n                = 0;
    OUT::mu_passtrig25_n              = 0;
    OUT::el_pt25_n                    = 0;
    OUT::el_passtrig_n                = 0;
    OUT::el_passtrigL_n               = 0;
    OUT::el_passtrig28_n              = 0;
    OUT::ph_noSIEIEiso533_n           = 0;
    OUT::ph_noSIEIEiso855_n           = 0;
    OUT::ph_noSIEIEiso1077_n          = 0;
    OUT::ph_noSIEIEiso1299_n          = 0;
    OUT::ph_noSIEIEiso151111_n        = 0;
    OUT::ph_noSIEIEiso201616_n        = 0;
    OUT::ph_passSIEIEiso53None_n      = 0;
    OUT::ph_passSIEIEiso85None_n      = 0;
    OUT::ph_passSIEIEiso107None_n     = 0;
    OUT::ph_passSIEIEiso129None_n     = 0;
    OUT::ph_passSIEIEiso1511None_n    = 0;
    OUT::ph_passSIEIEiso2016None_n    = 0;
    OUT::ph_passSIEIEiso5None3_n      = 0;
    OUT::ph_passSIEIEiso8None5_n      = 0;
    OUT::ph_passSIEIEiso10None7_n     = 0;
    OUT::ph_passSIEIEiso12None9_n     = 0;
    OUT::ph_passSIEIEiso15None11_n    = 0;
    OUT::ph_passSIEIEiso20None16_n    = 0;
    OUT::ph_passSIEIEisoNone33_n      = 0;
    OUT::ph_passSIEIEisoNone55_n      = 0;
    OUT::ph_passSIEIEisoNone77_n      = 0;
    OUT::ph_passSIEIEisoNone99_n      = 0;
    OUT::ph_passSIEIEisoNone1111_n    = 0;
    OUT::ph_passSIEIEisoNone1616_n    = 0;
    OUT::ph_failSIEIEiso53None_n      = 0;
    OUT::ph_failSIEIEiso85None_n      = 0;
    OUT::ph_failSIEIEiso107None_n     = 0;
    OUT::ph_failSIEIEiso129None_n     = 0;
    OUT::ph_failSIEIEiso1511None_n    = 0;
    OUT::ph_failSIEIEiso2016None_n    = 0;
    OUT::ph_failSIEIEiso5None3_n      = 0;
    OUT::ph_failSIEIEiso8None5_n      = 0;
    OUT::ph_failSIEIEiso10None7_n     = 0;
    OUT::ph_failSIEIEiso12None9_n     = 0;
    OUT::ph_failSIEIEiso15None11_n    = 0;
    OUT::ph_failSIEIEiso20None16_n    = 0;
    OUT::ph_failSIEIEisoNone33_n      = 0;
    OUT::ph_failSIEIEisoNone55_n      = 0;
    OUT::ph_failSIEIEisoNone77_n      = 0;
    OUT::ph_failSIEIEisoNone99_n      = 0;
    OUT::ph_failSIEIEisoNone1111_n    = 0;
    OUT::ph_failSIEIEisoNone1616_n    = 0;
    OUT::ph_mediumNoNeuIsoNoPhoIso_n  = 0;
    OUT::ph_mediumNoChIsoNoPhoIso_n   = 0;
    OUT::ph_mediumNoChIsoNoNeuIso_n   = 0;
    OUT::ph_mediumNoSIEIENoPhoIso_n   = 0;
    OUT::ph_mediumNoSIEIENoNeuIso_n   = 0;
    OUT::ph_mediumNoSIEIENoChIso_n    = 0;
    OUT::ph_mediumNoSIEIENoEleVeto_n  = 0;
    OUT::ph_mediumNoSIEIEPassPSV_n    = 0;
    OUT::ph_mediumNoSIEIEFailPSV_n    = 0;
    OUT::ph_mediumNoSIEIEPassCSEV_n   = 0;
    OUT::ph_mediumNoSIEIEFailCSEV_n   = 0;
    OUT::ph_mediumNoEleVeto_n         = 0;
    OUT::ph_mediumPassPSV_n           = 0;
    OUT::ph_mediumFailPSV_n           = 0;
    OUT::ph_mediumPassCSEV_n          = 0;
    OUT::ph_mediumFailCSEV_n          = 0;
    OUT::ph_mediumNoChIsoNoEleVeto_n  = 0;
    OUT::ph_mediumNoChIsoPassPSV_n    = 0;
    OUT::ph_mediumNoChIsoFailPSV_n    = 0;
    OUT::ph_mediumNoChIsoPassCSEV_n   = 0;
    OUT::ph_mediumNoChIsoFailCSEV_n   = 0;
    OUT::ph_mediumNoNeuIsoNoEleVeto_n = 0;
    OUT::ph_mediumNoNeuIsoPassPSV_n   = 0;
    OUT::ph_mediumNoNeuIsoFailPSV_n   = 0;
    OUT::ph_mediumNoNeuIsoPassCSEV_n  = 0;
    OUT::ph_mediumNoNeuIsoFailCSEV_n  = 0;
    OUT::ph_mediumNoPhoIsoNoEleVeto_n = 0;
    OUT::ph_mediumNoPhoIsoPassPSV_n   = 0;
    OUT::ph_mediumNoPhoIsoFailPSV_n   = 0;
    OUT::ph_mediumNoPhoIsoPassCSEV_n  = 0;
    OUT::ph_mediumNoPhoIsoFailCSEV_n  = 0;

    OUT::leadPhot_sublPhotDR          = 0;
    OUT::leadPhot_sublPhotDPhi        = 0;
    OUT::phPhot_lepDPhi               = 0;
    OUT::dphi_met_lep1                = 0;
    OUT::dphi_met_lep2                = 0;
    OUT::dphi_met_ph1                 = 0;
    OUT::dphi_met_ph2                 = 0;
    OUT::mt_lep_met                   = 0;
    OUT::mt_lepph1_met                = 0;
    OUT::mt_lepph2_met                = 0;
    OUT::mt_lepphph_met               = 0;
    OUT::mt_trigel_met                = 0;
    OUT::mt_trigmu_met                = 0;
    OUT::m_leplep                     = 0;
    OUT::m_mumu                       = 0;
    OUT::m_elel                       = 0;
    OUT::m_leplep_uncorr              = 0;
    OUT::m_lepph1                     = 0;
    OUT::m_lepph2                     = 0;
    OUT::m_trigelph1                  = 0;
    OUT::m_trigelph2                  = 0;
    OUT::m_lep2ph1                    = 0;
    OUT::m_lep2ph2                    = 0;
    OUT::m_lepphlead                  = 0;
    OUT::m_lepphsubl                  = 0;
    OUT::m_lep2phlead                 = 0;
    OUT::m_lep2phsubl                 = 0;
    OUT::m_leplepph                   = 0;
    OUT::m_leplepphph                 = 0;
    OUT::m_leplepph1                  = 0;
    OUT::m_leplepph2                  = 0;
    OUT::m_lepphph                    = 0;
    OUT::m_trigelphph                 = 0;
    OUT::m_phph                       = 0;
    OUT::m_3lep                       = 0;
    OUT::m_4lep                       = 0;
    OUT::pt_phph                      = 0;
    OUT::pt_leplep                    = 0;
    OUT::pt_lepph1                    = 0;
    OUT::pt_lepph2                    = 0;
    OUT::pt_lepphph                   = 0;
    OUT::pt_leplepph                  = 0;
    OUT::pt_secondLepton              = 0;
    OUT::pt_thirdLepton               = 0;
    OUT::leadPhot_leadLepDR           = 0;
    OUT::leadPhot_sublLepDR           = 0;
    OUT::sublPhot_leadLepDR           = 0;
    OUT::sublPhot_sublLepDR           = 0;
    OUT::leadPhot_trigElDR            = 0;
    OUT::sublPhot_trigElDR            = 0;
    OUT::leadPhot_trigMuDR            = 0;
    OUT::sublPhot_trigMuDR            = 0;
    OUT::m_leadPhot_leadLep           = 0;
    OUT::m_leadPhot_trigEl            = 0;
    OUT::m_sublPhot_leadLep           = 0;
    OUT::m_sublPhot_trigEl            = 0;
    OUT::m_leadPhot_sublPhot_trigEl   = 0;
    OUT::dphi_met_leadPhot            = 0;
    OUT::dphi_met_sublPhot            = 0;
    OUT::dr_ph1_leadLep               = 0;
    OUT::dr_ph1_sublLep               = 0;
    OUT::dr_ph2_leadLep               = 0;
    OUT::dr_ph2_sublLep               = 0;
    OUT::dr_ph1_trigEle               = 0;
    OUT::dr_ph2_trigEle               = 0;
    OUT::dr_ph1_trigMu                = 0;
    OUT::dr_ph2_trigMu                = 0;
    OUT::dphi_ph1_leadLep             = 0;
    OUT::dphi_ph1_sublLep             = 0;
    OUT::dphi_ph2_leadLep             = 0;
    OUT::dphi_ph2_sublLep             = 0;
    OUT::m_ph1_ph2                    = 0;
    OUT::dr_ph1_ph2                   = 0;
    OUT::dphi_ph1_ph2                 = 0; 
    OUT::pt_ph1_ph2                   = 0; 
    OUT::m_leadLep_ph1_ph2            = 0; 
    OUT::m_leadLep_ph1                = 0; 
    OUT::m_leadLep_ph2                = 0; 
    OUT::m_sublLep_ph1                = 0; 
    OUT::m_sublLep_ph2                = 0; 
    OUT::pt_leadph12                  = 0;
    OUT::pt_sublph12                  = 0;
    OUT::eta_leadph12                 = 0;
    OUT::eta_sublph12                 = 0;
    OUT::hasPixSeed_leadph12          = 0;
    OUT::hasPixSeed_sublph12          = 0;
    OUT::sieie_leadph12               = 0;
    OUT::sieie_sublph12               = 0;
    OUT::chIsoCorr_leadph12           = 0;
    OUT::chIsoCorr_sublph12           = 0;
    OUT::neuIsoCorr_leadph12          = 0;
    OUT::neuIsoCorr_sublph12          = 0;
    OUT::phoIsoCorr_leadph12          = 0;
    OUT::phoIsoCorr_sublph12          = 0;

    OUT::ptSorted_ph_noSIEIEiso533_idx->clear();
    OUT::ptSorted_ph_noSIEIEiso855_idx->clear();
    OUT::ptSorted_ph_noSIEIEiso1077_idx->clear();
    OUT::ptSorted_ph_noSIEIEiso1299_idx->clear();
    OUT::ptSorted_ph_noSIEIEiso151111_idx->clear();
    OUT::ptSorted_ph_noSIEIEiso201616_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso53None_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso85None_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso107None_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso129None_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso1511None_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso2016None_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso5None3_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso8None5_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso10None7_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso12None9_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso15None11_idx->clear();
    OUT::ptSorted_ph_passSIEIEiso20None16_idx->clear();
    OUT::ptSorted_ph_passSIEIEisoNone33_idx->clear();
    OUT::ptSorted_ph_passSIEIEisoNone55_idx->clear();
    OUT::ptSorted_ph_passSIEIEisoNone77_idx->clear();
    OUT::ptSorted_ph_passSIEIEisoNone99_idx->clear();
    OUT::ptSorted_ph_passSIEIEisoNone1111_idx->clear();
    OUT::ptSorted_ph_passSIEIEisoNone1616_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso53None_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso85None_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso107None_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso129None_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso1511None_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso2016None_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso5None3_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso8None5_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso10None7_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso12None9_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso15None11_idx->clear();
    OUT::ptSorted_ph_failSIEIEiso20None16_idx->clear();
    OUT::ptSorted_ph_failSIEIEisoNone33_idx->clear();
    OUT::ptSorted_ph_failSIEIEisoNone55_idx->clear();
    OUT::ptSorted_ph_failSIEIEisoNone77_idx->clear();
    OUT::ptSorted_ph_failSIEIEisoNone99_idx->clear();
    OUT::ptSorted_ph_failSIEIEisoNone1111_idx->clear();
    OUT::ptSorted_ph_failSIEIEisoNone1616_idx->clear();
    OUT::ptSorted_ph_mediumNoNeuIsoNoPhoIso_idx->clear();
    OUT::ptSorted_ph_mediumNoChIsoNoPhoIso_idx->clear();
    OUT::ptSorted_ph_mediumNoChIsoNoNeuIso_idx->clear();
    OUT::ptSorted_ph_mediumNoSIEIENoPhoIso_idx->clear();
    OUT::ptSorted_ph_mediumNoSIEIENoNeuIso_idx->clear();
    OUT::ptSorted_ph_mediumNoSIEIENoChIso_idx->clear();
    OUT::ptSorted_ph_mediumNoSIEIENoEleVeto_idx->clear();
    OUT::ptSorted_ph_mediumNoSIEIEPassPSV_idx->clear();
    OUT::ptSorted_ph_mediumNoSIEIEFailPSV_idx->clear();
    OUT::ptSorted_ph_mediumNoSIEIEPassCSEV_idx->clear();
    OUT::ptSorted_ph_mediumNoSIEIEFailCSEV_idx->clear();
    OUT::ptSorted_ph_mediumNoEleVeto_idx->clear();
    OUT::ptSorted_ph_mediumPassPSV_idx->clear();
    OUT::ptSorted_ph_mediumFailPSV_idx->clear();
    OUT::ptSorted_ph_mediumPassCSEV_idx->clear();
    OUT::ptSorted_ph_mediumFailCSEV_idx->clear();
    OUT::ptSorted_ph_mediumNoChIsoNoEleVeto_idx->clear();
    OUT::ptSorted_ph_mediumNoChIsoPassPSV_idx->clear();
    OUT::ptSorted_ph_mediumNoChIsoFailPSV_idx->clear();
    OUT::ptSorted_ph_mediumNoChIsoPassCSEV_idx->clear();
    OUT::ptSorted_ph_mediumNoChIsoFailCSEV_idx->clear();
    OUT::ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx->clear();
    OUT::ptSorted_ph_mediumNoNeuIsoPassPSV_idx->clear();
    OUT::ptSorted_ph_mediumNoNeuIsoFailPSV_idx->clear();
    OUT::ptSorted_ph_mediumNoNeuIsoPassCSEV_idx->clear();
    OUT::ptSorted_ph_mediumNoNeuIsoFailCSEV_idx->clear();
    OUT::ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx->clear();
    OUT::ptSorted_ph_mediumNoPhoIsoPassPSV_idx->clear();
    OUT::ptSorted_ph_mediumNoPhoIsoFailPSV_idx->clear();
    OUT::ptSorted_ph_mediumNoPhoIsoPassCSEV_idx->clear();
    OUT::ptSorted_ph_mediumNoPhoIsoFailCSEV_idx->clear();

    OUT::ph_trigMatch_el->clear();
    OUT::ph_elMinDR     ->clear();
    OUT::EventWeight = 1.0;

    TLorentzVector metlv;
#ifdef EXISTS_pfType01MET
    metlv.SetPtEtaPhiM( OUT::pfType01MET, 0.0, OUT::pfType01METPhi, 0.0 );
#endif

    #ifdef EXISTS_el_n
    #ifdef EXISTS_mu_n
    #ifdef EXISTS_ph_n
    std::vector<TLorentzVector> leptons;
    std::vector<TLorentzVector> muons;
    std::vector<TLorentzVector> electrons;
    std::vector<TLorentzVector> trigelectrons;
    std::vector<TLorentzVector> trigmuons;
    std::vector<TLorentzVector> leptons_uncorr;
    // map pt to a bool, int pair.  The bool is 1 if electron, 0 if muon.  The int is the index
    std::vector<std::pair<float, std::pair<bool, int > > > sorted_leptons;
    for( int idx = 0; idx < OUT::el_n; idx++ ) {

        TLorentzVector lv;
        lv.SetPtEtaPhiE(  OUT::el_pt->at(idx),
                          OUT::el_eta->at(idx),
                          OUT::el_phi->at(idx),
                          OUT::el_e->at(idx)
                        );
        leptons.push_back(lv);
        electrons.push_back( lv );
        sorted_leptons.push_back( std::make_pair( lv.Pt(), std::make_pair( 1, idx ) ) );

#ifdef EXISTS_el_pt_uncorr
#ifdef EXISTS_el_e_uncorr
        TLorentzVector lv_uncorr;
        lv_uncorr.SetPtEtaPhiE(  OUT::el_pt_uncorr->at(idx),
                                 OUT::el_eta->at(idx),
                                 OUT::el_phi->at(idx),
                                 OUT::el_e_uncorr->at(idx)
                        );
        leptons_uncorr.push_back(lv_uncorr);
#endif 
#endif 

        if( lv.Pt() > 25 ) {
            OUT::el_pt25_n++;
        }
        if( lv.Pt() > 28 && OUT::el_triggerMatch->at(idx) && OUT::el_passMvaTrig->at(idx) ) {
            OUT::el_passtrig28_n++;
        }

        if( lv.Pt() > 30 && OUT::el_triggerMatch->at(idx) && OUT::el_passMvaTrig->at(idx) ) {
            OUT::el_passtrig_n++;
            trigelectrons.push_back( lv );
           
        }
        if( lv.Pt() > 30 && OUT::el_triggerMatch->at(idx) && OUT::el_passLoose->at(idx) ) {
            OUT::el_passtrigL_n++;
        }

    }

    for( int idx = 0; idx < OUT::mu_n; idx++ ) {

        TLorentzVector lv;
        lv.SetPtEtaPhiM(  OUT::mu_pt->at(idx),
                          OUT::mu_eta->at(idx),
                          OUT::mu_phi->at(idx),
                          0.1057
                        );
        leptons.push_back(lv);
        muons.push_back( lv );
        sorted_leptons.push_back( std::make_pair( lv.Pt(), std::make_pair( 0, idx ) ) );

        #ifdef EXISTS_mu_pt_uncorr
        #ifdef EXISTS_mu_eta_uncorr
        #ifdef EXISTS_mu_phi_uncorr
        #ifdef EXISTS_mu_e_uncorr
        TLorentzVector lv_uncorr;
        lv_uncorr.SetPtEtaPhiE(  OUT::mu_pt_uncorr->at(idx),
                                 OUT::mu_eta_uncorr->at(idx),
                                 OUT::mu_phi_uncorr->at(idx),
                                 OUT::mu_e_uncorr->at(idx)
                        );
        leptons_uncorr.push_back(lv_uncorr);
        #endif
        #endif
        #endif
        #endif

        if( lv.Pt() > 25 ) {
            OUT::mu_pt25_n++;
        }
        if( lv.Pt() > 30 && fabs(lv.Eta()) < 2.1 && OUT::mu_triggerMatch->at(idx) ) {
            OUT::mu_passtrig_n++;
        }
        if( lv.Pt() > 25 && fabs(lv.Eta()) < 2.1 && OUT::mu_triggerMatch->at(idx) ) {
            OUT::mu_passtrig25_n++;
            trigmuons.push_back(lv);
        }
    }

    std::vector<TLorentzVector> photons;
    std::vector<std::pair<float, int> > sorted_photons;

    std::vector<std::pair<float, int> > sorted_photons_iso533;
    std::vector<std::pair<float, int> > sorted_photons_iso855;
    std::vector<std::pair<float, int> > sorted_photons_iso1077;
    std::vector<std::pair<float, int> > sorted_photons_iso1299;
    std::vector<std::pair<float, int> > sorted_photons_iso151111;
    std::vector<std::pair<float, int> > sorted_photons_iso201616;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso53None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso85None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso107None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso129None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso1511None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso2016None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso5None3;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso8None5;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso10None7;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso12None9;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso15None11;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso20None16;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone33;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone55;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone77;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone99;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone1111;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone1616;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso53None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso85None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso107None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso129None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso1511None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso2016None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso5None3;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso8None5;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso10None7;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso12None9;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso15None11;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso20None16;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone33;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone55;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone77;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone99;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone1111;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone1616;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoNoPhoIso;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoNoPhoIso;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoNoNeuIso;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoPhoIso;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoNeuIso;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoChIso;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIEPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIEFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIEPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIEFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoFailCSEV;

    for( int idx = 0; idx < OUT::ph_n; ++idx ) {
        TLorentzVector phot;
        phot.SetPtEtaPhiE(  OUT::ph_pt->at(idx), 
                            OUT::ph_eta->at(idx),
                            OUT::ph_phi->at(idx),
                            OUT::ph_e->at(idx)
                        );
        photons.push_back(phot);

        std::pair<float, int> sort_pair = std::make_pair( phot.Pt(), idx );

        sorted_photons.push_back( sort_pair );

        if( OUT::ph_passHOverEMedium->at(idx)) {

            if( OUT::ph_chIsoCorr->at(idx) < 5   && 
                OUT::ph_neuIsoCorr->at(idx) < 3  && 
                OUT::ph_phoIsoCorr->at(idx) < 3 ) {
                OUT::ph_noSIEIEiso533_n++;
                sorted_photons_iso533.push_back( sort_pair );
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 8  && 
                OUT::ph_neuIsoCorr->at(idx) < 5 && 
                OUT::ph_phoIsoCorr->at(idx) < 5 ) {
                OUT::ph_noSIEIEiso855_n++;
                sorted_photons_iso855.push_back( sort_pair );
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 10 && 
                OUT::ph_neuIsoCorr->at(idx) < 7  && 
                OUT::ph_phoIsoCorr->at(idx) < 7 ) {
                OUT::ph_noSIEIEiso1077_n++;
                sorted_photons_iso1077.push_back( sort_pair );
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 12 && 
                OUT::ph_neuIsoCorr->at(idx) < 9  && 
                OUT::ph_phoIsoCorr->at(idx) < 9 ) {
                OUT::ph_noSIEIEiso1299_n++;
                sorted_photons_iso1299.push_back( sort_pair );
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 15 && 
                OUT::ph_neuIsoCorr->at(idx) < 11 && 
                OUT::ph_phoIsoCorr->at(idx) < 11 ) {
                OUT::ph_noSIEIEiso151111_n++;
                sorted_photons_iso151111.push_back( sort_pair );
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 20 && 
                OUT::ph_neuIsoCorr->at(idx) < 16 && 
                OUT::ph_phoIsoCorr->at(idx) < 16 ) {
                OUT::ph_noSIEIEiso201616_n++;
                sorted_photons_iso201616.push_back( sort_pair );
            }
            if( OUT::ph_passSIEIEMedium->at(idx) ) {

                // For phoIsoCorr, passing SIEIE, loosen other isolations
                if( OUT::ph_chIsoCorr->at(idx) < 5   && 
                    OUT::ph_neuIsoCorr->at(idx) < 3 ) {
                    OUT::ph_passSIEIEiso53None_n++;
                    sorted_photons_passSIEIEiso53None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 8  && 
                    OUT::ph_neuIsoCorr->at(idx) < 5 ) {
                    OUT::ph_passSIEIEiso85None_n++;
                    sorted_photons_passSIEIEiso85None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 10 && 
                    OUT::ph_neuIsoCorr->at(idx) < 7 ) {
                    OUT::ph_passSIEIEiso107None_n++;
                    sorted_photons_passSIEIEiso107None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 12 && 
                    OUT::ph_neuIsoCorr->at(idx) < 9 ) {
                    OUT::ph_passSIEIEiso129None_n++;
                    sorted_photons_passSIEIEiso129None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 15 && 
                    OUT::ph_neuIsoCorr->at(idx) < 11 ) {
                    OUT::ph_passSIEIEiso1511None_n++;
                    sorted_photons_passSIEIEiso1511None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 20 && 
                    OUT::ph_neuIsoCorr->at(idx) < 16 ) {
                    OUT::ph_passSIEIEiso2016None_n++;
                    sorted_photons_passSIEIEiso2016None.push_back( sort_pair );
                }

                // For neuIsoCorr, passing SIEIE, loosen other isolations
                if( OUT::ph_chIsoCorr->at(idx) < 5   && 
                    OUT::ph_phoIsoCorr->at(idx) < 3 ) {
                    OUT::ph_passSIEIEiso5None3_n++;
                    sorted_photons_passSIEIEiso5None3.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 8  && 
                    OUT::ph_phoIsoCorr->at(idx) < 5 ) {
                    OUT::ph_passSIEIEiso8None5_n++;
                    sorted_photons_passSIEIEiso8None5.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 10 && 
                    OUT::ph_phoIsoCorr->at(idx) < 7 ) {
                    OUT::ph_passSIEIEiso10None7_n++;
                    sorted_photons_passSIEIEiso10None7.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 12 && 
                    OUT::ph_phoIsoCorr->at(idx) < 9 ) {
                    OUT::ph_passSIEIEiso12None9_n++;
                    sorted_photons_passSIEIEiso12None9.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 15 && 
                    OUT::ph_phoIsoCorr->at(idx) < 11 ) {
                    OUT::ph_passSIEIEiso15None11_n++;
                    sorted_photons_passSIEIEiso15None11.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 20 && 
                    OUT::ph_phoIsoCorr->at(idx) < 16 ) {
                    OUT::ph_passSIEIEiso20None16_n++;
                    sorted_photons_passSIEIEiso20None16.push_back( sort_pair );
                }

                // For chIsoCorr, passing SIEIE, loosen other isolations
                if( OUT::ph_neuIsoCorr->at(idx) < 3  && 
                    OUT::ph_phoIsoCorr->at(idx) < 3 ) {
                    OUT::ph_passSIEIEisoNone33_n++;
                    sorted_photons_passSIEIEisoNone33.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 5 && 
                    OUT::ph_phoIsoCorr->at(idx) < 5 ) {
                    OUT::ph_passSIEIEisoNone55_n++;
                    sorted_photons_passSIEIEisoNone55.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 7  && 
                    OUT::ph_phoIsoCorr->at(idx) < 7 ) {
                    OUT::ph_passSIEIEisoNone77_n++;
                    sorted_photons_passSIEIEisoNone77.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 9  && 
                    OUT::ph_phoIsoCorr->at(idx) < 9 ) {
                    OUT::ph_passSIEIEisoNone99_n++;
                    sorted_photons_passSIEIEisoNone99.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 11 && 
                    OUT::ph_phoIsoCorr->at(idx) < 11 ) {
                    OUT::ph_passSIEIEisoNone1111_n++;
                    sorted_photons_passSIEIEisoNone1111.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 16 && 
                    OUT::ph_phoIsoCorr->at(idx) < 16 ) {
                    OUT::ph_passSIEIEisoNone1616_n++;
                    sorted_photons_passSIEIEisoNone1616.push_back( sort_pair );
                }
            }
            else {
                // For phoIsoCorr, failing SIEIE, loosen other isolations
                if( OUT::ph_chIsoCorr->at(idx) < 5   && 
                    OUT::ph_neuIsoCorr->at(idx) < 3 ) {
                    OUT::ph_failSIEIEiso53None_n++;
                    sorted_photons_failSIEIEiso53None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 8  && 
                    OUT::ph_neuIsoCorr->at(idx) < 5 ) {
                    OUT::ph_failSIEIEiso85None_n++;
                    sorted_photons_failSIEIEiso85None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 10 && 
                    OUT::ph_neuIsoCorr->at(idx) < 7 ) {
                    OUT::ph_failSIEIEiso107None_n++;
                    sorted_photons_failSIEIEiso107None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 12 && 
                    OUT::ph_neuIsoCorr->at(idx) < 9 ) {
                    OUT::ph_failSIEIEiso129None_n++;
                    sorted_photons_failSIEIEiso129None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 15 && 
                    OUT::ph_neuIsoCorr->at(idx) < 11 ) {
                    OUT::ph_failSIEIEiso1511None_n++;
                    sorted_photons_failSIEIEiso1511None.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 20 && 
                    OUT::ph_neuIsoCorr->at(idx) < 16 ) {
                    OUT::ph_failSIEIEiso2016None_n++;
                    sorted_photons_failSIEIEiso2016None.push_back( sort_pair );
                }

                // For neuIsoCorr, failing SIEIE, loosen other isolations
                if( OUT::ph_chIsoCorr->at(idx) < 5   && 
                    OUT::ph_phoIsoCorr->at(idx) < 3 ) {
                    OUT::ph_failSIEIEiso5None3_n++;
                    sorted_photons_failSIEIEiso5None3.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 8  && 
                    OUT::ph_phoIsoCorr->at(idx) < 5 ) {
                    OUT::ph_failSIEIEiso8None5_n++;
                    sorted_photons_failSIEIEiso8None5.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 10 && 
                    OUT::ph_phoIsoCorr->at(idx) < 7 ) {
                    OUT::ph_failSIEIEiso10None7_n++;
                    sorted_photons_failSIEIEiso10None7.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 12 && 
                    OUT::ph_phoIsoCorr->at(idx) < 9 ) {
                    OUT::ph_failSIEIEiso12None9_n++;
                    sorted_photons_failSIEIEiso12None9.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 15 && 
                    OUT::ph_phoIsoCorr->at(idx) < 11 ) {
                    OUT::ph_failSIEIEiso15None11_n++;
                    sorted_photons_failSIEIEiso15None11.push_back( sort_pair );
                }
                
                if( OUT::ph_chIsoCorr->at(idx) < 20 && 
                    OUT::ph_phoIsoCorr->at(idx) < 16 ) {
                    OUT::ph_failSIEIEiso20None16_n++;
                    sorted_photons_failSIEIEiso20None16.push_back( sort_pair );
                }

                // For chIsoCorr, failing SIEIE, loosen other isolations
                if( OUT::ph_neuIsoCorr->at(idx) < 3  && 
                    OUT::ph_phoIsoCorr->at(idx) < 3 ) {
                    OUT::ph_failSIEIEisoNone33_n++;
                    sorted_photons_failSIEIEisoNone33.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 5 && 
                    OUT::ph_phoIsoCorr->at(idx) < 5 ) {
                    OUT::ph_failSIEIEisoNone55_n++;
                    sorted_photons_failSIEIEisoNone55.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 7  && 
                    OUT::ph_phoIsoCorr->at(idx) < 7 ) {
                    OUT::ph_failSIEIEisoNone77_n++;
                    sorted_photons_failSIEIEisoNone77.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 9  && 
                    OUT::ph_phoIsoCorr->at(idx) < 9 ) {
                    OUT::ph_failSIEIEisoNone99_n++;
                    sorted_photons_failSIEIEisoNone99.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 11 && 
                    OUT::ph_phoIsoCorr->at(idx) < 11 ) {
                    OUT::ph_failSIEIEisoNone1111_n++;
                    sorted_photons_failSIEIEisoNone1111.push_back( sort_pair );
                }
                
                if( OUT::ph_neuIsoCorr->at(idx) < 16 && 
                    OUT::ph_phoIsoCorr->at(idx) < 16 ) {
                    OUT::ph_failSIEIEisoNone1616_n++;
                    sorted_photons_failSIEIEisoNone1616.push_back( sort_pair );
                }
            }
        }
        if( OUT::ph_passHOverEMedium->at(idx)) { 
            if( OUT::ph_passSIEIEMedium->at(idx) ) { 
                if( OUT::ph_passChIsoCorrMedium->at(idx) ) {
                    OUT::ph_mediumNoNeuIsoNoPhoIso_n++;
                    sorted_photons_mediumNoNeuIsoNoPhoIso.push_back( sort_pair );
                }
                if( OUT::ph_passNeuIsoCorrMedium->at(idx) ) {
                    OUT::ph_mediumNoChIsoNoPhoIso_n++;
                    sorted_photons_mediumNoChIsoNoPhoIso.push_back( sort_pair );
                }
                if( OUT::ph_passPhoIsoCorrMedium->at(idx) ) {
                    OUT::ph_mediumNoChIsoNoNeuIso_n++;
                    sorted_photons_mediumNoChIsoNoNeuIso.push_back( sort_pair );
                }
            }
            if( OUT::ph_passChIsoCorrMedium->at(idx) ) { 
                if( OUT::ph_passNeuIsoCorrMedium->at(idx) ) {
                    OUT::ph_mediumNoSIEIENoPhoIso_n++;
                    sorted_photons_mediumNoSIEIENoPhoIso.push_back( sort_pair );
                }
                if( OUT::ph_passPhoIsoCorrMedium->at(idx) ) {
                    OUT::ph_mediumNoSIEIENoNeuIso_n++;
                    sorted_photons_mediumNoSIEIENoNeuIso.push_back( sort_pair );
                }
            }
            if( OUT::ph_passNeuIsoCorrMedium->at(idx) ) { 
                if( OUT::ph_passPhoIsoCorrMedium->at(idx) ) {
                    OUT::ph_mediumNoSIEIENoChIso_n++;
                    sorted_photons_mediumNoSIEIENoChIso.push_back( sort_pair );
                }
            }
        }
        if( OUT::ph_passHOverEMedium->at(idx) && OUT::ph_passChIsoCorrMedium->at(idx)  && OUT::ph_passNeuIsoCorrMedium->at(idx) && OUT::ph_passPhoIsoCorrMedium->at(idx) ) {
            OUT::ph_mediumNoSIEIENoEleVeto_n++;
            sorted_photons_mediumNoSIEIENoEleVeto.push_back( sort_pair );

            if( OUT::ph_hasPixSeed->at(idx)==0 ) {
                OUT::ph_mediumNoSIEIEPassPSV_n++;
                sorted_photons_mediumNoSIEIEPassPSV.push_back( sort_pair );
            }
            if( OUT::ph_hasPixSeed->at(idx)==1 ) {
                OUT::ph_mediumNoSIEIEFailPSV_n++;
                sorted_photons_mediumNoSIEIEFailPSV.push_back( sort_pair );
            }
            if( OUT::ph_eleVeto->at(idx)==0 ) {
                OUT::ph_mediumNoSIEIEPassCSEV_n++;
                sorted_photons_mediumNoSIEIEPassCSEV.push_back( sort_pair );
            }
            if( OUT::ph_eleVeto->at(idx)==1 ) {
                OUT::ph_mediumNoSIEIEFailCSEV_n++;
                sorted_photons_mediumNoSIEIEFailCSEV.push_back( sort_pair );
            }
            if( OUT::ph_passSIEIEMedium->at(idx) ) {
                OUT::ph_mediumNoEleVeto_n++;
                sorted_photons_mediumNoEleVeto.push_back( sort_pair );
            
                if( OUT::ph_hasPixSeed->at(idx)==0 ) {
                    OUT::ph_mediumPassPSV_n++;
                    sorted_photons_mediumPassPSV.push_back( sort_pair );
                }
                if( OUT::ph_hasPixSeed->at(idx)==1 ) {
                    OUT::ph_mediumFailPSV_n++;
                    sorted_photons_mediumFailPSV.push_back( sort_pair );
                }
                if( OUT::ph_eleVeto->at(idx)==0 ) {
                    OUT::ph_mediumPassCSEV_n++;
                    sorted_photons_mediumPassCSEV.push_back( sort_pair );
                }
                if( OUT::ph_eleVeto->at(idx)==1 ) {
                    OUT::ph_mediumFailCSEV_n++;
                    sorted_photons_mediumFailCSEV.push_back( sort_pair );
                }
            }
        }
        if( OUT::ph_passHOverEMedium->at(idx) && OUT::ph_passSIEIEMedium->at(idx)  && OUT::ph_passNeuIsoCorrMedium->at(idx) && OUT::ph_passPhoIsoCorrMedium->at(idx) ) {
            OUT::ph_mediumNoChIsoNoEleVeto_n++;
            sorted_photons_mediumNoChIsoNoEleVeto.push_back( sort_pair );

            if( OUT::ph_hasPixSeed->at(idx)==0 ) {
                OUT::ph_mediumNoChIsoPassPSV_n++;
                sorted_photons_mediumNoChIsoPassPSV.push_back( sort_pair );
            }
            if( OUT::ph_hasPixSeed->at(idx)==1 ) {
                OUT::ph_mediumNoChIsoFailPSV_n++;
                sorted_photons_mediumNoChIsoFailPSV.push_back( sort_pair );
            }
            if( OUT::ph_eleVeto->at(idx)==0 ) {
                OUT::ph_mediumNoChIsoPassCSEV_n++;
                sorted_photons_mediumNoChIsoPassCSEV.push_back( sort_pair );
            }
            if( OUT::ph_eleVeto->at(idx)==1 ) {
                OUT::ph_mediumNoChIsoFailCSEV_n++;
                sorted_photons_mediumNoChIsoFailCSEV.push_back( sort_pair );
            }
        }
        if( OUT::ph_passHOverEMedium->at(idx) && OUT::ph_passSIEIEMedium->at(idx)  && OUT::ph_passChIsoCorrMedium->at(idx) && OUT::ph_passPhoIsoCorrMedium->at(idx) ) {
            OUT::ph_mediumNoNeuIsoNoEleVeto_n++;
            sorted_photons_mediumNoNeuIsoNoEleVeto.push_back( sort_pair );

            if( OUT::ph_hasPixSeed->at(idx)==0 ) {
                OUT::ph_mediumNoNeuIsoPassPSV_n++;
                sorted_photons_mediumNoNeuIsoPassPSV.push_back( sort_pair );
            }
            if( OUT::ph_hasPixSeed->at(idx)==1 ) {
                OUT::ph_mediumNoNeuIsoFailPSV_n++;
                sorted_photons_mediumNoNeuIsoFailPSV.push_back( sort_pair );
            }
            if( OUT::ph_eleVeto->at(idx)==0 ) {
                OUT::ph_mediumNoNeuIsoPassCSEV_n++;
                sorted_photons_mediumNoNeuIsoPassCSEV.push_back( sort_pair );
            }
            if( OUT::ph_eleVeto->at(idx)==1 ) {
                OUT::ph_mediumNoNeuIsoFailCSEV_n++;
                sorted_photons_mediumNoNeuIsoFailCSEV.push_back( sort_pair );
            }
        }
        if( OUT::ph_passHOverEMedium->at(idx) && OUT::ph_passSIEIEMedium->at(idx)  && OUT::ph_passChIsoCorrMedium->at(idx) && OUT::ph_passNeuIsoCorrMedium->at(idx) ) {
            OUT::ph_mediumNoPhoIsoNoEleVeto_n++;
            sorted_photons_mediumNoPhoIsoNoEleVeto.push_back( sort_pair );

            if( OUT::ph_hasPixSeed->at(idx)==0 ) {
                OUT::ph_mediumNoPhoIsoPassPSV_n++;
                sorted_photons_mediumNoPhoIsoPassPSV.push_back( sort_pair );
            }
            if( OUT::ph_hasPixSeed->at(idx)==1 ) {
                OUT::ph_mediumNoPhoIsoFailPSV_n++;
                sorted_photons_mediumNoPhoIsoFailPSV.push_back( sort_pair );
            }
            if( OUT::ph_eleVeto->at(idx)==0 ) {
                OUT::ph_mediumNoPhoIsoPassCSEV_n++;
                sorted_photons_mediumNoPhoIsoPassCSEV.push_back( sort_pair );
            }
            if( OUT::ph_eleVeto->at(idx)==1 ) {
                OUT::ph_mediumNoPhoIsoFailCSEV_n++;
                sorted_photons_mediumNoPhoIsoFailCSEV.push_back( sort_pair );
            }
        }
        
        bool match_eltrig = false;
        for( int elidx = 0; elidx < IN::el_n; elidx++ ) {

            // use IN electrons so that 
            TLorentzVector ellv;
            ellv.SetPtEtaPhiE(  IN::el_pt->at(elidx),
                              IN::el_eta->at(elidx),
                              IN::el_phi->at(elidx),
                              IN::el_e->at(elidx)
                            );
            if( ellv.DeltaR( phot ) < 0.2 && IN::el_triggerMatch->at(elidx) ) {
                match_eltrig=true;
            }
        }
        OUT::ph_trigMatch_el->push_back(match_eltrig);

        // electron overlap removal
        // use OUT because we want to remove
        // overlap with fully identified electrons
        float min_dr = 100.0;
        for( int eidx = 0; eidx < OUT::el_n; eidx++ ) {
            TLorentzVector ellv;
            ellv.SetPtEtaPhiE( OUT::el_pt->at(eidx), 
                               OUT::el_eta->at(eidx), 
                               OUT::el_phi->at(eidx), 
                               OUT::el_e->at(eidx) );

            float dr = phot.DeltaR( ellv );
            if( dr < min_dr ) {
                min_dr = dr;
            }
        }
        OUT::ph_elMinDR->push_back( min_dr );
    }

    std::map<std::string, float> results;
    std::map<std::string, std::vector<float> > vector_results;
    Wgg::CalcEventVars( photons, electrons, muons, trigelectrons, trigmuons, metlv, results, vector_results );

    CopyMapVarsToOut( results );
    CopyVectorMapVarsToOut( vector_results );

    // sort the list of photon momenta in descending order
    std::sort(sorted_photons.rbegin(), sorted_photons.rend());
    std::sort(sorted_leptons.rbegin(), sorted_leptons.rend());

    std::sort(sorted_photons_iso533.rbegin()                  , sorted_photons_iso533.rend());
    std::sort(sorted_photons_iso855.rbegin()                  , sorted_photons_iso855.rend());
    std::sort(sorted_photons_iso1077.rbegin()                 , sorted_photons_iso1077.rend());
    std::sort(sorted_photons_iso1299.rbegin()                 , sorted_photons_iso1299.rend());
    std::sort(sorted_photons_iso151111.rbegin()               , sorted_photons_iso151111.rend());
    std::sort(sorted_photons_iso201616.rbegin()               , sorted_photons_iso201616.rend());
    std::sort(sorted_photons_passSIEIEiso53None.rbegin()      , sorted_photons_passSIEIEiso53None.rend());
    std::sort(sorted_photons_passSIEIEiso85None.rbegin()      , sorted_photons_passSIEIEiso85None.rend());
    std::sort(sorted_photons_passSIEIEiso107None.rbegin()     , sorted_photons_passSIEIEiso107None.rend());
    std::sort(sorted_photons_passSIEIEiso129None.rbegin()     , sorted_photons_passSIEIEiso129None.rend());
    std::sort(sorted_photons_passSIEIEiso1511None.rbegin()    , sorted_photons_passSIEIEiso1511None.rend());
    std::sort(sorted_photons_passSIEIEiso2016None.rbegin()    , sorted_photons_passSIEIEiso2016None.rend());
    std::sort(sorted_photons_passSIEIEiso5None3.rbegin()       , sorted_photons_passSIEIEiso5None3.rend());
    std::sort(sorted_photons_passSIEIEiso8None5.rbegin()       , sorted_photons_passSIEIEiso8None5.rend());
    std::sort(sorted_photons_passSIEIEiso10None7.rbegin()      , sorted_photons_passSIEIEiso10None7.rend());
    std::sort(sorted_photons_passSIEIEiso12None9.rbegin()      , sorted_photons_passSIEIEiso12None9.rend());
    std::sort(sorted_photons_passSIEIEiso15None11.rbegin()    , sorted_photons_passSIEIEiso15None11.rend());
    std::sort(sorted_photons_passSIEIEiso20None16.rbegin()    , sorted_photons_passSIEIEiso20None16.rend());
    std::sort(sorted_photons_passSIEIEisoNone33.rbegin()      , sorted_photons_passSIEIEisoNone33.rend());
    std::sort(sorted_photons_passSIEIEisoNone55.rbegin()      , sorted_photons_passSIEIEisoNone55.rend());
    std::sort(sorted_photons_passSIEIEisoNone77.rbegin()      , sorted_photons_passSIEIEisoNone77.rend());
    std::sort(sorted_photons_passSIEIEisoNone99.rbegin()      , sorted_photons_passSIEIEisoNone99.rend());
    std::sort(sorted_photons_passSIEIEisoNone1111.rbegin()    , sorted_photons_passSIEIEisoNone1111.rend());
    std::sort(sorted_photons_passSIEIEisoNone1616.rbegin()    , sorted_photons_passSIEIEisoNone1616.rend());
    std::sort(sorted_photons_failSIEIEiso53None.rbegin()      , sorted_photons_failSIEIEiso53None.rend());
    std::sort(sorted_photons_failSIEIEiso85None.rbegin()      , sorted_photons_failSIEIEiso85None.rend());
    std::sort(sorted_photons_failSIEIEiso107None.rbegin()     , sorted_photons_failSIEIEiso107None.rend());
    std::sort(sorted_photons_failSIEIEiso129None.rbegin()     , sorted_photons_failSIEIEiso129None.rend());
    std::sort(sorted_photons_failSIEIEiso1511None.rbegin()    , sorted_photons_failSIEIEiso1511None.rend());
    std::sort(sorted_photons_failSIEIEiso2016None.rbegin()    , sorted_photons_failSIEIEiso2016None.rend());
    std::sort(sorted_photons_failSIEIEiso5None3.rbegin()       , sorted_photons_failSIEIEiso5None3.rend());
    std::sort(sorted_photons_failSIEIEiso8None5.rbegin()       , sorted_photons_failSIEIEiso8None5.rend());
    std::sort(sorted_photons_failSIEIEiso10None7.rbegin()      , sorted_photons_failSIEIEiso10None7.rend());
    std::sort(sorted_photons_failSIEIEiso12None9.rbegin()      , sorted_photons_failSIEIEiso12None9.rend());
    std::sort(sorted_photons_failSIEIEiso15None11.rbegin()    , sorted_photons_failSIEIEiso15None11.rend());
    std::sort(sorted_photons_failSIEIEiso20None16.rbegin()    , sorted_photons_failSIEIEiso20None16.rend());
    std::sort(sorted_photons_failSIEIEisoNone33.rbegin()      , sorted_photons_failSIEIEisoNone33.rend());
    std::sort(sorted_photons_failSIEIEisoNone55.rbegin()      , sorted_photons_failSIEIEisoNone55.rend());
    std::sort(sorted_photons_failSIEIEisoNone77.rbegin()      , sorted_photons_failSIEIEisoNone77.rend());
    std::sort(sorted_photons_failSIEIEisoNone99.rbegin()      , sorted_photons_failSIEIEisoNone99.rend());
    std::sort(sorted_photons_failSIEIEisoNone1111.rbegin()    , sorted_photons_failSIEIEisoNone1111.rend());
    std::sort(sorted_photons_failSIEIEisoNone1616.rbegin()    , sorted_photons_failSIEIEisoNone1616.rend());
    std::sort(sorted_photons_mediumNoNeuIsoNoPhoIso.rbegin()  , sorted_photons_mediumNoNeuIsoNoPhoIso.rend());
    std::sort(sorted_photons_mediumNoChIsoNoPhoIso.rbegin()   , sorted_photons_mediumNoChIsoNoPhoIso.rend());
    std::sort(sorted_photons_mediumNoChIsoNoNeuIso.rbegin()   , sorted_photons_mediumNoChIsoNoNeuIso.rend());
    std::sort(sorted_photons_mediumNoSIEIENoPhoIso.rbegin()   , sorted_photons_mediumNoSIEIENoPhoIso.rend());
    std::sort(sorted_photons_mediumNoSIEIENoNeuIso.rbegin()   , sorted_photons_mediumNoSIEIENoNeuIso.rend());
    std::sort(sorted_photons_mediumNoSIEIENoChIso.rbegin()    , sorted_photons_mediumNoSIEIENoChIso.rend());
    std::sort(sorted_photons_mediumNoSIEIENoEleVeto.rbegin()  , sorted_photons_mediumNoSIEIENoEleVeto.rend());
    std::sort(sorted_photons_mediumNoSIEIEPassPSV.rbegin()    , sorted_photons_mediumNoSIEIEPassPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIEFailPSV.rbegin()    , sorted_photons_mediumNoSIEIEFailPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIEPassCSEV.rbegin()   , sorted_photons_mediumNoSIEIEPassCSEV.rend());
    std::sort(sorted_photons_mediumNoSIEIEFailCSEV.rbegin()   , sorted_photons_mediumNoSIEIEFailCSEV.rend());
    std::sort(sorted_photons_mediumNoEleVeto.rbegin()         , sorted_photons_mediumNoEleVeto.rend());
    std::sort(sorted_photons_mediumPassPSV.rbegin()           , sorted_photons_mediumPassPSV.rend());
    std::sort(sorted_photons_mediumFailPSV.rbegin()           , sorted_photons_mediumFailPSV.rend());
    std::sort(sorted_photons_mediumPassCSEV.rbegin()          , sorted_photons_mediumPassCSEV.rend());
    std::sort(sorted_photons_mediumFailCSEV.rbegin()          , sorted_photons_mediumFailCSEV.rend());
    std::sort(sorted_photons_mediumNoChIsoNoEleVeto.rbegin()  , sorted_photons_mediumNoChIsoNoEleVeto.rend());
    std::sort(sorted_photons_mediumNoChIsoPassPSV.rbegin()    , sorted_photons_mediumNoChIsoPassPSV.rend());
    std::sort(sorted_photons_mediumNoChIsoFailPSV.rbegin()    , sorted_photons_mediumNoChIsoFailPSV.rend());
    std::sort(sorted_photons_mediumNoChIsoPassCSEV.rbegin()   , sorted_photons_mediumNoChIsoPassCSEV.rend());
    std::sort(sorted_photons_mediumNoChIsoFailCSEV.rbegin()   , sorted_photons_mediumNoChIsoFailCSEV.rend());
    std::sort(sorted_photons_mediumNoNeuIsoNoEleVeto.rbegin() , sorted_photons_mediumNoNeuIsoNoEleVeto.rend());
    std::sort(sorted_photons_mediumNoNeuIsoPassPSV.rbegin()   , sorted_photons_mediumNoNeuIsoPassPSV.rend());
    std::sort(sorted_photons_mediumNoNeuIsoFailPSV.rbegin()   , sorted_photons_mediumNoNeuIsoFailPSV.rend());
    std::sort(sorted_photons_mediumNoNeuIsoPassCSEV.rbegin()  , sorted_photons_mediumNoNeuIsoPassCSEV.rend());
    std::sort(sorted_photons_mediumNoNeuIsoFailCSEV.rbegin()  , sorted_photons_mediumNoNeuIsoFailCSEV.rend());
    std::sort(sorted_photons_mediumNoPhoIsoNoEleVeto.rbegin() , sorted_photons_mediumNoPhoIsoNoEleVeto.rend());
    std::sort(sorted_photons_mediumNoPhoIsoPassPSV.rbegin()   , sorted_photons_mediumNoPhoIsoPassPSV.rend());
    std::sort(sorted_photons_mediumNoPhoIsoFailPSV.rbegin()   , sorted_photons_mediumNoPhoIsoFailPSV.rend());
    std::sort(sorted_photons_mediumNoPhoIsoPassCSEV.rbegin()  , sorted_photons_mediumNoPhoIsoPassCSEV.rend());
    std::sort(sorted_photons_mediumNoPhoIsoFailCSEV.rbegin()  , sorted_photons_mediumNoPhoIsoFailCSEV.rend());


    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso533.begin() ; itr != sorted_photons_iso533.end(); ++itr ) {
        OUT::ptSorted_ph_noSIEIEiso533_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso855.begin() ; itr != sorted_photons_iso855.end(); ++itr ) {
        OUT::ptSorted_ph_noSIEIEiso855_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso1077.begin() ; itr != sorted_photons_iso1077.end(); ++itr ) {
        OUT::ptSorted_ph_noSIEIEiso1077_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso1299.begin() ; itr != sorted_photons_iso1299.end(); ++itr ) {
        OUT::ptSorted_ph_noSIEIEiso1299_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso151111.begin() ; itr != sorted_photons_iso151111.end(); ++itr ) {
        OUT::ptSorted_ph_noSIEIEiso151111_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso201616.begin() ; itr != sorted_photons_iso201616.end(); ++itr ) {
        OUT::ptSorted_ph_noSIEIEiso201616_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso53None.begin() ; itr != sorted_photons_passSIEIEiso53None.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso53None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso85None.begin() ; itr != sorted_photons_passSIEIEiso85None.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso85None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso107None.begin() ; itr != sorted_photons_passSIEIEiso107None.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso107None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso129None.begin() ; itr != sorted_photons_passSIEIEiso129None.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso129None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso1511None.begin() ; itr != sorted_photons_passSIEIEiso1511None.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso1511None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso2016None.begin() ; itr != sorted_photons_passSIEIEiso2016None.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso2016None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso5None3.begin() ; itr != sorted_photons_passSIEIEiso5None3.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso5None3_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso8None5.begin() ; itr != sorted_photons_passSIEIEiso8None5.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso8None5_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso10None7.begin() ; itr != sorted_photons_passSIEIEiso10None7.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso10None7_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso12None9.begin() ; itr != sorted_photons_passSIEIEiso12None9.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso12None9_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso15None11.begin() ; itr != sorted_photons_passSIEIEiso15None11.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso15None11_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso20None16.begin() ; itr != sorted_photons_passSIEIEiso20None16.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEiso20None16_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone33.begin() ; itr != sorted_photons_passSIEIEisoNone33.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEisoNone33_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone55.begin() ; itr != sorted_photons_passSIEIEisoNone55.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEisoNone55_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone77.begin() ; itr != sorted_photons_passSIEIEisoNone77.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEisoNone77_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone99.begin() ; itr != sorted_photons_passSIEIEisoNone99.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEisoNone99_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone1111.begin() ; itr != sorted_photons_passSIEIEisoNone1111.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEisoNone1111_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone1616.begin() ; itr != sorted_photons_passSIEIEisoNone1616.end(); ++itr ) {
        OUT::ptSorted_ph_passSIEIEisoNone1616_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso53None.begin() ; itr != sorted_photons_failSIEIEiso53None.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso53None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso85None.begin() ; itr != sorted_photons_failSIEIEiso85None.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso85None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso107None.begin() ; itr != sorted_photons_failSIEIEiso107None.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso107None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso129None.begin() ; itr != sorted_photons_failSIEIEiso129None.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso129None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso1511None.begin() ; itr != sorted_photons_failSIEIEiso1511None.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso1511None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso2016None.begin() ; itr != sorted_photons_failSIEIEiso2016None.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso2016None_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso5None3.begin() ; itr != sorted_photons_failSIEIEiso5None3.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso5None3_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso8None5.begin() ; itr != sorted_photons_failSIEIEiso8None5.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso8None5_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso10None7.begin() ; itr != sorted_photons_failSIEIEiso10None7.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso10None7_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso12None9.begin() ; itr != sorted_photons_failSIEIEiso12None9.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso12None9_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso15None11.begin() ; itr != sorted_photons_failSIEIEiso15None11.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso15None11_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso20None16.begin() ; itr != sorted_photons_failSIEIEiso20None16.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEiso20None16_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone33.begin() ; itr != sorted_photons_failSIEIEisoNone33.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEisoNone33_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone55.begin() ; itr != sorted_photons_failSIEIEisoNone55.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEisoNone55_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone77.begin() ; itr != sorted_photons_failSIEIEisoNone77.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEisoNone77_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone99.begin() ; itr != sorted_photons_failSIEIEisoNone99.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEisoNone99_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone1111.begin() ; itr != sorted_photons_failSIEIEisoNone1111.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEisoNone1111_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone1616.begin() ; itr != sorted_photons_failSIEIEisoNone1616.end(); ++itr ) {
        OUT::ptSorted_ph_failSIEIEisoNone1616_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoNoPhoIso.begin() ; itr != sorted_photons_mediumNoNeuIsoNoPhoIso.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoNeuIsoNoPhoIso_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoNoPhoIso.begin() ; itr != sorted_photons_mediumNoChIsoNoPhoIso.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoChIsoNoPhoIso_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoNoNeuIso.begin() ; itr != sorted_photons_mediumNoChIsoNoNeuIso.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoChIsoNoNeuIso_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoPhoIso.begin() ; itr != sorted_photons_mediumNoSIEIENoPhoIso.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoSIEIENoPhoIso_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoNeuIso.begin() ; itr != sorted_photons_mediumNoSIEIENoNeuIso.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoSIEIENoNeuIso_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoChIso.begin() ; itr != sorted_photons_mediumNoSIEIENoChIso.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoSIEIENoChIso_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoEleVeto.begin() ; itr != sorted_photons_mediumNoSIEIENoEleVeto.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoSIEIENoEleVeto_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIEPassPSV.begin() ; itr != sorted_photons_mediumNoSIEIEPassPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoSIEIEPassPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIEFailPSV.begin() ; itr != sorted_photons_mediumNoSIEIEFailPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoSIEIEFailPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIEPassCSEV.begin() ; itr != sorted_photons_mediumNoSIEIEPassCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoSIEIEPassCSEV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIEFailCSEV.begin() ; itr != sorted_photons_mediumNoSIEIEFailCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoSIEIEFailCSEV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoEleVeto.begin() ; itr != sorted_photons_mediumNoEleVeto.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoEleVeto_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumPassPSV.begin() ; itr != sorted_photons_mediumPassPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumPassPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumFailPSV.begin() ; itr != sorted_photons_mediumFailPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumFailPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumPassCSEV.begin() ; itr != sorted_photons_mediumPassCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumPassCSEV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumFailCSEV.begin() ; itr != sorted_photons_mediumFailCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumFailCSEV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoNoEleVeto.begin() ; itr != sorted_photons_mediumNoChIsoNoEleVeto.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoChIsoNoEleVeto_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoPassPSV.begin() ; itr != sorted_photons_mediumNoChIsoPassPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoChIsoPassPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoFailPSV.begin() ; itr != sorted_photons_mediumNoChIsoFailPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoChIsoFailPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoPassCSEV.begin() ; itr != sorted_photons_mediumNoChIsoPassCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoChIsoPassCSEV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoFailCSEV.begin() ; itr != sorted_photons_mediumNoChIsoFailCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoChIsoFailCSEV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoNoEleVeto.begin() ; itr != sorted_photons_mediumNoNeuIsoNoEleVeto.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoPassPSV.begin() ; itr != sorted_photons_mediumNoNeuIsoPassPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoNeuIsoPassPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoFailPSV.begin() ; itr != sorted_photons_mediumNoNeuIsoFailPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoNeuIsoFailPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoPassCSEV.begin() ; itr != sorted_photons_mediumNoNeuIsoPassCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoNeuIsoPassCSEV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoFailCSEV.begin() ; itr != sorted_photons_mediumNoNeuIsoFailCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoNeuIsoFailCSEV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoNoEleVeto.begin() ; itr != sorted_photons_mediumNoPhoIsoNoEleVeto.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoPassPSV.begin() ; itr != sorted_photons_mediumNoPhoIsoPassPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoPhoIsoPassPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoFailPSV.begin() ; itr != sorted_photons_mediumNoPhoIsoFailPSV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoPhoIsoFailPSV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoPassCSEV.begin() ; itr != sorted_photons_mediumNoPhoIsoPassCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoPhoIsoPassCSEV_idx->push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoFailCSEV.begin() ; itr != sorted_photons_mediumNoPhoIsoFailCSEV.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoPhoIsoFailCSEV_idx->push_back( itr->second );
    }

    if( sorted_photons.size() > 1 ) {
        int leadidx = sorted_photons[0].second;
        int sublidx = sorted_photons[1].second;
        OUT::hasPixSeed_leadph12 = OUT::ph_hasPixSeed->at(leadidx);
        OUT::hasPixSeed_sublph12 = OUT::ph_hasPixSeed->at(sublidx);
        OUT::sieie_leadph12 = OUT::ph_sigmaIEIE->at(leadidx);
        OUT::sieie_sublph12 = OUT::ph_sigmaIEIE->at(sublidx);
        OUT::chIsoCorr_leadph12 = OUT::ph_chIsoCorr->at(leadidx);
        OUT::chIsoCorr_sublph12 = OUT::ph_chIsoCorr->at(sublidx);
        OUT::neuIsoCorr_leadph12 = OUT::ph_neuIsoCorr->at(leadidx);
        OUT::neuIsoCorr_sublph12 = OUT::ph_neuIsoCorr->at(sublidx);
        OUT::phoIsoCorr_leadph12 = OUT::ph_phoIsoCorr->at(leadidx);
        OUT::phoIsoCorr_sublph12 = OUT::ph_phoIsoCorr->at(sublidx);
        OUT::isEB_leadph12 = OUT::ph_IsEB->at(leadidx);
        OUT::isEB_sublph12 = OUT::ph_IsEB->at(sublidx);
        OUT::isEE_leadph12 = OUT::ph_IsEE->at(leadidx);
        OUT::isEE_sublph12 = OUT::ph_IsEE->at(sublidx);
        OUT::truthMatchPh_leadph12 = OUT::ph_truthMatch_ph->at(leadidx);
        OUT::truthMatchPh_sublph12 = OUT::ph_truthMatch_ph->at(sublidx);
        OUT::truthMatchPhMomPID_leadph12 = OUT::ph_truthMatchMotherPID_ph->at(leadidx);
        OUT::truthMatchPhMomPID_sublph12 = OUT::ph_truthMatchMotherPID_ph->at(sublidx);
    }
    //// fill variables for pT sorted photons
    //if( sorted_photons.size() > 0 ) { 
    //    unsigned leadidx = sorted_photons[0].second;
    //    
    //    OUT::dphi_met_leadPhot = photons[leadidx].DeltaPhi( metlv );
    //    if( sorted_leptons.size() > 0 ) {
    //        unsigned leadlepidx = sorted_leptons[0].second.second;
    //        OUT::leadPhot_leadLepDR = photons[leadidx].DeltaR(leptons[leadlepidx]);
    //        OUT::m_leadPhot_leadLep = ( leptons[0] + photons[leadidx] ).M();
    //        if( sorted_leptons.size() > 1 ) {
    //            unsigned subllepidx = sorted_leptons[1].second.second;
    //            OUT::leadPhot_sublLepDR = photons[leadidx].DeltaR(leptons[subllepidx]);
    //        }
    //    }
    //    if( trigelectrons.size() > 0 ) {
    //        OUT::m_leadPhot_trigEl = ( trigelectrons[0] + photons[leadidx] ).M();
    //        OUT::leadPhot_trigElDR = photons[leadidx].DeltaR(trigelectrons[0]);
    //    }
    //    if( trigmuons.size() > 0 ) {
    //        OUT::leadPhot_trigMuDR = photons[leadidx].DeltaR(trigmuons[0]);
    //    }
    //    if( sorted_photons.size() > 1 ) {
    //        int leadidx = sorted_photons[0].second;
    //        int sublidx = sorted_photons[1].second;
    //        OUT::leadPhot_sublPhotDR    = photons[leadidx].DeltaR(photons[sublidx]);
    //        OUT::leadPhot_sublPhotDPhi    = photons[leadidx].DeltaPhi(photons[sublidx]);
    //        OUT::dphi_met_sublPhot = photons[sublidx].DeltaPhi( metlv );
    //        if( sorted_leptons.size() > 0 ) {
    //            unsigned leadlepidx = sorted_leptons[0].second.second;
    //            OUT::sublPhot_leadLepDR = photons[sublidx].DeltaR(leptons[leadlepidx]);
    //            OUT::m_sublPhot_leadLep = ( leptons[leadlepidx] + photons[sublidx] ).M();
    //            if( sorted_leptons.size() > 1 ) {
    //                unsigned subllepidx = sorted_leptons[1].second.second;
    //                OUT::sublPhot_sublLepDR = photons[sublidx].DeltaR(leptons[subllepidx]);
    //            }
    //        }
    //        if( trigelectrons.size() > 0 ) {
    //            OUT::m_sublPhot_trigEl = ( trigelectrons[0] + photons[sublidx] ).M();
    //            OUT::m_leadPhot_sublPhot_trigEl = ( trigelectrons[0] + photons[leadidx] + photons[sublidx] ).M();
    //            OUT::sublPhot_trigElDR = photons[sublidx].DeltaR(trigelectrons[0]);
    //        }
    //        if( trigmuons.size() > 0 ) {
    //            OUT::sublPhot_trigMuDR = photons[sublidx].DeltaR(trigmuons[0]);
    //        }

    //        OUT::pt_leadph12 = photons[leadidx].Pt();
    //        OUT::pt_sublph12 = photons[sublidx].Pt();
    //        OUT::eta_leadph12 = photons[leadidx].Eta();
    //        OUT::eta_sublph12 = photons[sublidx].Eta();
    //        OUT::hasPixSeed_leadph12 = OUT::ph_hasPixSeed->at(leadidx);
    //        OUT::hasPixSeed_sublph12 = OUT::ph_hasPixSeed->at(sublidx);
    //        OUT::sieie_leadph12 = OUT::ph_sigmaIEIE->at(leadidx);
    //        OUT::sieie_sublph12 = OUT::ph_sigmaIEIE->at(sublidx);
    //        OUT::chIsoCorr_leadph12 = OUT::ph_chIsoCorr->at(leadidx);
    //        OUT::chIsoCorr_sublph12 = OUT::ph_chIsoCorr->at(sublidx);
    //        OUT::neuIsoCorr_leadph12 = OUT::ph_neuIsoCorr->at(leadidx);
    //        OUT::neuIsoCorr_sublph12 = OUT::ph_neuIsoCorr->at(sublidx);
    //        OUT::phoIsoCorr_leadph12 = OUT::ph_phoIsoCorr->at(leadidx);
    //        OUT::phoIsoCorr_sublph12 = OUT::ph_phoIsoCorr->at(sublidx);
    //        OUT::isEB_leadph12 = OUT::ph_IsEB->at(leadidx);
    //        OUT::isEB_sublph12 = OUT::ph_IsEB->at(sublidx);
    //        OUT::isEE_leadph12 = OUT::ph_IsEE->at(leadidx);
    //        OUT::isEE_sublph12 = OUT::ph_IsEE->at(sublidx);
    //        OUT::truthMatchPh_leadph12 = OUT::ph_truthMatch_ph->at(leadidx);
    //        OUT::truthMatchPh_sublph12 = OUT::ph_truthMatch_ph->at(sublidx);
    //        OUT::truthMatchPhMomPID_leadph12 = OUT::ph_truthMatchMotherPID_ph->at(leadidx);
    //        OUT::truthMatchPhMomPID_sublph12 = OUT::ph_truthMatchMotherPID_ph->at(sublidx);

    //    }
    //}
    //// fill variables for default sorted photons
    //if( photons.size() > 0 ) { 
    //    OUT::dphi_met_ph1 = photons[0].DeltaPhi( metlv );
    //    if( sorted_leptons.size() > 0 ) {
    //        OUT::dr_ph1_leadLep = photons[0].DeltaR(leptons[sorted_leptons[0].second.second]);
    //        OUT::dphi_ph1_leadLep = photons[0].DeltaPhi(leptons[sorted_leptons[0].second.second]);
    //        OUT::m_leadLep_ph1 = ( photons[0] + leptons[sorted_leptons[0].second.second] ).M();
    //        if( sorted_leptons.size() > 1 ) {
    //            OUT::dr_ph1_sublLep = photons[0].DeltaR(leptons[sorted_leptons[1].second.second]);
    //            OUT::dphi_ph1_sublLep = photons[0].DeltaPhi(leptons[sorted_leptons[1].second.second]);
    //        }

    //        OUT::mt_lepph1_met = Utils::calc_mt( leptons[0] + photons[0], metlv );
    //        OUT::m_lepph1 = ( leptons[0] + photons[0] ).M();
    //    }


    //    if( trigelectrons.size() > 0 ) {
    //        OUT::dr_ph1_trigEle = photons[0].DeltaR( trigelectrons[0] );
    //        OUT::m_trigelph1 = ( photons[0] + trigelectrons[0] ).M();
    //    }
    //    if( trigmuons.size() > 0 ) {
    //        OUT::dr_ph1_trigMu = photons[0].DeltaR( trigmuons[0] );
    //    }
    //    if( sorted_leptons.size() > 1) {
    //        unsigned subllepidx = sorted_leptons[1].second.second;
    //        OUT::m_sublLep_ph1 = ( leptons[subllepidx] + photons[0] ).M();
    //    }
    //    if( photons.size() > 1 ) {

    //        OUT::dr_ph1_ph2 = photons[0].DeltaR(photons[1]);
    //        OUT::dphi_ph1_ph2 = photons[0].DeltaPhi(photons[1]);
    //        OUT::m_ph1_ph2 = (photons[0] + photons[1]).M();
    //        OUT::pt_ph1_ph2 = (photons[0] + photons[1]).Pt();
    //        OUT::dphi_met_ph2 = photons[1].DeltaPhi( metlv );

    //        if( sorted_leptons.size() > 0 ) {
    //            OUT::dr_ph2_leadLep = photons[1].DeltaR( leptons[sorted_leptons[0].second.second]);
    //            OUT::dphi_ph2_leadLep = photons[1].DeltaPhi( leptons[sorted_leptons[0].second.second]);
    //            OUT::m_leadLep_ph1_ph2 = ( photons[0] + photons[1] + leptons[sorted_leptons[0].second.second] ).M();
    //            OUT::m_leadLep_ph2 = ( photons[1] + leptons[sorted_leptons[0].second.second] ).M();

    //            OUT::mt_lepph2_met = Utils::calc_mt( leptons[0] + photons[1], metlv );
    //            OUT::mt_lepphph_met =Utils::calc_mt( leptons[0] + photons[0] + photons[1], metlv );
    //            OUT::pt_lepph1  = ( leptons[0] + photons[0] ).Pt();
    //            OUT::m_lepph2 = ( leptons[0] + photons[1] ).M();
    //            OUT::m_lepphph = ( leptons[0] + photons[0] + photons[1] ).M();

    //            if( sorted_leptons.size() > 1 ) {
    //                unsigned subllepidx = sorted_leptons[1].second.second;
    //                OUT::dr_ph2_sublLep = photons[1].DeltaR(leptons[subllepidx]);
    //                OUT::dphi_ph2_sublLep = photons[1].DeltaPhi(leptons[subllepidx]);
    //                OUT::m_sublLep_ph2 = ( leptons[subllepidx] + photons[1] ).M();
    //                OUT::pt_lepph2  = ( leptons[0] + photons[1] ).Pt();
    //                OUT::pt_lepphph = ( leptons[0] + photons[0] + photons[1] ).Pt();
    //            }
    //        }
    //        if( trigelectrons.size() > 0 ) {
    //            OUT::dr_ph2_trigEle = photons[1].DeltaR( trigelectrons[0] );
    //            OUT::m_trigelph2 = ( photons[1] + trigelectrons[0] ).M();
    //            OUT::m_trigelphph = ( photons[0] + photons[1] + trigelectrons[0] ).M();
    //        }
    //        if( trigmuons.size() > 0 ) {
    //            OUT::dr_ph2_trigMu = photons[1].DeltaR( trigmuons[0] );
    //        }
    //    }
    //}

    //if( leptons.size() > 0 ) {
    //    OUT::mt_lep_met = Utils::calc_mt( leptons[0], metlv );
    //    OUT::dphi_met_lep1 = leptons[0].DeltaPhi( metlv );

    //    if( leptons.size() > 1 ) {

    //        OUT::m_leplep = ( leptons[0] + leptons[1] ).M();
    //        OUT::pt_leplep = ( leptons[0] + leptons[1] ).Pt();
    //        if (leptons_uncorr.size() > 1) {
    //            OUT::m_leplep_uncorr = ( leptons_uncorr[0] + leptons_uncorr[1] ).M();
    //        }

    //        OUT::dphi_met_lep2 = leptons[1].DeltaPhi( metlv );

    //        if( photons.size() > 0 ) { 
    //            OUT::m_leplepph  = (leptons[0] + leptons[1] + photons[0] ).M();
    //            OUT::pt_leplepph  = (leptons[0] + leptons[1] + photons[0] ).Pt();
    //            if( photons.size() > 1 ) { 
    //                OUT::m_leplepphph  = (leptons[0] + leptons[1] + photons[0] + photons[1] ).M();
    //                OUT::m_leplepph1  = (leptons[0] + leptons[1] + photons[0] ).M();
    //                OUT::m_leplepph2  = (leptons[0] + leptons[1] + photons[1] ).M();
    //            }
    //        }
    //    }
    //}
    //if( trigelectrons.size() > 0 ) {
    //    OUT::mt_trigel_met = Utils::calc_mt( trigelectrons[0], metlv );
    //}
    //if( trigmuons.size() > 0 ) {
    //    OUT::mt_trigmu_met = Utils::calc_mt( trigmuons[0], metlv );
    //}
    //if( muons.size() > 1 ) {
    //    OUT::m_mumu = ( muons[0] + muons[1] ).M();
    //}
    //if( electrons.size() > 1 ) {
    //    OUT::m_elel = ( electrons[0] + electrons[1] ).M();
    //}
    //if( leptons.size() == 2 ) {
    //    OUT::pt_secondLepton = sorted_leptons[1].first;
    //}
    //if( leptons.size() == 3 ) {
    //    OUT::pt_thirdLepton = sorted_leptons[2].first;
    //    OUT::m_3lep = ( leptons[0] + leptons[1] + leptons[2] ).M();
    //}

    //if( leptons.size() == 4 ) {
    //    OUT::m_4lep = ( leptons[0] + leptons[1] + leptons[2] + leptons[3] ).M();
    //}

    #endif //el_n
    #endif //mu_n
    #endif //ph_n

}

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    #ifdef EXISTS_el_n
    #ifdef EXISTS_mu_n
    #ifdef EXISTS_ph_n
    int nPh = OUT::ph_n;
    
    int nLep = 0;
    int nLep25 = 0;
    int nLep20 = 0;
    int nLep10 = 0;
    int nLepTrigMatch = 0;
    int nLepTrigMatchSoft = 0;
    int nElTrigMatch = 0;
    int nElPh = 0;
    int nEl = 0;
    int nPhTruthMatchEl = 0;
    int nPhPassSIEIEAndEVeto =0;

    std::vector<TLorentzVector> leptons;
    std::vector<TLorentzVector> photons;

    for( int i = 0; i < OUT::mu_n; ++i ) {
        nLep++;
        TLorentzVector tlv;
        tlv.SetPtEtaPhiE( OUT::mu_pt->at(i), 
                          OUT::mu_eta->at(i), 
                          OUT::mu_phi->at(i), 
                          OUT::mu_e->at(i) );

        leptons.push_back(tlv);
        
        if( OUT::mu_pt->at(i) > 25 ) {
            nLep25++;
        }
        if( OUT::mu_pt->at(i) > 20 ) {
            nLep20++;
        }
        if( OUT::mu_pt->at(i) > 10 ) {
            nLep10++;
        }

        if( OUT::mu_triggerMatch->at(i) ) {
            nLepTrigMatchSoft++;
            if( OUT::mu_pt->at(i) > 25 ) {
                nLepTrigMatch++;
            }
        }
    }
    for( int i = 0; i < OUT::el_n; ++i ) {
        nLep++;
        nElPh++;
        nEl++;

        TLorentzVector tlv;
        tlv.SetPtEtaPhiE( OUT::el_pt->at(i), 
                          OUT::el_eta->at(i), 
                          OUT::el_phi->at(i), 
                          OUT::el_e->at(i) );

        leptons.push_back(tlv);

        if( OUT::el_pt->at(i) > 25 ) {
            nLep25++;
        }
        if( OUT::el_pt->at(i) > 20 ) {
            nLep20++;
        }
        if( OUT::el_pt->at(i) > 10 ) {
            nLep10++;
        }

        if( OUT::el_triggerMatch->at(i) && OUT::el_passMvaTrig->at(i) ) {
            nLepTrigMatchSoft++;
            if( OUT::el_pt->at(i) > 30 ) {
                nLepTrigMatch++;
                nElTrigMatch++;
            }
        }
    }

    for( int i = 0; i < OUT::ph_n; ++i ) {
        nElPh++;
        TLorentzVector tlv;
        tlv.SetPtEtaPhiM( OUT::ph_pt->at(i), 
                          OUT::ph_eta->at(i), 
                          OUT::ph_phi->at(i), 
                          0.0);

        photons.push_back(tlv);
        if( OUT::ph_truthMatch_el->at(i) ) {
            nPhTruthMatchEl++;
        }
        if( OUT::ph_passSIEIEMedium->at(i) && OUT::ph_eleVeto->at(i)== 0 ) {
            nPhPassSIEIEAndEVeto++;
        }
    }

    int n_overlap = 0;
    int n_combs = 0;
    for( unsigned int lidx = 0; lidx < leptons.size() ; lidx++ )  {
        for( unsigned int pidx = 0; pidx < photons.size() ; pidx++ )  {
            n_combs++;
            float dr = leptons[lidx].DeltaR( photons[pidx] );

            if( dr < 0.4 ) n_overlap++;
        }
    }

    int n_not_overlap = n_combs - n_overlap;

    if( !config.PassBool( "cut_SingleLepTrig", (OUT::passTrig_ele27WP80 || OUT::passTrig_mu24eta2p1 || OUT::passTrig_mu24 ) ) ) keep_event = false;
    if( !config.PassBool( "cut_DiLepTrig", (OUT::passTrig_mu17_mu8 || OUT::passTrig_mu17_Tkmu8 || OUT::passTrig_ele17_ele8_22 || OUT::passTrig_ele17_ele8_9) ) ) keep_event = false;
    if( !config.PassBool( "cut_DiMuTrig", (OUT::passTrig_mu17_mu8 || OUT::passTrig_mu17_Tkmu8 ) ) ) keep_event = false;
    if( !config.PassBool( "cut_DiElTrig", (OUT::passTrig_ele17_ele8_22 || OUT::passTrig_ele17_ele8_9 ) ) ) keep_event = false;

    if( !config.PassInt( "cut_nLep", nLep ) ) keep_event=false;
    if( !config.PassInt( "cut_nLep25", nLep25 ) ) keep_event=false;
    if( !config.PassInt( "cut_nLep20", nLep20 ) ) keep_event=false;
    if( !config.PassInt( "cut_nLep10", nLep10 ) ) keep_event=false;
    if( !config.PassInt( "cut_nLepTrigMatch", nLepTrigMatch ) ) keep_event=false;
    if( !config.PassInt( "cut_nLepTrigMatch", nLepTrigMatchSoft ) ) keep_event=false;
    if( !config.PassInt( "cut_nElTrigMatch", nElTrigMatch ) ) keep_event=false;
    if( !config.PassInt( "cut_nPh", nPh ) )   keep_event = false;
    if( !config.PassInt( "cut_nElPh", nElPh ) )   keep_event = false;
    if( !config.PassInt( "cut_nEl", nEl ) )   keep_event = false;
    if( !config.PassInt( "cut_nPhTruthMatchEl", nPhTruthMatchEl ) )   keep_event = false;
    if( !config.PassInt( "cut_nPhPassSIEIEAndEVeto", nPhPassSIEIEAndEVeto) )   keep_event = false;
    if( !config.PassInt( "cut_nPhPassMedium", OUT::ph_mediumPassPSV_n) )   keep_event = false;
    if( !config.PassInt( "cut_nPhPassMediumNoEleVeto", OUT::ph_mediumNoEleVeto_n) )   keep_event = false;
    if( !config.PassInt( "cut_nPhPassMediumFailEleVeto", OUT::ph_mediumFailPSV_n) )   keep_event = false;
    if( OUT::ph_n > 1 ) {
        if( OUT::ph_pt->at(0) > OUT::ph_pt->at(1) ) {
            if( !config.PassBool( "cut_hasPixSeed_leadph12", OUT::ph_hasPixSeed->at(0) ) ) keep_event = false;
            if( !config.PassBool( "cut_hasPixSeed_sublph12", OUT::ph_hasPixSeed->at(1) ) ) keep_event = false;
        }
        else {
            if( !config.PassBool( "cut_hasPixSeed_leadph12", OUT::ph_hasPixSeed->at(1) ) ) keep_event = false;
            if( !config.PassBool( "cut_hasPixSeed_sublph12", OUT::ph_hasPixSeed->at(0) ) ) keep_event = false;
        }
    }

    if( !config.PassInt( "cut_nNotOverlap", n_not_overlap ) )   keep_event = false;


    if( leptons.size() > 1 && config.HasCut( "cut_m_leplep" ) ) { 

        float mass = (leptons[0] + leptons[1] ).M();

        if( !config.PassFloat( "cut_m_leplep", mass ) ) keep_event = false;
    }

    if( !config.PassFloat( "cut_m_lepph1", OUT::m_lepph1 ) ) keep_event = false;
    if( !config.PassFloat( "cut_m_lepph2", OUT::m_lepph2 ) ) keep_event = false;
    if( !config.PassFloat( "cut_m_lep2ph1", OUT::m_lep2ph1 ) ) keep_event = false;
    if( !config.PassFloat( "cut_m_lep2ph2", OUT::m_lep2ph2 ) ) keep_event = false;


    #endif //el_n
    #endif //mu_n
    #endif //ph_n
    return keep_event;
}

bool RunModule::FilterBlind( ModuleConfig & config ) const {

    bool keep_event = true;

    bool pass_blind = true;
    if( !config.PassInt( "cut_nPhPassMedium", OUT::ph_mediumPassPSV_n ) ) pass_blind=false;
    if( !config.PassInt( "cut_ph_pt_lead", OUT::pt_leadph12) ) pass_blind=false;

    // electron channel mass
    if( OUT::el_passtrig_n > 0 ) {

        //if( !config.PassFloat( "cut_m_lepphph", OUT::m_lepphph) ) pass_blind=false;
        //if( !config.PassFloat( "cut_m_lepph1", OUT::m_lepph1  ) ) pass_blind=false;
        //if( !config.PassFloat( "cut_m_lepph2", OUT::m_lepph2  ) ) pass_blind=false;
        if( !config.PassFloat( "cut_m_lepphph", OUT::m_lepphph) && !config.PassFloat( "cut_m_lepph1", OUT::m_lepph1 ) && !config.PassFloat( "cut_m_lepph2", OUT::m_lepph2  ) )  pass_blind = false;

    }
    
    if( !pass_blind ) {
        OUT::isBlinded=true;
        if( _isData ) keep_event=false;
    }
    else {
        OUT::isBlinded=false;
    }

    return keep_event;

}

void RunModule::FilterJet( ModuleConfig & config ) const {

    #ifdef EXISTS_jet_n

    OUT::jet_n = 0;
    ClearOutputPrefix( "jet_" );

    for( int idx = 0; idx < IN::jet_n; idx++ ) {

        bool keep_jet = true;

        if( !config.PassInt( "cut_jet_n_constituents", IN::jet_Nconstitutents->at(idx) ) )keep_jet =false;
        if( !config.PassInt( "cut_jet_nch", IN::jet_NCH->at(idx) ) )   keep_jet = false;
        if( !config.PassFloat( "cut_jet_nhf", IN::jet_NHF->at(idx) ) ) keep_jet = false;
        if( !config.PassFloat( "cut_jet_nef", IN::jet_NEF->at(idx) ) ) keep_jet = false;
        if( !config.PassFloat( "cut_jet_chf", IN::jet_CHF->at(idx) ) ) keep_jet = false;
        if( !config.PassFloat( "cut_jet_cef", IN::jet_CEF->at(idx) ) ) keep_jet = false;

        // don't continue if the jet should be rejected
        if( !keep_jet ) continue;

        TLorentzVector jetlv;
        jetlv.SetPtEtaPhiE( IN::jet_pt->at(idx), 
                            IN::jet_eta->at(idx),
                            IN::jet_phi->at(idx),
                            IN::jet_e->at(idx)
                           );

        for( int eidx = 0; eidx < OUT::el_n; eidx++ ) {
            TLorentzVector ellv;
            ellv.SetPtEtaPhiE( OUT::el_pt->at(eidx), 
                               OUT::el_eta->at(eidx),
                               OUT::el_phi->at(eidx),
                               OUT::el_e->at(eidx)
                              );

            //delta R 
            float dr = ellv.DeltaR( jetlv );
            if( !config.PassFloat( "cut_jet_ele_dr", dr ) ) keep_jet = false;
        }

        // don't continue if the jet should be rejected
        if( !keep_jet ) continue;

        for( int pidx = 0; pidx < OUT::ph_n; pidx++ ) {

            TLorentzVector phlv;
            phlv.SetPtEtaPhiE( OUT::ph_pt->at(pidx), 
                               OUT::ph_eta->at(pidx),
                               OUT::ph_phi->at(pidx),
                               OUT::ph_e->at(pidx)
                              );

            //delta R 
            float dr = phlv.DeltaR( jetlv );
            if( !config.PassFloat( "cut_jet_ph_dr", dr ) ) keep_jet = false;
        }

        // don't continue if the jet should be rejected
        if( !keep_jet ) continue;

        for( int midx = 0; midx < OUT::mu_n; midx++ ) {
            TLorentzVector mulv;
            mulv.SetPtEtaPhiE( OUT::mu_pt->at(midx), 
                               OUT::mu_eta->at(midx),
                               OUT::mu_phi->at(midx),
                               OUT::mu_e->at(midx)
                              );

            //delta R 
            float dr = mulv.DeltaR( jetlv );
            if( !config.PassFloat( "cut_jet_mu_dr", dr ) ) keep_jet = false;
        }

        if( !keep_jet ) continue;

        OUT::jet_n++;
        CopyPrefixIndexBranchesInToOut( "jet_", idx, true );

    }
    #endif
}

RunModule::RunModule()  :
        _doMuPtScaleDown(0),
        _doMuPtScaleUp(0),
        _muPtScaleDownBarrel(-1),
        _muPtScaleDownEndcap(-1),
        _muPtScaleUpBarrel(-1),
        _muPtScaleUpEndcap(-1)
        {
        }



