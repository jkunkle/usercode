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
#include "include/MuScleFitCorrector.h"
#include "include/EnergyScaleCorrection_class.h"

#include "Core/Util.h"

#include "TFile.h"
#include "TH1D.h"

int main(int argc, char **argv)
{

    CmdOptions options = ParseOptions( argc, argv );

    // Parse the text file and form the configuration object
    AnaConfig ana_config = ParseConfig( options.config_file, options );
    std::cout << "Configured " << ana_config.size() << " analysis modules " << std::endl;

    RunModule runmod;
    ana_config.Run(runmod, options);

    std::cout << "^_^ Finished ^_^" << std::endl;


}

void RunModule::initialize( TChain * chain, TTree * outtree, TFile *outfile,
                            const CmdOptions & options, std::vector<ModuleConfig> & configs ) {

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Set defaults for added output variables
    // *************************
    OUT::el_pt                     = 0;
    OUT::el_eta                    = 0;
    OUT::el_sceta                  = 0;
    OUT::el_phi                    = 0;
    OUT::el_e                      = 0;
    OUT::el_pt_uncorr              = 0;
    OUT::el_e_uncorr               = 0;
    OUT::el_mva_trig               = 0;
    OUT::el_mva_nontrig            = 0;
    OUT::el_d0pv                   = 0;
    OUT::el_z0pv                   = 0;
    OUT::el_sigmaIEIE              = 0;
    OUT::el_pfiso30                = 0;
    OUT::el_pfiso40                = 0;
    OUT::el_charge                 = 0;
    OUT::el_triggerMatch           = 0;
    OUT::el_hasMatchedConv         = 0;
    OUT::el_passTight              = 0;
    OUT::el_passMedium             = 0;
    OUT::el_passLoose              = 0;
    OUT::el_passVeryLoose          = 0;
    OUT::el_passTightTrig          = 0;
    OUT::el_passMvaNonTrig         = 0;
    OUT::el_passMvaTrig            = 0;
    OUT::el_passMvaNonTrigNoIso    = 0;
    OUT::el_passMvaTrigNoIso       = 0;
    OUT::el_passMvaNonTrigOnlyIso  = 0;
    OUT::el_passMvaTrigOnlyIso     = 0;
    OUT::el_truthMatch_el          = 0;
    OUT::el_truthMinDR_el          = 0;
    OUT::el_truthMatchPt_el        = 0;
    OUT::mu_pt                     = 0;
    OUT::mu_eta                    = 0;
    OUT::mu_phi                    = 0;
    OUT::mu_e                      = 0;
    OUT::mu_pt_uncorr              = 0;
    OUT::mu_eta_uncorr             = 0;
    OUT::mu_phi_uncorr             = 0;
    OUT::mu_e_uncorr               = 0;
    OUT::mu_isGlobal               = 0;
    OUT::mu_isPF                   = 0;
    OUT::mu_chi2                   = 0;
    OUT::mu_nHits                  = 0;
    OUT::mu_nMuStations            = 0;
    OUT::mu_nPixHits               = 0;
    OUT::mu_nTrkLayers             = 0;
    OUT::mu_d0                     = 0;
    OUT::mu_z0                     = 0;
    OUT::mu_pfIso_ch               = 0;
    OUT::mu_pfIso_nh               = 0;
    OUT::mu_pfIso_pho              = 0;
    OUT::mu_pfIso_pu               = 0;
    OUT::mu_corrIso                = 0;
    OUT::mu_trkIso                 = 0;
    OUT::mu_charge                 = 0;
    OUT::mu_triggerMatch           = 0;
    OUT::mu_triggerMatchDiMu       = 0;
    OUT::mu_passTight              = 0;
    OUT::mu_passTightNoIso         = 0;
    OUT::mu_passTightNoD0          = 0;
    OUT::mu_passTightNoIsoNoD0     = 0;
    OUT::mu_truthMatch             = 0;
    OUT::mu_truthMinDR             = 0;
    OUT::ph_pt                     = 0;
    OUT::ph_eta                    = 0;
    OUT::ph_sceta                  = 0;
    OUT::ph_phi                    = 0;
    OUT::ph_e                      = 0;
    OUT::ph_scE                    = 0;
    OUT::ph_pt_uncorr              = 0;
    OUT::ph_HoverE                 = 0;
    OUT::ph_HoverE12               = 0;
    OUT::ph_sigmaIEIE              = 0;
    OUT::ph_sigmaIEIP              = 0;
    OUT::ph_r9                     = 0;
    OUT::ph_E1x3                   = 0;
    OUT::ph_E2x2                   = 0;
    OUT::ph_E5x5                   = 0;
    OUT::ph_E2x5Max                = 0;
    OUT::ph_SCetaWidth             = 0;
    OUT::ph_SCphiWidth             = 0;
    OUT::ph_ESEffSigmaRR           = 0;
    OUT::ph_hcalIsoDR03            = 0;
    OUT::ph_trkIsoHollowDR03       = 0;
    OUT::ph_chgpfIsoDR02           = 0;
    OUT::ph_pfChIsoWorst           = 0;
    OUT::ph_chIso                  = 0;
    OUT::ph_neuIso                 = 0;
    OUT::ph_phoIso                 = 0;
    OUT::ph_chIsoCorr              = 0;
    OUT::ph_neuIsoCorr             = 0;
    OUT::ph_phoIsoCorr             = 0;
    OUT::ph_eleVeto                = 0;
    OUT::ph_hasPixSeed             = 0;
    OUT::ph_drToTrk                = 0;
    OUT::ph_isConv                 = 0;
    OUT::ph_conv_nTrk              = 0;
    OUT::ph_conv_vtx_x             = 0;
    OUT::ph_conv_vtx_y             = 0;
    OUT::ph_conv_vtx_z             = 0;
    OUT::ph_conv_ptin1             = 0;
    OUT::ph_conv_ptin2             = 0;
    OUT::ph_conv_ptout1            = 0;
    OUT::ph_conv_ptout2            = 0;
    OUT::ph_passTight              = 0;
    OUT::ph_passMedium             = 0;
    OUT::ph_passLoose              = 0;
    OUT::ph_passLooseNoSIEIE       = 0;
    OUT::ph_passHOverELoose        = 0;
    OUT::ph_passHOverEMedium       = 0;
    OUT::ph_passHOverETight        = 0;
    OUT::ph_passSIEIELoose         = 0;
    OUT::ph_passSIEIEMedium        = 0;
    OUT::ph_passSIEIETight         = 0;
    OUT::ph_passChIsoCorrLoose     = 0;
    OUT::ph_passChIsoCorrMedium    = 0;
    OUT::ph_passChIsoCorrTight     = 0;
    OUT::ph_passNeuIsoCorrLoose    = 0;
    OUT::ph_passNeuIsoCorrMedium   = 0;
    OUT::ph_passNeuIsoCorrTight    = 0;
    OUT::ph_passPhoIsoCorrLoose    = 0;
    OUT::ph_passPhoIsoCorrMedium   = 0;
    OUT::ph_passPhoIsoCorrTight    = 0;
    OUT::ph_truthMatch_ph          = 0;
    OUT::ph_truthMinDR_ph          = 0;
    OUT::ph_truthMatchPt_ph        = 0;
    OUT::ph_truthMatchMotherPID_ph = 0;
    OUT::ph_truthMatch_el          = 0;
    OUT::ph_truthMinDR_el          = 0;
    OUT::ph_truthMatchPt_el        = 0;
    OUT::ph_hasSLConv              = 0;
    OUT::ph_pass_mva_presel        = 0;
    OUT::ph_mvascore               = 0;
    OUT::ph_IsEB                   = 0;
    OUT::ph_IsEE                   = 0;

    OUT::jet_pt                    = 0;
    OUT::jet_eta                   = 0;
    OUT::jet_phi                   = 0;
    OUT::jet_JECUnc                = 0;
    OUT::jet_e                     = 0;

    OUT::jet_NCH                   = 0;
    OUT::jet_Nconstitutents        = 0;
    OUT::jet_NEF                   = 0;
    OUT::jet_CEF                   = 0;
    OUT::jet_CHF                   = 0;
    OUT::jet_NHF                   = 0;

    OUT::jet_PUIDLoose             = 0;
    OUT::jet_PUIDMedium            = 0;
    OUT::jet_PUIDTight             = 0;

    OUT::jet_CSV                   = 0;


// jet gen variables do not exist for data
#ifdef EXISTS_jetGenJetIndex
    OUT::jet_genIndex              = 0;
    OUT::jet_genPt                 = 0;
    OUT::jet_genEta                = 0;
    OUT::jet_genPhi                = 0;
    OUT::jet_genE                  = 0;
#endif

    // *************************
    // Declare Branches
    // *************************
    outtree->Branch("el_n"                      , &OUT::el_n  , "el_n/I"          );
    outtree->Branch("mu_n"                      , &OUT::mu_n  , "mu_n/I"          );
    outtree->Branch("ph_n"                      , &OUT::ph_n , "ph_n/I"           );
    outtree->Branch("jet_n"                     , &OUT::jet_n , "jet_n/I"         );
    outtree->Branch("vtx_n"                     , &OUT::vtx_n   , "vtx_n/I"       );

    outtree->Branch("el_pt"                     , &OUT::el_pt                     );
    outtree->Branch("el_eta"                    , &OUT::el_eta                    );
    outtree->Branch("el_sceta"                  , &OUT::el_sceta                  );
    outtree->Branch("el_phi"                    , &OUT::el_phi                    );
    outtree->Branch("el_e"                      , &OUT::el_e                      );
    outtree->Branch("el_pt_uncorr"              , &OUT::el_pt_uncorr              );
    outtree->Branch("el_e_uncorr"               , &OUT::el_e_uncorr               );
    outtree->Branch("el_mva_trig"               , &OUT::el_mva_trig               );
    outtree->Branch("el_mva_nontrig"            , &OUT::el_mva_nontrig            );
    outtree->Branch("el_d0pv"                   , &OUT::el_d0pv                   );
    outtree->Branch("el_z0pv"                   , &OUT::el_z0pv                   );
    outtree->Branch("el_sigmaIEIE"              , &OUT::el_sigmaIEIE              );
    outtree->Branch("el_pfiso30"                , &OUT::el_pfiso30                );
    outtree->Branch("el_pfiso40"                , &OUT::el_pfiso40                );
    outtree->Branch("el_charge"                 , &OUT::el_charge                 );
    outtree->Branch("el_triggerMatch"           , &OUT::el_triggerMatch           );
    outtree->Branch("el_hasMatchedConv"         , &OUT::el_hasMatchedConv         );
    outtree->Branch("el_passTight"              , &OUT::el_passTight              );
    outtree->Branch("el_passMedium"             , &OUT::el_passMedium             );
    outtree->Branch("el_passLoose"              , &OUT::el_passLoose              );
    outtree->Branch("el_passVeryLoose"          , &OUT::el_passVeryLoose          );
    outtree->Branch("el_passTightTrig"          , &OUT::el_passTightTrig          );
    outtree->Branch("el_passMvaTrig"            , &OUT::el_passMvaTrig            );
    outtree->Branch("el_passMvaNonTrig"         , &OUT::el_passMvaNonTrig         );
    outtree->Branch("el_passMvaTrigNoIso"       , &OUT::el_passMvaTrigNoIso       );
    outtree->Branch("el_passMvaNonTrigNoIso"    , &OUT::el_passMvaNonTrigNoIso    );
    outtree->Branch("el_passMvaTrigOnlyIso"     , &OUT::el_passMvaTrigOnlyIso     );
    outtree->Branch("el_passMvaNonTrigOnlyIso"  , &OUT::el_passMvaNonTrigOnlyIso  );
    outtree->Branch("el_truthMatch_el"          , &OUT::el_truthMatch_el          );
    outtree->Branch("el_truthMinDR_el"          , &OUT::el_truthMinDR_el          );
    outtree->Branch("el_truthMatchPt_el"        , &OUT::el_truthMatchPt_el        );
    
    outtree->Branch("mu_pt"                     , &OUT::mu_pt                     );
    outtree->Branch("mu_eta"                    , &OUT::mu_eta                    );
    outtree->Branch("mu_phi"                    , &OUT::mu_phi                    );
    outtree->Branch("mu_e"                      , &OUT::mu_e                      );
    outtree->Branch("mu_pt_uncorr"              , &OUT::mu_pt_uncorr              );
    outtree->Branch("mu_eta_uncorr"             , &OUT::mu_eta_uncorr             );
    outtree->Branch("mu_phi_uncorr"             , &OUT::mu_phi_uncorr             );
    outtree->Branch("mu_e_uncorr"               , &OUT::mu_e_uncorr               );
    outtree->Branch("mu_isGlobal"               , &OUT::mu_isGlobal               );
    outtree->Branch("mu_isPF"                   , &OUT::mu_isPF                   );
    outtree->Branch("mu_chi2"                   , &OUT::mu_chi2                   );
    outtree->Branch("mu_nHits"                  , &OUT::mu_nHits                  );
    outtree->Branch("mu_nMuStations"            , &OUT::mu_nMuStations            );
    outtree->Branch("mu_nPixHits"               , &OUT::mu_nPixHits               );
    outtree->Branch("mu_nTrkLayers"             , &OUT::mu_nTrkLayers             );
    outtree->Branch("mu_d0"                     , &OUT::mu_d0                     );
    outtree->Branch("mu_z0"                     , &OUT::mu_z0                     );
    outtree->Branch("mu_pfIso_ch"               , &OUT::mu_pfIso_ch               );
    outtree->Branch("mu_pfIso_nh"               , &OUT::mu_pfIso_nh               );
    outtree->Branch("mu_pfIso_pho"              , &OUT::mu_pfIso_pho              );
    outtree->Branch("mu_pfIso_pu"               , &OUT::mu_pfIso_pu               );
    outtree->Branch("mu_corrIso"                , &OUT::mu_corrIso                );
    outtree->Branch("mu_trkIso"                 , &OUT::mu_trkIso                 );
    outtree->Branch("mu_charge"                 , &OUT::mu_charge                 );
    outtree->Branch("mu_triggerMatch"           , &OUT::mu_triggerMatch           );
    outtree->Branch("mu_triggerMatchDiMu"       , &OUT::mu_triggerMatchDiMu       );
    outtree->Branch("mu_passTight"              , &OUT::mu_passTight              );
    outtree->Branch("mu_passTightNoIso"         , &OUT::mu_passTightNoIso         );
    outtree->Branch("mu_passTightNoD0"          , &OUT::mu_passTightNoD0          );
    outtree->Branch("mu_passTightNoIsoNoD0"     , &OUT::mu_passTightNoIsoNoD0     );
    outtree->Branch("mu_truthMatch"             , &OUT::mu_truthMatch             );
    outtree->Branch("mu_truthMinDR"             , &OUT::mu_truthMinDR             );
    
    outtree->Branch("ph_pt"                     , &OUT::ph_pt                     );
    outtree->Branch("ph_eta"                    , &OUT::ph_eta                    );
    outtree->Branch("ph_sceta"                  , &OUT::ph_sceta                  );
    outtree->Branch("ph_phi"                    , &OUT::ph_phi                    );
    outtree->Branch("ph_e"                      , &OUT::ph_e                      );
    outtree->Branch("ph_scE"                    , &OUT::ph_scE                    );
    outtree->Branch("ph_pt_uncorr"              , &OUT::ph_pt_uncorr              );
    outtree->Branch("ph_HoverE"                 , &OUT::ph_HoverE                 );
    outtree->Branch("ph_HoverE12"               , &OUT::ph_HoverE12               );
    outtree->Branch("ph_sigmaIEIE"              , &OUT::ph_sigmaIEIE              );
    outtree->Branch("ph_sigmaIEIP"              , &OUT::ph_sigmaIEIP              );
    outtree->Branch("ph_r9"                     , &OUT::ph_r9                     );
    outtree->Branch("ph_E1x3"                   , &OUT::ph_E1x3                   );
    outtree->Branch("ph_E2x2"                   , &OUT::ph_E2x2                   );
    outtree->Branch("ph_E5x5"                   , &OUT::ph_E5x5                   );
    outtree->Branch("ph_E2x5Max"                , &OUT::ph_E2x5Max                );
    outtree->Branch("ph_SCetaWidth"             , &OUT::ph_SCetaWidth             );
    outtree->Branch("ph_SCphiWidth"             , &OUT::ph_SCphiWidth             );
    outtree->Branch("ph_ESEffSigmaRR"           , &OUT::ph_ESEffSigmaRR           );
    outtree->Branch("ph_hcalIsoDR03"            , &OUT::ph_hcalIsoDR03            );
    outtree->Branch("ph_trkIsoHollowDR03"       , &OUT::ph_trkIsoHollowDR03       );
    outtree->Branch("ph_chgpfIsoDR02"           , &OUT::ph_chgpfIsoDR02           );
    outtree->Branch("ph_pfChIsoWorst"           , &OUT::ph_pfChIsoWorst           );
    outtree->Branch("ph_chIso"                  , &OUT::ph_chIso                  );
    outtree->Branch("ph_neuIso"                 , &OUT::ph_neuIso                 );
    outtree->Branch("ph_phoIso"                 , &OUT::ph_phoIso                 );
    outtree->Branch("ph_chIsoCorr"              , &OUT::ph_chIsoCorr              );
    outtree->Branch("ph_neuIsoCorr"             , &OUT::ph_neuIsoCorr             );
    outtree->Branch("ph_phoIsoCorr"             , &OUT::ph_phoIsoCorr             );
    outtree->Branch("ph_SCRChIso"               , &OUT::ph_SCRChIso               );
    outtree->Branch("ph_SCRPhoIso"              , &OUT::ph_SCRPhoIso              );
    outtree->Branch("ph_SCRNeuIso"              , &OUT::ph_SCRNeuIso              );
    outtree->Branch("ph_SCRChIso04"             , &OUT::ph_SCRChIso04             );
    outtree->Branch("ph_SCRPhoIso04"            , &OUT::ph_SCRPhoIso04            );
    outtree->Branch("ph_SCRNeuIso04"            , &OUT::ph_SCRNeuIso04            );
    outtree->Branch("ph_RandConeChIso"          , &OUT::ph_RandConeChIso          );
    outtree->Branch("ph_RandConePhoIso"         , &OUT::ph_RandConePhoIso         );
    outtree->Branch("ph_RandConeNeuIso"         , &OUT::ph_RandConeNeuIso         );
    outtree->Branch("ph_RandConeChIso04"        , &OUT::ph_RandConeChIso04        );
    outtree->Branch("ph_RandConePhoIso04"       , &OUT::ph_RandConePhoIso04       );
    outtree->Branch("ph_RandConeNeuIso04"       , &OUT::ph_RandConeNeuIso04       );
    outtree->Branch("ph_eleVeto"                , &OUT::ph_eleVeto                );
    outtree->Branch("ph_hasPixSeed"             , &OUT::ph_hasPixSeed             );
    outtree->Branch("ph_drToTrk"                , &OUT::ph_drToTrk                );
    outtree->Branch("ph_isConv"                 , &OUT::ph_isConv                 );
    outtree->Branch("ph_conv_nTrk"              , &OUT::ph_conv_nTrk              );
    outtree->Branch("ph_conv_vtx_x"             , &OUT::ph_conv_vtx_x             );
    outtree->Branch("ph_conv_vtx_y"             , &OUT::ph_conv_vtx_y             );
    outtree->Branch("ph_conv_vtx_z"             , &OUT::ph_conv_vtx_z             );
    outtree->Branch("ph_conv_ptin1"             , &OUT::ph_conv_ptin1             );
    outtree->Branch("ph_conv_ptin2"             , &OUT::ph_conv_ptin2             );
    outtree->Branch("ph_conv_ptout1"            , &OUT::ph_conv_ptout1            );
    outtree->Branch("ph_conv_ptout2"            , &OUT::ph_conv_ptout2            );
    outtree->Branch("ph_passTight"              , &OUT::ph_passTight              );
    outtree->Branch("ph_passMedium"             , &OUT::ph_passMedium             );
    outtree->Branch("ph_passLoose"              , &OUT::ph_passLoose              );
    outtree->Branch("ph_passLooseNoSIEIE"       , &OUT::ph_passLooseNoSIEIE       );
    outtree->Branch("ph_passHOverELoose"        , &OUT::ph_passHOverELoose        );
    outtree->Branch("ph_passHOverEMedium"       , &OUT::ph_passHOverEMedium       );
    outtree->Branch("ph_passHOverETight"        , &OUT::ph_passHOverETight        );
    outtree->Branch("ph_passSIEIELoose"         , &OUT::ph_passSIEIELoose         );
    outtree->Branch("ph_passSIEIEMedium"        , &OUT::ph_passSIEIEMedium        );
    outtree->Branch("ph_passSIEIETight"         , &OUT::ph_passSIEIETight         );
    outtree->Branch("ph_passChIsoCorrLoose"     , &OUT::ph_passChIsoCorrLoose     );
    outtree->Branch("ph_passChIsoCorrMedium"    , &OUT::ph_passChIsoCorrMedium    );
    outtree->Branch("ph_passChIsoCorrTight"     , &OUT::ph_passChIsoCorrTight     );
    outtree->Branch("ph_passNeuIsoCorrLoose"    , &OUT::ph_passNeuIsoCorrLoose    );
    outtree->Branch("ph_passNeuIsoCorrMedium"   , &OUT::ph_passNeuIsoCorrMedium   );
    outtree->Branch("ph_passNeuIsoCorrTight"    , &OUT::ph_passNeuIsoCorrTight    );
    outtree->Branch("ph_passPhoIsoCorrLoose"    , &OUT::ph_passPhoIsoCorrLoose    );
    outtree->Branch("ph_passPhoIsoCorrMedium"   , &OUT::ph_passPhoIsoCorrMedium   );
    outtree->Branch("ph_passPhoIsoCorrTight"    , &OUT::ph_passPhoIsoCorrTight    );
    outtree->Branch("ph_truthMatch_el"          , &OUT::ph_truthMatch_el          );
    outtree->Branch("ph_truthMinDR_el"          , &OUT::ph_truthMinDR_el          );
    outtree->Branch("ph_truthMatchPt_el"        , &OUT::ph_truthMatchPt_el        );
    outtree->Branch("ph_truthMatch_ph"          , &OUT::ph_truthMatch_ph          );
    outtree->Branch("ph_truthMinDR_ph"          , &OUT::ph_truthMinDR_ph          );
    outtree->Branch("ph_truthMatchPt_ph"        , &OUT::ph_truthMatchPt_ph        );
    outtree->Branch("ph_truthMatchMotherPID_ph" , &OUT::ph_truthMatchMotherPID_ph );
    outtree->Branch("ph_hasSLConv"              , &OUT::ph_hasSLConv              );
    outtree->Branch("ph_pass_mva_presel"        , &OUT::ph_pass_mva_presel        );
    outtree->Branch("ph_mvascore"               , &OUT::ph_mvascore               );
    outtree->Branch("ph_IsEB"                   , &OUT::ph_IsEB                   );
    outtree->Branch("ph_IsEE"                   , &OUT::ph_IsEE                   );
    
    outtree->Branch("jet_pt"                    , &OUT::jet_pt                    );
    outtree->Branch("jet_eta"                   , &OUT::jet_eta                   );
    outtree->Branch("jet_phi"                   , &OUT::jet_phi                   );
    outtree->Branch("jet_JECUnc"                , &OUT::jet_JECUnc                );
    outtree->Branch("jet_e"                     , &OUT::jet_e                     );
    outtree->Branch("jet_NCH"                   , &OUT::jet_NCH);
    outtree->Branch("jet_Nconstitutents"        , &OUT::jet_Nconstitutents);
    outtree->Branch("jet_NEF"                   , &OUT::jet_NEF);
    outtree->Branch("jet_CEF"                   , &OUT::jet_CEF);
    outtree->Branch("jet_CHF"                   , &OUT::jet_CHF);
    outtree->Branch("jet_NHF"                   , &OUT::jet_NHF);
    outtree->Branch("jet_PUIDLoose"             , &OUT::jet_PUIDLoose);
    outtree->Branch("jet_PUIDMedium"            , &OUT::jet_PUIDMedium);
    outtree->Branch("jet_PUIDTight"             , &OUT::jet_PUIDTight);
    outtree->Branch("jet_CSV"                   , &OUT::jet_CSV);

// jet gen variables do not exist for data
#ifdef EXISTS_jetGenJetIndex
    outtree->Branch("jet_genIndex"              , &OUT::jet_genIndex              );
    outtree->Branch("jet_genPt"                 , &OUT::jet_genPt                 );
    outtree->Branch("jet_genEta"                , &OUT::jet_genEta                );
    outtree->Branch("jet_genPhi"                , &OUT::jet_genPhi                );
    outtree->Branch("jet_genE"                  , &OUT::jet_genE                  );
#endif

    //outtree->Branch("avgPU"              , &OUT::avgPU, "avgPU/F"                        );
    outtree->Branch("PUWeight"       , &OUT::PUWeight    , "PUWeight/F"       );
    outtree->Branch("PUWeightDN5"    , &OUT::PUWeightDN5 , "PUWeightDN5/F"    );
    outtree->Branch("PUWeightDN10"   , &OUT::PUWeightDN10, "PUWeightDN10/F"   );

    outtree->Branch("PUWeightUP5"    , &OUT::PUWeightUP5 , "PUWeightUP5/F"    );
    outtree->Branch("PUWeightUP6"    , &OUT::PUWeightUP6 , "PUWeightUP6/F"    );
    outtree->Branch("PUWeightUP7"    , &OUT::PUWeightUP7 , "PUWeightUP7/F"    );
    outtree->Branch("PUWeightUP8"    , &OUT::PUWeightUP8 , "PUWeightUP8/F"    );
    outtree->Branch("PUWeightUP9"    , &OUT::PUWeightUP9 , "PUWeightUP9/F"    );
    outtree->Branch("PUWeightUP10"    , &OUT::PUWeightUP10 , "PUWeightUP10/F"    );
    outtree->Branch("PUWeightUP11"    , &OUT::PUWeightUP11 , "PUWeightUP11/F"    );
    outtree->Branch("PUWeightUP12"    , &OUT::PUWeightUP12 , "PUWeightUP12/F"    );
    outtree->Branch("PUWeightUP13"    , &OUT::PUWeightUP13 , "PUWeightUP13/F"    );
    outtree->Branch("PUWeightUP14"    , &OUT::PUWeightUP14 , "PUWeightUP14/F"    );
    outtree->Branch("PUWeightUP15"    , &OUT::PUWeightUP15 , "PUWeightUP15/F"    );
    outtree->Branch("PUWeightUP16"    , &OUT::PUWeightUP16 , "PUWeightUP16/F"    );
    outtree->Branch("PUWeightUP17"    , &OUT::PUWeightUP17 , "PUWeightUP17/F"    );

    outtree->Branch("passTrig_ele27WP80"    , &OUT::passTrig_ele27WP80    , "passTrig_ele27WP80/O"     );
    outtree->Branch("passTrig_mu24eta2p1"   , &OUT::passTrig_mu24eta2p1   , "passTrig_mu24eta2p1/O"    );
    outtree->Branch("passTrig_mu24"         , &OUT::passTrig_mu24         , "passTrig_mu24/O"          );
    outtree->Branch("passTrig_mu17_mu8"     , &OUT::passTrig_mu17_mu8     , "passTrig_mu17_mu8/O"      );
    outtree->Branch("passTrig_mu17_Tkmu8"   , &OUT::passTrig_mu17_Tkmu8   , "passTrig_mu17_Tkmu8/O"    );
    outtree->Branch("passTrig_ele17_ele8_9" , &OUT::passTrig_ele17_ele8_9 , "passTrig_ele17_ele8_9/O"  );
    outtree->Branch("passTrig_ele17_ele8_22", &OUT::passTrig_ele17_ele8_22, "passTrig_ele17_ele8_22/O" );

    eval_el_tight       = false;
    eval_el_medium      = false;
    eval_el_loose       = false;
    eval_el_veryloose   = false;
    eval_el_tightTrig   = false;
    eval_el_tightTrig   = false;
    eval_el_mva_trig    = false;
    eval_el_mva_nontrig = false;

    eval_mu_tight       = false;

    eval_ph_tight     = false;
    eval_ph_medium    = false;
    eval_ph_loose     = false;

    apply_electron_corrections = false;
    apply_photon_corrections   = false;
    apply_muon_corrections     = false;
    apply_jet_corrections      = false;

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
    
    
        if( mod_conf.GetName() == "BuildElectron" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "evalPID" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string pid = eitr->second;
                if( pid == "tight"     ) eval_el_tight       = true;
                if( pid == "medium"    ) eval_el_medium      = true;
                if( pid == "loose"     ) eval_el_loose       = true;
                if( pid == "veryloose" ) eval_el_veryloose   = true;
                if( pid == "tightTrig" ) eval_el_tightTrig   = true;
                if( pid == "mvaTrig"   ) eval_el_mva_trig    = true;
                if( pid == "mvaNonTrig") eval_el_mva_nontrig = true;
            }

            std::map<std::string, std::string>::const_iterator citr = mod_conf.GetInitData().find( "applyCorrections" );
            if( citr != mod_conf.GetInitData().end() && citr->second == "true" ) {
                apply_electron_corrections=true;
            }
            citr = mod_conf.GetInitData().find( "correctionFile" );
            if( citr != mod_conf.GetInitData().end() ) {
                ele_correction_path = citr->second;

            }
            citr = mod_conf.GetInitData().find( "smearingFile" );
            if( citr != mod_conf.GetInitData().end() ) {
                ele_smearing_path = citr->second;
            }


        }
        if( mod_conf.GetName() == "BuildPhoton" ) { 
            std::map<std::string, std::string>::const_iterator itr = mod_conf.GetInitData().find( "evalPID" );
            if( itr != mod_conf.GetInitData().end() ) {
                std::string pid = itr->second;
                if( pid == "tight"     ) eval_ph_tight     = true;
                if( pid == "medium"    ) eval_ph_medium    = true;
                if( pid == "loose"     ) eval_ph_loose     = true;
            }
            std::map<std::string, std::string>::const_iterator citr = mod_conf.GetInitData().find( "applyCorrections" );
            if( citr != mod_conf.GetInitData().end() && citr->second == "true" ) {
                apply_photon_corrections=true;
            }
            citr = mod_conf.GetInitData().find( "TMVAWeightsFileEB" );
            if( citr != mod_conf.GetInitData().end() ) {
                std::string mva_weights_eb = citr->second;  
                TMVAReaderEB = new TMVA::Reader( "!Color:!Silent:Error" );
                TMVAReaderEB->SetVerbose(true);

                TMVAReaderEB->AddVariable("phoPhi", &MVAVars::phoPhi);
                TMVAReaderEB->AddVariable("phoR9", &MVAVars::phoR9);
                TMVAReaderEB->AddVariable("phoSigmaIEtaIEta", &MVAVars::phoSigmaIEtaIEta  );
                TMVAReaderEB->AddVariable("phoSigmaIEtaIPhi", &MVAVars::phoSigmaIEtaIPhi );
                TMVAReaderEB->AddVariable("s13", &MVAVars::s13 );
                TMVAReaderEB->AddVariable("s4ratio", &MVAVars::s4ratio );
                TMVAReaderEB->AddVariable("s25", &MVAVars::s25 );
                TMVAReaderEB->AddVariable("phoSCEta", &MVAVars::phoSCEta );
                TMVAReaderEB->AddVariable("phoSCRawE", &MVAVars::phoSCRawE );
                TMVAReaderEB->AddVariable("phoSCEtaWidth", &MVAVars::phoSCEtaWidth );
                TMVAReaderEB->AddVariable("phoSCPhiWidth", &MVAVars::phoSCPhiWidth );
                TMVAReaderEB->AddVariable("rho2012", &MVAVars::rho2012 );
                TMVAReaderEB->AddVariable("phoPFPhoIso", &MVAVars::phoPFPhoIso );
                TMVAReaderEB->AddVariable("phoPFChIso", &MVAVars::phoPFChIso );
                TMVAReaderEB->AddVariable("phoPFChIsoWorst", &MVAVars::phoPFChIsoWorst );

                TMVAReaderEB->AddSpectator("phoEt", &MVAVars::phoEt);
                TMVAReaderEB->AddSpectator("phoEta", &MVAVars::phoEta);

                TMVAReaderEB->BookMVA("BDT", mva_weights_eb);


            }
            citr = mod_conf.GetInitData().find( "TMVAWeightsFileEE" );
            if( citr != mod_conf.GetInitData().end() ) {
                std::string mva_weights_ee = citr->second;  
                TMVAReaderEE = new TMVA::Reader( "!Color:!Silent:Error" );
                TMVAReaderEE->SetVerbose(true);

                TMVAReaderEE->AddVariable("phoPhi", &MVAVars::phoPhi );
                TMVAReaderEE->AddVariable("phoR9", &MVAVars::phoR9 );
                TMVAReaderEE->AddVariable("phoSigmaIEtaIEta", &MVAVars::phoSigmaIEtaIEta );
                TMVAReaderEE->AddVariable("phoSigmaIEtaIPhi", &MVAVars::phoSigmaIEtaIPhi );
                TMVAReaderEE->AddVariable("s13", &MVAVars::s13 );
                TMVAReaderEE->AddVariable("s4ratio", &MVAVars::s4ratio );
                TMVAReaderEE->AddVariable("s25", &MVAVars::s25 );
                TMVAReaderEE->AddVariable("phoSCEta", &MVAVars::phoSCEta );
                TMVAReaderEE->AddVariable("phoSCRawE", &MVAVars::phoSCRawE );
                TMVAReaderEE->AddVariable("phoSCEtaWidth", &MVAVars::phoSCEtaWidth );
                TMVAReaderEE->AddVariable("phoSCPhiWidth", &MVAVars::phoSCPhiWidth );
                TMVAReaderEE->AddVariable("phoESEn/phoSCRawE", &MVAVars::phoESEnToRawE );
                TMVAReaderEE->AddVariable("phoESEffSigmaRR", &MVAVars::phoESEffSigmaRR );
                TMVAReaderEE->AddVariable("rho2012", &MVAVars::rho2012 );
                TMVAReaderEE->AddVariable("phoPFPhoIso", &MVAVars::phoPFPhoIso );
                TMVAReaderEE->AddVariable("phoPFChIso", &MVAVars::phoPFChIso );
                TMVAReaderEE->AddVariable("phoPFChIsoWorst", &MVAVars::phoPFChIsoWorst );

                TMVAReaderEE->AddSpectator("phoEt", &MVAVars::phoEt);
                TMVAReaderEE->AddSpectator("phoEta", &MVAVars::phoEta);
                TMVAReaderEE->BookMVA("BDT", mva_weights_ee);
            }
        }
        if( mod_conf.GetName() == "BuildMuon" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "evalPID" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string pid = eitr->second;
                if( pid == "tight"     ) eval_mu_tight       = true;
            }

            std::map<std::string, std::string>::const_iterator citr = mod_conf.GetInitData().find( "applyCorrections" );
            if( citr != mod_conf.GetInitData().end() && citr->second == "true" ) {
                apply_muon_corrections=true;
            }
            std::map<std::string, std::string>::const_iterator pitr = mod_conf.GetInitData().find( "path" );
            if( pitr != mod_conf.GetInitData().end() ) {
                muon_correction_path=pitr->second;
            }

        }
        if( mod_conf.GetName() == "BuildJet" ) { 
            std::map<std::string, std::string>::const_iterator citr = mod_conf.GetInitData().find( "applyCorrections" );
            if( citr != mod_conf.GetInitData().end() && citr->second == "true" ) {
                apply_jet_corrections=true;
            }
        }
        if( mod_conf.GetName() == "WeightEvent" ) { 
            std::string sample_filename;
            std::string data_filename;
            std::string sample_histname;
            std::string data_histname;
            std::map<std::string, std::string>::const_iterator sfitr = mod_conf.GetInitData().find( "sample_file" );
            std::map<std::string, std::string>::const_iterator dfitr = mod_conf.GetInitData().find( "data_file" );
            std::map<std::string, std::string>::const_iterator shitr = mod_conf.GetInitData().find( "sample_hist" );
            std::map<std::string, std::string>::const_iterator dhitr = mod_conf.GetInitData().find( "data_hist" );

            if( sfitr != mod_conf.GetInitData().end() ) {
                sample_filename = sfitr->second;
            }
            if( dfitr != mod_conf.GetInitData().end() ) {
                data_filename = dfitr->second;
            }
            if( shitr != mod_conf.GetInitData().end() ) {
                sample_histname = shitr->second;
            }
            if( dhitr != mod_conf.GetInitData().end() ) {
                data_histname = dhitr->second;
            }

            puweight_sample_file = TFile::Open( sample_filename.c_str(), "READ" );
            puweight_data_file = TFile::Open( data_filename.c_str(), "READ" );

            puweight_sample_hist = dynamic_cast<TH1F*>(puweight_sample_file->Get( sample_histname.c_str() ) ) ;
            puweight_data_hist = dynamic_cast<TH1D*>(puweight_data_file->Get( data_histname.c_str() ) );
            if( !puweight_sample_hist ) {
                std::cout << "Could not retrieve histogram " << sample_histname << " from " << sample_filename  << std::endl;
            }
            if( !puweight_data_hist ) {
                std::cout << "Could not retrieve histogram " << data_histname << " from " << data_filename << std::endl;
            }
            


        }

    }
    _rand.SetSeed( 80385 ); // W mass in MeV

    if( apply_muon_corrections ) {
        muCorr = new MuScleFitCorrector( muon_correction_path );
    }
    else {
        muCorr = 0;
    }

    if( apply_electron_corrections ) {
        eleCorr = new EnergyScaleCorrection_class( ele_correction_path, ele_smearing_path);
    }
    else {
        eleCorr = 0;
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

bool RunModule::ApplyModule( ModuleConfig & config ) {

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
    
    //mcParentage && 0x12 == 0x12
    if( config.GetName() == "BuildElectron" ) {
        BuildElectron( config );
    }
    if( config.GetName() == "BuildMuon" ) {
        BuildMuon( config );
    }
    if( config.GetName() == "BuildPhoton" ) {
        BuildPhoton( config );
    }
    if( config.GetName() == "BuildJet" ) {
        BuildJet( config );
    }
    if( config.GetName() == "WeightEvent" ) {
        WeightEvent( config );
    }
    if( config.GetName() == "BuildTriggerBits" ) {
        BuildTriggerBits( config );
    }


    // If the module applies a filter the filter decision
    // is passed back to here.  There is no requirement
    // that a function returns a bool, but
    // if you want the filter to work you need to do this
    //
    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }
    if( config.GetName() == "FilterTrigger" ) {
        keep_evt &= FilterTrigger( config );
    }

    return keep_evt;
}


// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************

void RunModule::BuildMuon( ModuleConfig & config ) const {

    OUT::mu_pt                 -> clear();
    OUT::mu_eta                -> clear();
    OUT::mu_phi                -> clear();
    OUT::mu_e                  -> clear();
    OUT::mu_pt_uncorr          -> clear();
    OUT::mu_eta_uncorr         -> clear();
    OUT::mu_phi_uncorr         -> clear();
    OUT::mu_e_uncorr           -> clear();
    OUT::mu_isGlobal           -> clear();
    OUT::mu_isPF               -> clear();
    OUT::mu_chi2               -> clear();
    OUT::mu_nHits              -> clear();
    OUT::mu_nMuStations        -> clear();
    OUT::mu_nPixHits           -> clear();
    OUT::mu_nTrkLayers         -> clear();
    OUT::mu_d0                 -> clear();
    OUT::mu_z0                 -> clear();
    OUT::mu_pfIso_ch           -> clear();
    OUT::mu_pfIso_nh           -> clear();
    OUT::mu_pfIso_pho          -> clear();
    OUT::mu_pfIso_pu           -> clear();
    OUT::mu_corrIso            -> clear();
    OUT::mu_trkIso             -> clear();
    OUT::mu_charge             -> clear();
    OUT::mu_triggerMatch       -> clear();
    OUT::mu_triggerMatchDiMu   -> clear();
    OUT::mu_passTight          -> clear();
    OUT::mu_passTightNoIso     -> clear();
    OUT::mu_passTightNoD0      -> clear();
    OUT::mu_passTightNoIsoNoD0 -> clear();
    OUT::mu_truthMatch         -> clear();
    OUT::mu_truthMinDR         -> clear();
    OUT::mu_n          = 0;

#ifdef EXISTS_nMu
    for( int idx = 0; idx < IN::nMu; ++idx ) {
       
        float pt = IN::muPt->at(idx);
        float eta = IN::muEta->at(idx);
        float phi = IN::muPhi->at(idx);
        unsigned int GlobalMuon = 1<<1;
        unsigned int PFMuon =  1<<5;
        bool is_global_muon = IN::muType->at(idx) & GlobalMuon;
        bool is_pf_muon = IN::muType->at(idx) & PFMuon;

        float chi2       = IN::muChi2NDF->at(idx);
        int   nHits      = IN::muNumberOfValidMuonHits->at(idx);
        int   nTrkLayers = IN::muNumberOfValidTrkLayers->at(idx);
        int   muStations = IN::muStations->at(idx);
        int   nPixHit    = IN::muNumberOfValidPixelHits->at(idx);
        float d0         = IN::muD0GV->at(idx);
        float z0         = IN::muDzGV->at(idx);
        float tkIso      = IN::muIsoTrk->at(idx);
        float muPFIsoCH  = IN::muPFIsoR04_CH->at(idx);
        float muPFIsoNH  = IN::muPFIsoR04_NH->at(idx);
        float muPFIsoPho = IN::muPFIsoR04_Pho->at(idx);
        float muPFIsoPU  = IN::muPFIsoR04_PU->at(idx);
        int charge       = IN::muCharge->at(idx);


        // trigger matching
        bool trigMatch = false;
        bool trigMatchDiMu = false;
        if( ( (IN::muTrg->at(idx) & 0x1) == 0x1 ) || ( (IN::muTrg->at(idx) & 0x2) == 0x2 ) ) trigMatch = true;
        if( ( (IN::muTrg->at(idx) & 0x4) == 0x4 ) || ( (IN::muTrg->at(idx) & 0x8) == 0x8 ) ) trigMatchDiMu = true;

        // muon momentum corrections
        #ifdef EXISTS_isData
        if( apply_muon_corrections && !IN::isData ) {
            TLorentzVector muvec;
            muvec.SetPtEtaPhiM( pt, eta, phi, 0.105 );
            muCorr->applyPtCorrection( muvec, charge );
            muCorr->applyPtSmearing( muvec, charge, false );
            pt = muvec.Pt();
            eta = muvec.Eta();
            phi = muvec.Phi();
        }
        #endif

        // isolation calculation
        float sum_neu = muPFIsoNH + muPFIsoPho - 0.5*muPFIsoPU;
        if( sum_neu < 0 ) {
            sum_neu = 0.0;
        }
        float corriso = muPFIsoCH+sum_neu;

        if( !config.PassFloat( "cut_pt"         , pt             ) ) continue;
        if( !config.PassFloat( "cut_abseta"     , fabs(eta)      ) ) continue;

        bool pass_tight = true;
        bool pass_tightNoIso = true;
        bool pass_tightNoD0 = true;
        bool pass_tightNoIsoNoD0 = true;

        if( !config.PassBool ( "cut_isGlobal"   , is_global_muon ) ) {
            pass_tight = false;
            pass_tightNoIso = false;
            pass_tightNoD0 = false;
            pass_tightNoIsoNoD0 = false;
        }
        if( !config.PassBool ( "cut_isPF"       , is_pf_muon     ) ) {
            pass_tight = false;
            pass_tightNoIso = false;
            pass_tightNoD0 = false;
            pass_tightNoIsoNoD0 = false;
        }
        if( !config.PassFloat( "cut_chi2"       , chi2           ) ) { 
            pass_tight = false;
            pass_tightNoIso = false;
            pass_tightNoD0 = false;
            pass_tightNoIsoNoD0 = false;
        }
        if( !config.PassFloat( "cut_nMuonHits"  , nHits          ) ) { 
            pass_tight = false;
            pass_tightNoIso = false;
            pass_tightNoD0 = false;
            pass_tightNoIsoNoD0 = false;
        }
        if( !config.PassFloat( "cut_nStations"  , muStations     ) ) { 
            pass_tight = false;
            pass_tightNoIso = false;
            pass_tightNoD0 = false;
            pass_tightNoIsoNoD0 = false;
        }
        if( !config.PassFloat( "cut_nPixelHits" , nPixHit        ) ) { 
            pass_tight = false;
            pass_tightNoIso = false;
            pass_tightNoD0 = false;
            pass_tightNoIsoNoD0 = false;
        }
        if( !config.PassFloat( "cut_nTrkLayers" , nTrkLayers     ) ) { 
            pass_tight = false;
            pass_tightNoIso = false;
            pass_tightNoD0 = false;
            pass_tightNoIsoNoD0 = false;
        }
        if( !config.PassFloat( "cut_d0"         , fabs(d0)       ) ) { 
            pass_tight = false;
            pass_tightNoIso = false;
        }
        if( !config.PassFloat( "cut_z0"         , fabs(z0)       ) ) { 
            pass_tight = false;
            pass_tightNoIso = false;
            pass_tightNoD0 = false;
            pass_tightNoIsoNoD0 = false;
        }
        if( !config.PassFloat( "cut_trkiso"     , tkIso/pt       ) ) { 
            pass_tight = false;
            pass_tightNoD0 = false;
        }
        if( !config.PassFloat( "cut_corriso"    , corriso/pt     ) ) { 
            pass_tight = false;
            pass_tightNoD0 = false;
        }

        // evaluate tight cuts if requested
        if( eval_mu_tight && !pass_tight ) continue;

        OUT::mu_n++;

        TLorentzVector muon;
        muon.SetPtEtaPhiM( pt, eta, phi, 0.106 );

        TLorentzVector muon_uncorr;
        muon_uncorr.SetPtEtaPhiM( IN::muPt->at(idx), IN::muEta->at(idx), IN::muPhi->at(idx), 0.106 );

        OUT::mu_pt                 -> push_back(muon.Pt() );
        OUT::mu_eta                -> push_back(muon.Eta());
        OUT::mu_phi                -> push_back(muon.Phi());
        OUT::mu_e                  -> push_back(muon.E()  );
        OUT::mu_pt_uncorr          -> push_back(muon_uncorr.Pt() );
        OUT::mu_eta_uncorr         -> push_back(muon_uncorr.Eta());
        OUT::mu_phi_uncorr         -> push_back(muon_uncorr.Phi());
        OUT::mu_e_uncorr           -> push_back(muon_uncorr.E()  );
        OUT::mu_isGlobal           -> push_back( is_global_muon );
        OUT::mu_isPF               -> push_back( is_pf_muon );
        OUT::mu_chi2               -> push_back( chi2 );
        OUT::mu_nHits              -> push_back( nHits );
        OUT::mu_nMuStations        -> push_back( muStations );
        OUT::mu_nPixHits           -> push_back( nPixHit );
        OUT::mu_nTrkLayers         -> push_back( nTrkLayers );
        OUT::mu_d0                 -> push_back( d0 );
        OUT::mu_z0                 -> push_back( z0 );
        OUT::mu_pfIso_ch           -> push_back(muPFIsoCH);
        OUT::mu_pfIso_nh           -> push_back(muPFIsoNH);
        OUT::mu_pfIso_pho          -> push_back(muPFIsoPho);
        OUT::mu_pfIso_pu           -> push_back(muPFIsoPU);
        OUT::mu_corrIso            -> push_back(corriso);
        OUT::mu_trkIso             -> push_back(tkIso);
        OUT::mu_charge             -> push_back(charge);
        OUT::mu_triggerMatch       -> push_back( trigMatch );
        OUT::mu_triggerMatchDiMu   -> push_back( trigMatchDiMu );
        OUT::mu_passTight          -> push_back( pass_tight );
        OUT::mu_passTightNoIso     -> push_back( pass_tightNoIso );
        OUT::mu_passTightNoD0      -> push_back( pass_tightNoD0 );
        OUT::mu_passTightNoIsoNoD0 -> push_back( pass_tightNoIsoNoD0 );


        std::vector<int> matchPID;
        matchPID.push_back(13);
        matchPID.push_back(-13);
        
        float truthMinDR = 100.0;
        bool has_match = HasTruthMatch( muon, matchPID, 0.1, truthMinDR );
        OUT::mu_truthMinDR->push_back( truthMinDR );
        OUT::mu_truthMatch->push_back( has_match );
    }
#endif

}

void RunModule::BuildElectron( ModuleConfig & config ) {

    OUT::el_pt                    -> clear();
    OUT::el_eta                   -> clear();
    OUT::el_sceta                 -> clear();
    OUT::el_phi                   -> clear();
    OUT::el_e                     -> clear();
    OUT::el_pt_uncorr             -> clear();
    OUT::el_e_uncorr              -> clear();
    OUT::el_mva_nontrig           -> clear();
    OUT::el_mva_trig              -> clear();
    OUT::el_d0pv                  -> clear();
    OUT::el_z0pv                  -> clear();
    OUT::el_sigmaIEIE             -> clear();
    OUT::el_pfiso30               -> clear();
    OUT::el_pfiso40               -> clear();
    OUT::el_charge                -> clear();
    OUT::el_triggerMatch          -> clear();
    OUT::el_hasMatchedConv        -> clear();
    OUT::el_passTight             -> clear();
    OUT::el_passMedium            -> clear();
    OUT::el_passLoose             -> clear();
    OUT::el_passVeryLoose         -> clear();
    OUT::el_passTightTrig         -> clear();
    OUT::el_passMvaNonTrig        -> clear();
    OUT::el_passMvaTrig           -> clear();
    OUT::el_passMvaNonTrigNoIso   -> clear();
    OUT::el_passMvaTrigNoIso      -> clear();
    OUT::el_passMvaNonTrigOnlyIso -> clear();
    OUT::el_passMvaTrigOnlyIso    -> clear();
    OUT::el_truthMatch_el         -> clear();
    OUT::el_truthMinDR_el         -> clear();
    OUT::el_truthMatchPt_el       -> clear();
    OUT::el_n              = 0;

#ifdef EXISTS_nEle
    for( int idx = 0; idx < IN::nEle; ++idx ) {

        float dEtaIn       = fabs(IN::eledEtaAtVtx->at(idx));
        float dPhiIn       = fabs(IN::eledPhiAtVtx->at(idx));
        float sigmaIEIE    = IN::eleSigmaIEtaIEta->at(idx);
        float d0           = fabs(IN::eleD0GV->at(idx));
        float z0           = fabs(IN::eleDzGV->at(idx));
        float hovere       = IN::eleHoverE->at(idx);
        int convfit      = IN::eleConvVtxFit->at(idx);
        int misshits       = IN::eleMissHits->at(idx);
        float ip3d         = IN::eleIP3D->at(idx);
        float ip3dErr      = IN::eleIP3DErr->at(idx);
        float sip = -100;
        if( ip3dErr != 0 ) {
            sip = ip3d/ip3dErr;
        }

        float pt           = IN::elePt->at(idx);
        float eta          = IN::eleEta->at(idx);
        float sceta        = IN::eleSCEta->at(idx);
        float phi          = IN::elePhi->at(idx);
        float en           = IN::eleEn->at(idx);
        float Ecalen       = IN::eleEcalEn->at(idx);
        float pin          = IN::elePin->at(idx);
        float momentum     = en/(IN::eleEoverP->at(idx));
        //float eoverp       = fabs( (1/en) - (1/momentum) );
        float eoverp      = fabs( (1/Ecalen) - (1/pin) );
        float mva_trig     = IN::eleIDMVATrig->at(idx);
        float mva_nontrig  = IN::eleIDMVANonTrig->at(idx);
        float ecalIso30    = IN::eleIsoEcalDR03->at(idx);
        float hcalIso30    = IN::eleIsoHcalDR03->at(idx);
        float trkIso30     = IN::eleIsoTrkDR03->at(idx);
        float phoIso30     = IN::elePFPhoIso03->at(idx);
        float neuIso30     = IN::elePFNeuIso03->at(idx);
        float chIso30      = IN::elePFChIso03->at(idx);
        float phoIso40     = IN::elePFPhoIso04->at(idx);
        float neuIso40     = IN::elePFNeuIso04->at(idx);
        float chIso40      = IN::elePFChIso04->at(idx);
        float r9           = IN::eleR9->at(idx);
        int   charge       = IN::eleCharge->at(idx);

        float rho = IN::rho2012;

        // trigger matching
        bool trigMatch = false;
        if( (IN::eleTrg->at(idx) & 0x1) == 0x1 ) trigMatch = true;

        // effective areas isolation
        float ea03 = get_ele_eff_area( sceta, 3 );
        float ea04 = get_ele_eff_area( sceta, 4 );

        float neuIsoCorr30 = phoIso30 + neuIso30 - ea03*rho;
        float neuIsoCorr40 = phoIso40 + neuIso40 - ea04*rho;

        if( neuIsoCorr30 < 0 ) {
            neuIsoCorr30 = 0.0;
        }
        if( neuIsoCorr40 < 0 ) {
            neuIsoCorr40 = 0.0;
        }

        float pfIsoCorr30 = chIso30 + neuIsoCorr30;
        float pfIsoCorr40 = chIso40 + neuIsoCorr40;

        // electron mometum correction
        #ifdef EXISTS_isData
        #ifdef EXISTS_run
        if( apply_electron_corrections ) {

            bool iseb = false;
            if( fabs(sceta) < 1.479 ) {
                iseb = true;
            }
            float scale = 1.0;
            if( IN::isData ) {
                // last 2 args aren't used
                scale = eleCorr->ScaleCorrection(IN::run, iseb, r9, sceta, pt, 0, 0 );
            }
            else {
                scale = eleCorr->getSmearing(IN::run, en, iseb, r9, sceta );
            }

            pt*=scale;
            en*=scale;
        }
        #endif
        #endif

        if( !config.PassFloat( "cut_pt"  , pt  ) ) continue;

        if( !config.PassFloat( "cut_abseta"         , fabs(eta) ) ) continue;
        if( !config.PassFloat( "cut_abseta_crack"   , fabs(eta) ) ) continue;
        if( !config.PassFloat( "cut_abssceta"       , fabs(sceta) ) ) continue;
        if( !config.PassFloat( "cut_abssceta_crack" , fabs(sceta) ) ) continue;

        bool pass_tight             = true;
        bool pass_medium            = true;
        bool pass_loose             = true;
        bool pass_veryloose         = true;
        bool pass_tightTrig         = true;
        bool pass_mva_trig          = true;
        bool pass_mva_nontrig       = true;
        bool pass_mva_trig_noiso    = true;
        bool pass_mva_nontrig_noiso = true;
        bool pass_mva_trig_onlyiso    = true;
        bool pass_mva_nontrig_onlyiso = true;

        bool use_eval = eval_el_tight || eval_el_medium || eval_el_loose || eval_el_veryloose || eval_el_tightTrig || eval_el_mva_nontrig || eval_el_mva_trig;


        if( fabs(sceta) < 1.479 ) { // barrel

            
            // Tight cuts
            if( !use_eval || eval_el_tight ) {
                if( !config.PassFloat( "cut_absdEtaIn_barrel_tight"    , dEtaIn       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_barrel_tight"    , dPhiIn       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_tight" , sigmaIEIE    ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_d0_barrel_tight"        , d0           ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_z0_barrel_tight"        , z0           ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_tight"    , hovere       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_eoverp_barrel_tight"    , eoverp       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_pfIsoCorr30_barrel_tight"   , pfIsoCorr30/pt   ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassInt( "cut_convfit_barrel_tight"   , convfit      ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_barrel_tight"  , misshits     ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
            }
            
            // Medium cuts
            if( !use_eval || eval_el_medium ) {
                if( !config.PassFloat( "cut_absdEtaIn_barrel_medium"    , dEtaIn       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_barrel_medium"    , dPhiIn       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_medium" , sigmaIEIE    ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_d0_barrel_medium"        , d0           ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_z0_barrel_medium"        , z0           ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_medium"    , hovere       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_eoverp_barrel_medium"    , eoverp       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_pfIsoCorr30_barrel_medium"   , pfIsoCorr30/pt   ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassInt( "cut_convfit_barrel_medium"   , convfit      ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_barrel_medium"  , misshits     ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
            }
            
            // Loose cuts
            if( !use_eval || eval_el_loose ) {
                if( !config.PassFloat( "cut_absdEtaIn_barrel_loose"    , dEtaIn       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_barrel_loose"    , dPhiIn       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_loose" , sigmaIEIE    ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_d0_barrel_loose"        , d0           ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_z0_barrel_loose"        , z0           ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_loose"    , hovere       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_eoverp_barrel_loose"    , eoverp       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_pfIsoCorr30_barrel_loose"   , pfIsoCorr30/pt   ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassInt( "cut_convfit_barrel_loose"   , convfit      ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_barrel_loose"  , misshits     ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
            }

            // Very Loose cuts
            if( !use_eval || eval_el_veryloose ) {
                if( !config.PassFloat( "cut_absdEtaIn_barrel_veryloose"    , dEtaIn       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_barrel_veryloose"    , dPhiIn       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_veryloose" , sigmaIEIE    ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_d0_barrel_veryloose"        , d0           ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_z0_barrel_veryloose"        , z0           ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_veryloose"    , hovere       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_eoverp_barrel_veryloose"    , eoverp       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_pfIsoCorr30_barrel_veryloose"   , pfIsoCorr30/pt   ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassInt( "cut_convfit_barrel_veryloose"   , convfit      ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_barrel_veryloose"  , misshits     ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
            }

            // tight trigger cuts
            if( !use_eval || eval_el_tightTrig ) {
                if( !config.PassFloat( "cut_absdEtaIn_barrel_tightTrig"   , dEtaIn      ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_barrel_tightTrig"   , dPhiIn      ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_tightTrig"   , sigmaIEIE   ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_tightTrig"   , hovere         ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_ecalIso30_barrel_tightTrig"   , ecalIso30/pt) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_hcalIso30_barrel_tightTrig"   , hcalIso30/pt) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_trkIso30_barrel_tightTrig"   , trkIso30/pt  ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
            }


        }
        else { // endcap

            // Tight cuts
            if( !use_eval || eval_el_tight ) {
                if( !config.PassFloat( "cut_absdEtaIn_endcap_tight"    , dEtaIn       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_endcap_tight"    , dPhiIn       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_tight" , sigmaIEIE    ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_d0_endcap_tight"        , d0           ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_z0_endcap_tight"        , z0           ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_tight"    , hovere       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_eoverp_endcap_tight"    , eoverp       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( pt < 20 ) {
                  if( !config.PassFloat( "cut_pfIsoCorr30_endcap_lowPt_tight"   , pfIsoCorr30/pt   ) ) {
                      pass_tight=false;
                    if( eval_el_tight ) continue;
                  }
                }
                else {
                  if( !config.PassFloat( "cut_pfIsoCorr30_endcap_highPt_tight"   , pfIsoCorr30/pt   ) ) {
                      pass_tight=false;
                    if( eval_el_tight ) continue;
                  }
                }

                if( !config.PassInt( "cut_convfit_endcap_tight"   , convfit      ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_endcap_tight"  , misshits     ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
            }
            
            // Medium cuts
            if( !use_eval || eval_el_medium ) {
                if( !config.PassFloat( "cut_absdEtaIn_endcap_medium"    , dEtaIn       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_endcap_medium"    , dPhiIn       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_medium" , sigmaIEIE    ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_d0_endcap_medium"        , d0           ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_z0_endcap_medium"        , z0           ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_medium"    , hovere       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_eoverp_endcap_medium"    , eoverp       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( pt < 20 ) {
                    if( !config.PassFloat( "cut_pfIsoCorr30_endcap_lowPt_medium"   , pfIsoCorr30/pt   ) ) {
                        pass_medium=false;
                    if( eval_el_medium ) continue;
                    }
                }
                else {
                    if( !config.PassFloat( "cut_pfIsoCorr30_endcap_highPt_medium"   , pfIsoCorr30/pt   ) ) {
                        pass_medium=false;
                    if( eval_el_medium ) continue;
                    }
                }
                if( !config.PassInt( "cut_convfit_endcap_medium"   , convfit      ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_endcap_medium"  , misshits     ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
            }
            
            // Loose cuts
            if( !use_eval || eval_el_loose ) {
                if( !config.PassFloat( "cut_absdEtaIn_endcap_loose"    , dEtaIn       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_endcap_loose"    , dPhiIn       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_loose" , sigmaIEIE    ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_d0_endcap_loose"        , d0           ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_z0_endcap_loose"        , z0           ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_loose"    , hovere       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_eoverp_endcap_loose"    , eoverp       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( pt < 20 ) {
                    if( !config.PassFloat( "cut_pfIsoCorr30_endcap_lowPt_loose"   , pfIsoCorr30/pt   ) ) {
                        pass_loose=false;
                    if( eval_el_loose ) continue;
                    }
                }
                else {
                    if( !config.PassFloat( "cut_pfIsoCorr30_endcap_highPt_loose"   , pfIsoCorr30/pt   ) ) {
                        pass_loose=false;
                    if( eval_el_loose ) continue;
                    }
                }
                if( !config.PassInt( "cut_convfit_endcap_loose"   , convfit      ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_endcap_loose"  , misshits     ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
            }

            // Very Loose cuts
            if( !use_eval || eval_el_veryloose ) {
                if( !config.PassFloat( "cut_absdEtaIn_endcap_veryloose"    , dEtaIn       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_endcap_veryloose"    , dPhiIn       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_veryloose" , sigmaIEIE    ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_d0_endcap_veryloose"        , d0           ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_z0_endcap_veryloose"        , z0           ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_veryloose"    , hovere       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_eoverp_endcap_veryloose"    , eoverp       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_pfIsoCorr30_endcap_veryloose"   , pfIsoCorr30/pt   ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassInt( "cut_convfit_endcap_veryloose"   , convfit      ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_endcap_veryloose"  , misshits     ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
            }

            // tight trigger cuts
            if( !use_eval || eval_el_tightTrig ) {
                if( !config.PassFloat( "cut_absdEtaIn_endcap_tightTrig"   , dEtaIn      ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_endcap_tightTrig"   , dPhiIn      ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_tightTrig"   , sigmaIEIE   ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_tightTrig"   , hovere         ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_ecalIso30_endcap_tightTrig"   , ecalIso30/pt) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_hcalIso30_endcap_tightTrig"   , hcalIso30/pt) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
                if( !config.PassFloat( "cut_trkIso30_endcap_tightTrig"   , trkIso30/pt  ) ) {
                    pass_tightTrig=false;
                    if( eval_el_tightTrig ) continue;
                }
            }
        }

        // non-triggering MVA
        if( !use_eval || eval_el_mva_nontrig) {

            if( pt < 10 ) {
                if( fabs(sceta) < 0.8 ) {
                    if( !config.PassFloat( "cut_mva_central_lowpt_mvanontrig"   , mva_nontrig  ) ) {
                        pass_mva_nontrig =false;
                        pass_mva_nontrig_noiso =false;
                        if( eval_el_mva_nontrig ) continue;
                    }
                }
                else if( fabs(sceta) < 1.479 ) {
                    if( !config.PassFloat( "cut_mva_crack_lowpt_mvanontrig"   , mva_nontrig  ) ) {
                        pass_mva_nontrig =false;
                        pass_mva_nontrig_noiso =false;
                        if( eval_el_mva_nontrig ) continue;
                    }
                }
                else if( fabs(sceta) < 2.5 ) {
                    if( !config.PassFloat( "cut_mva_endcap_lowpt_mvanontrig"   , mva_nontrig  ) ) {
                        pass_mva_nontrig =false;
                        pass_mva_nontrig_noiso =false;
                        if( eval_el_mva_nontrig ) continue;
                    }
                }
            } else {
                if( fabs(sceta) < 0.8 ) {
                    if( !config.PassFloat( "cut_mva_central_highpt_mvanontrig"   , mva_nontrig  ) ) {
                        pass_mva_nontrig =false;
                        pass_mva_nontrig_noiso =false;
                        if( eval_el_mva_nontrig ) continue;
                    }
                }
                else if( fabs(sceta) < 1.479 ) {
                    if( !config.PassFloat( "cut_mva_crack_highpt_mvanontrig"   , mva_nontrig  ) ) {
                        pass_mva_nontrig =false;
                        pass_mva_nontrig_noiso =false;
                        if( eval_el_mva_nontrig ) continue;
                    }
                }
                else if( fabs(sceta) < 2.5 ) {
                    if( !config.PassFloat( "cut_mva_endcap_highpt_mvanontrig"   , mva_nontrig  ) ) {
                        pass_mva_nontrig =false;
                        pass_mva_nontrig_noiso =false;
                        if( eval_el_mva_nontrig ) continue;
                    }
                }
            }


            if( !config.PassFloat( "cut_relpfiso_mvanontrig"   , pfIsoCorr40/pt      ) ) {
                pass_mva_nontrig=false;
                pass_mva_nontrig_onlyiso=false;
                if( eval_el_mva_nontrig ) continue;
            }
            if( !config.PassInt( "cut_misshits_mvanontrig"   , misshits      ) ) {
                pass_mva_nontrig=false;
                pass_mva_nontrig_noiso =false;
                if( eval_el_mva_nontrig ) continue;
            }
            if( !config.PassFloat( "cut_sip_mvanontrig"   , sip     ) ) {
                pass_mva_nontrig=false;
                pass_mva_nontrig_noiso =false;
                if( eval_el_mva_nontrig ) continue;
            }
        }

        // triggering MVA
        if( !use_eval || eval_el_mva_trig) {

            if( pt < 20 ) {
                if( fabs(sceta) < 0.8 ) {
                    if( !config.PassFloat( "cut_mva_central_lowpt_mvatrig"   , mva_trig  ) ) {
                        pass_mva_trig =false;
                        pass_mva_trig_noiso = false;
                        if( eval_el_mva_trig ) continue;
                    }
                }
                else if( fabs(sceta) < 1.479 ) {
                    if( !config.PassFloat( "cut_mva_crack_lowpt_mvatrig"   , mva_trig  ) ) {
                        pass_mva_trig =false;
                        pass_mva_trig_noiso = false;
                        if( eval_el_mva_trig ) continue;
                    }
                }
                else if( fabs(sceta) < 2.5 ) {
                    if( !config.PassFloat( "cut_mva_endcap_lowpt_mvatrig"   , mva_trig  ) ) {
                        pass_mva_trig =false;
                        pass_mva_trig_noiso = false;
                        if( eval_el_mva_trig ) continue;
                    }
                }
            } else {
                if( fabs(sceta) < 0.8 ) {
                    if( !config.PassFloat( "cut_mva_central_highpt_mvatrig"   , mva_trig  ) ) {
                        pass_mva_trig =false;
                        pass_mva_trig_noiso = false;
                        if( eval_el_mva_trig ) continue;
                    }
                }
                else if( fabs(sceta) < 1.479 ) {
                    if( !config.PassFloat( "cut_mva_crack_highpt_mvatrig"   , mva_trig  ) ) {
                        pass_mva_trig =false;
                        pass_mva_trig_noiso = false;
                        if( eval_el_mva_trig ) continue;
                    }
                }
                else if( fabs(sceta) < 2.5 ) {
                    if( !config.PassFloat( "cut_mva_endcap_highpt_mvatrig"   , mva_trig  ) ) {
                        pass_mva_trig =false;
                        pass_mva_trig_noiso = false;
                        if( eval_el_mva_trig ) continue;
                    }
                }
            }

            if( !config.PassFloat( "cut_relpfiso_mvatrig"   , pfIsoCorr40/pt      ) ) {
                pass_mva_trig=false;
                pass_mva_trig_onlyiso=false;
                if( eval_el_mva_trig ) continue;
            }
            if( !config.PassInt( "cut_misshits_mvatrig"   , misshits      ) ) {
                pass_mva_trig=false;
                pass_mva_trig_noiso = false;
                if( eval_el_mva_trig ) continue;
            }
            if( !config.PassInt( "cut_convfit_mvatrig"   , convfit     ) ) {
                pass_mva_trig=false;
                pass_mva_trig_noiso = false;
                if( eval_el_mva_trig ) continue;
            }
        }

        if( !config.PassBool( "cut_pid_tightTrig"  , pass_tightTrig   ) ) continue;
        if( !config.PassBool( "cut_pid_tight"      , pass_tight       ) ) continue;
        if( !config.PassBool( "cut_pid_medium"     , pass_medium      ) ) continue;
        if( !config.PassBool( "cut_pid_loose"      , pass_loose       ) ) continue;
        if( !config.PassBool( "cut_pid_veryloose"  , pass_veryloose   ) ) continue;
        if( !config.PassBool( "cut_pid_mva_trig"   , pass_mva_trig    ) ) continue;
        if( !config.PassBool( "cut_pid_mva_nontrig", pass_mva_nontrig ) ) continue;

        OUT::el_n++;

        OUT::el_pt             -> push_back(pt);
        OUT::el_eta            -> push_back(eta);
        OUT::el_sceta          -> push_back(sceta);
        OUT::el_phi            -> push_back(phi);
        OUT::el_e              -> push_back(pt*cosh(eta));
        OUT::el_pt_uncorr      -> push_back(IN::elePt->at(idx));
        OUT::el_e_uncorr       -> push_back(IN::eleEn->at(idx));
        OUT::el_mva_trig       -> push_back(mva_trig);
        OUT::el_mva_nontrig    -> push_back(mva_nontrig);
        OUT::el_d0pv           -> push_back( d0 );
        OUT::el_z0pv           -> push_back( z0 );
        OUT::el_sigmaIEIE      -> push_back( sigmaIEIE );
        // sigmaIEIE cori
        //
        OUT::el_pfiso30               -> push_back( pfIsoCorr30 );
        OUT::el_pfiso40               -> push_back( pfIsoCorr40 );
        OUT::el_charge                -> push_back( charge );
        OUT::el_hasMatchedConv        -> push_back( convfit );
        OUT::el_passTight             -> push_back(pass_tight);
        OUT::el_passMedium            -> push_back(pass_medium);
        OUT::el_passLoose             -> push_back(pass_loose);
        OUT::el_passVeryLoose         -> push_back(pass_veryloose);
        OUT::el_passTightTrig         -> push_back(pass_tightTrig);
        OUT::el_passMvaTrig           -> push_back(pass_mva_trig);
        OUT::el_passMvaNonTrig        -> push_back(pass_mva_nontrig);
        OUT::el_passMvaTrigNoIso      -> push_back(pass_mva_trig_noiso);
        OUT::el_passMvaNonTrigNoIso   -> push_back(pass_mva_nontrig_noiso);
        OUT::el_passMvaTrigOnlyIso    -> push_back(pass_mva_trig_onlyiso);
        OUT::el_passMvaNonTrigOnlyIso -> push_back(pass_mva_nontrig_onlyiso);
        OUT::el_triggerMatch   -> push_back( trigMatch );

        // check truth matching
        TLorentzVector ellv;
        ellv.SetPtEtaPhiE( pt, eta, phi, en );
        std::vector<int> matchPID;
        matchPID.push_back(11);
        matchPID.push_back(-11);

        float minTruthDR = 100.0;
        TLorentzVector matchLV;
        bool match = HasTruthMatch( ellv, matchPID, 0.2, minTruthDR, matchLV );
        OUT::el_truthMatch_el->push_back( match  );
        OUT::el_truthMinDR_el->push_back( minTruthDR );
        OUT::el_truthMatchPt_el->push_back( matchLV.Pt() );

        //std::vector<int> matchPIDPH;
        //minTruthDR = 100.0;
        //matchLV.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);
        //matchPIDPH.push_back(22);
        //match = HasTruthMatch( ellv, matchPIDPH, 0.2, minTruthDR, matchLV );
        //OUT::el_truthMatch_ph->push_back( matchph );
        //OUT::el_truthMinDR_ph->push_back( minTruthDR );
        //OUT::el_truthMatchPt_ph->push_back( matchLV.Pt() );
        
    }
#endif

}        

float RunModule::get_ele_eff_area( float sceta, int cone ) const {

    float ea = -1;

    if( cone == 3 ) {
        if (fabs(sceta) < 1.0 )                              ea = 0.130;
        else if (fabs(sceta) >= 1.0 && fabs(sceta) < 1.479 ) ea = 0.137;
        else if (fabs(sceta) >= 1.479 && fabs(sceta) < 2.0 ) ea = 0.067;
        else if (fabs(sceta) >= 2.0 && fabs(sceta) < 2.2 )   ea = 0.089;
        else if (fabs(sceta) >= 2.2 && fabs(sceta) < 2.3 )   ea = 0.107;
        else if (fabs(sceta) >= 2.3 && fabs(sceta) < 2.4 )   ea = 0.110;
        else if (fabs(sceta) >= 2.4 )                        ea = 0.138;
        else {
            std::cout << "Did not get Effective Area for eta " << sceta << std::endl;
        }

        //if (fabs(sceta) >= 0.0 && fabs(sceta) < 1.0 ) ea = 0.13;
        //if (fabs(sceta) >= 1.0 && fabs(sceta) < 1.479 ) ea = 0.14;
        //if (fabs(sceta) >= 1.479 && fabs(sceta) < 2.0 ) ea = 0.07;
        //if (fabs(sceta) >= 2.0 && fabs(sceta) < 2.2 ) ea = 0.09;
        //if (fabs(sceta) >= 2.2 && fabs(sceta) < 2.3 ) ea = 0.11;
        //if (fabs(sceta) >= 2.3 && fabs(sceta) < 2.4 ) ea = 0.11;
        //if (fabs(sceta) >= 2.4 ) ea = 0.14;

    }
    else if( cone == 4 ) {

        if (fabs(sceta) < 1.0 )                              ea = 0.208;
        else if (fabs(sceta) >= 1.0 && fabs(sceta) < 1.479 ) ea = 0.209;
        else if (fabs(sceta) >= 1.479 && fabs(sceta) < 2.0 ) ea = 0.115;
        else if (fabs(sceta) >= 2.0 && fabs(sceta) < 2.2 )   ea = 0.143;
        else if (fabs(sceta) >= 2.2 && fabs(sceta) < 2.3 )   ea = 0.183;
        else if (fabs(sceta) >= 2.3 && fabs(sceta) < 2.4 )   ea = 0.194;
        else if (fabs(sceta) >= 2.4 )                        ea = 0.261;
        else {
            std::cout << "Did not get Effective Area for eta " << sceta << std::endl;
        }

    }
    else {
        std::cout << "Cone size must be 3 or 4" << std::endl;
    }

    return ea;
}

void RunModule::BuildJet( ModuleConfig & config ) const {

    OUT::jet_pt             -> clear();
    OUT::jet_eta            -> clear();
    OUT::jet_phi            -> clear();
    OUT::jet_e              -> clear();
    OUT::jet_JECUnc         -> clear();
    OUT::jet_NCH            -> clear();
    OUT::jet_Nconstitutents -> clear();
    OUT::jet_NEF            -> clear();
    OUT::jet_CEF            -> clear();
    OUT::jet_CHF            -> clear();
    OUT::jet_NHF            -> clear();

    OUT::jet_PUIDLoose      -> clear();
    OUT::jet_PUIDMedium     -> clear();
    OUT::jet_PUIDTight      -> clear();

    OUT::jet_CSV            -> clear();

// jet gen variables do not exist for data
#ifdef EXISTS_jetGenJetIndex
    OUT::jet_genIndex       -> clear();
    OUT::jet_genPt          -> clear();
    OUT::jet_genEta         -> clear();
    OUT::jet_genPhi         -> clear();
    OUT::jet_genE           -> clear();
#endif
    OUT::jet_n          = 0;


#ifdef EXISTS_nJet
    for( int idx = 0; idx < IN::nJet; ++idx ) {
        
        float pt  = IN::jetPt->at(idx);
        float eta = IN::jetEta->at(idx);
        float phi = IN::jetPhi->at(idx);
        float en  = IN::jetEn->at(idx);

        if( !config.PassFloat( "cut_pt", pt ) ) continue;
        if( !config.PassFloat( "cut_abseta", eta ) ) continue;

        OUT::jet_pt             -> push_back(pt);
        OUT::jet_eta            -> push_back(eta);
        OUT::jet_phi            -> push_back(phi);
        OUT::jet_e              -> push_back(en);

        OUT::jet_JECUnc         -> push_back( IN::jetJECUnc->at(idx) );

        OUT::jet_NCH            -> push_back( IN::jetNCH->at(idx) );
        OUT::jet_Nconstitutents -> push_back( IN::jetNConstituents->at(idx) );
        OUT::jet_NEF            -> push_back( IN::jetNEF->at(idx) );
        OUT::jet_CEF            -> push_back( IN::jetCEF->at(idx) );
        OUT::jet_CHF            -> push_back( IN::jetCHF->at(idx) );
        OUT::jet_NHF            -> push_back( IN::jetNHF->at(idx) );

        OUT::jet_PUIDLoose      -> push_back( IN::jetPuJetIdL->at(idx) );
        OUT::jet_PUIDMedium     -> push_back( IN::jetPuJetIdM->at(idx) );
        OUT::jet_PUIDTight      -> push_back( IN::jetPuJetIdT->at(idx) );

        OUT::jet_CSV            -> push_back( IN::jetCombinedSecondaryVtxBJetTags->at(idx) );

// jet gen variables do not exist for data
#ifdef EXISTS_jetGenJetIndex
        OUT::jet_genIndex       ->push_back( IN::jetGenJetIndex->at(idx) );
        OUT::jet_genPt          ->push_back( IN::jetGenJetPt   ->at(idx) );
        OUT::jet_genEta         ->push_back( IN::jetGenJetEta  ->at(idx) );
        OUT::jet_genPhi         ->push_back( IN::jetGenJetPhi  ->at(idx) );
        OUT::jet_genE           ->push_back( IN::jetGenJetEn   ->at(idx) );
#endif
            
        OUT::jet_n++;
    }
#endif
            
}        

void RunModule::BuildPhoton( ModuleConfig & config ) const {

    OUT::ph_pt                     -> clear();
    OUT::ph_eta                    -> clear();
    OUT::ph_sceta                  -> clear();
    OUT::ph_phi                    -> clear();
    OUT::ph_e                      -> clear();
    OUT::ph_scE                    -> clear();
    OUT::ph_pt_uncorr              -> clear();
    OUT::ph_HoverE                 -> clear();
    OUT::ph_HoverE12               -> clear();
    OUT::ph_sigmaIEIE              -> clear();
    OUT::ph_sigmaIEIP              -> clear();
    OUT::ph_r9                     -> clear();
    OUT::ph_E1x3                   -> clear();
    OUT::ph_E2x2                   -> clear();
    OUT::ph_E5x5                   -> clear();
    OUT::ph_E2x5Max                -> clear();
    OUT::ph_SCetaWidth             -> clear();
    OUT::ph_SCphiWidth             -> clear();
    OUT::ph_ESEffSigmaRR           -> clear();
    OUT::ph_hcalIsoDR03            -> clear();
    OUT::ph_trkIsoHollowDR03       -> clear();
    OUT::ph_chgpfIsoDR02           -> clear();
    OUT::ph_pfChIsoWorst           -> clear();
    OUT::ph_chIso                  -> clear();
    OUT::ph_neuIso                 -> clear();
    OUT::ph_phoIso                 -> clear();
    OUT::ph_chIsoCorr              -> clear();
    OUT::ph_neuIsoCorr             -> clear();
    OUT::ph_phoIsoCorr             -> clear();
    OUT::ph_SCRChIso               -> clear();
    OUT::ph_SCRPhoIso              -> clear();
    OUT::ph_SCRNeuIso              -> clear();
    OUT::ph_SCRChIso04             -> clear();
    OUT::ph_SCRPhoIso04            -> clear();
    OUT::ph_SCRNeuIso04            -> clear();
    OUT::ph_RandConeChIso          -> clear();
    OUT::ph_RandConePhoIso         -> clear();
    OUT::ph_RandConeNeuIso         -> clear();
    OUT::ph_RandConeChIso04        -> clear();
    OUT::ph_RandConePhoIso04       -> clear();
    OUT::ph_RandConeNeuIso04       -> clear();
    OUT::ph_eleVeto                -> clear();
    OUT::ph_hasPixSeed             -> clear();
    OUT::ph_drToTrk                -> clear();
    OUT::ph_isConv                 -> clear();
    OUT::ph_conv_nTrk              -> clear();
    OUT::ph_conv_vtx_x             -> clear();
    OUT::ph_conv_vtx_y             -> clear();
    OUT::ph_conv_vtx_z             -> clear();
    OUT::ph_conv_ptin1             -> clear();
    OUT::ph_conv_ptin2             -> clear();
    OUT::ph_conv_ptout1            -> clear();
    OUT::ph_conv_ptout2            -> clear();
    OUT::ph_passLoose              -> clear();
    OUT::ph_passLooseNoSIEIE       -> clear();
    OUT::ph_passHOverELoose         -> clear();
    OUT::ph_passHOverEMedium        -> clear();
    OUT::ph_passHOverETight         -> clear();
    OUT::ph_passSIEIELoose         -> clear();
    OUT::ph_passSIEIEMedium        -> clear();
    OUT::ph_passSIEIETight         -> clear();
    OUT::ph_passChIsoCorrLoose     -> clear();
    OUT::ph_passChIsoCorrMedium    -> clear();
    OUT::ph_passChIsoCorrTight     -> clear();
    OUT::ph_passNeuIsoCorrLoose    -> clear();
    OUT::ph_passNeuIsoCorrMedium   -> clear();
    OUT::ph_passNeuIsoCorrTight    -> clear();
    OUT::ph_passPhoIsoCorrLoose    -> clear();
    OUT::ph_passPhoIsoCorrMedium   -> clear();
    OUT::ph_passPhoIsoCorrTight    -> clear();
    OUT::ph_passMedium             -> clear();
    OUT::ph_passTight              -> clear();
    OUT::ph_truthMatch_el          -> clear();
    OUT::ph_truthMinDR_el          -> clear();
    OUT::ph_truthMatchPt_el        -> clear();
    OUT::ph_truthMatch_ph          -> clear();
    OUT::ph_truthMinDR_ph          -> clear();
    OUT::ph_truthMatchPt_ph        -> clear();
    OUT::ph_truthMatchMotherPID_ph -> clear();
    OUT::ph_hasSLConv              -> clear();
    OUT::ph_pass_mva_presel        -> clear();
    OUT::ph_mvascore               -> clear();
    OUT::ph_IsEB                   -> clear();
    OUT::ph_IsEE                   -> clear();
    OUT::ph_n          = 0;


#ifdef EXISTS_nPho
    for( int idx = 0; idx < IN::nPho; ++idx ) {
        float pt        = IN::phoEt->at(idx);
        float eta       = IN::phoEta->at(idx);
        float sceta     = IN::phoSCEta->at(idx);
        float phi       = IN::phoPhi->at(idx);
        float en        = IN::phoE->at(idx);
        float SCRawE    = IN::phoSCRawE->at(idx);
        float esE       = IN::phoESEn->at(idx);

        float rho = IN::rho2012;

        int   eleVeto      = IN::phoEleVeto->at(idx);
        float hovere       = IN::phoHoverE->at(idx);
        float hovere12     = IN::phoHoverE12->at(idx);
        float sigmaIEIE    = IN::phoSigmaIEtaIEta->at(idx);
        float sigmaIEIP    = IN::phoSigmaIEtaIPhi->at(idx);
        float r9           = IN::phoR9->at(idx);
        int   pixseed      = IN::phohasPixelSeed->at(idx);
        float drToTrk      = IN::phoCiCdRtoTrk->at(idx);
        float E1x3         = IN::phoE1x3->at(idx);
        float E2x2         = IN::phoE2x2->at(idx);
        float E5x5         = IN::phoE5x5->at(idx);
        // E2x5Max is duplicated in some ntuples. 
        // Get the index by checking the relative sizes
        unsigned dupidx = idx*IN::phoE2x5Max->size()/IN::nPho;
        float E2x5Max      = IN::phoE2x5Max->at(dupidx);
        float SCetaWidth   = IN::phoSCEtaWidth->at(idx);
        float SCphiWidth   = IN::phoSCPhiWidth->at(idx);
        float ESEffSigmaRR = IN::phoESEffSigmaRR_x->at(idx);

        // sigmaIEIE corr
        float r9Corr = r9;
        if( !IN::isData ) {
            if( fabs(sceta) < 1.479 ) {
                r9Corr = 0.000740 + 1.00139*r9;
                // correct sieie in MC
                sigmaIEIE =  0.0009133 + 0.891832*sigmaIEIE;
            }
            else {
                r9Corr = -0.000399 + 1.00016*r9;
            }
        }
        // photon mometum correction
        #ifdef EXISTS_isData
        #ifdef EXISTS_run
        if( apply_photon_corrections ) {

            bool iseb = false;
            if( fabs(sceta) < 1.479 ) {
                iseb = true;
            }
            float scale = 1.0;
            if( IN::isData ) {
                // last 2 args aren't used
                scale = eleCorr->ScaleCorrection(IN::run, iseb, r9, sceta, pt, 0, 0 );
            }
            else {
                scale = eleCorr->getSmearing(IN::run, en, iseb, r9, sceta );
            }

            pt*=scale;
            en*=scale;
        }
        #endif
        #endif

        // evaluate largest isolation value
        float phoPFChIsoWorst = 0;
        for (unsigned k = 0; k < IN::phoCiCPF4chgpfIso03->at(idx).size(); ++k) {
            if (phoPFChIsoWorst < IN::phoCiCPF4chgpfIso03->at(idx)[k]) {
                phoPFChIsoWorst = IN::phoCiCPF4chgpfIso03->at(idx)[k];
            }
        }

        float hcalIsoDR03      = IN::phoHcalIsoDR03->at(idx);
        float trkIsoHollowDR03 = IN::phoTrkIsoHollowDR03->at(idx);
        float chgpfIsoDR02     = IN::phoCiCPF4chgpfIso02->at(idx).at(0);

        float hcalIsoDR03PtCorr      = hcalIsoDR03 - 0.005 * pt;
        float trkIsoHollowDR03PtCorr = trkIsoHollowDR03  - 0.002 * pt;

        float pfChIso     = IN::phoPFChIso->at(idx);
        float pfNeuIso    = IN::phoPFNeuIso->at(idx);
        float pfPhoIso    = IN::phoPFPhoIso->at(idx);

        float pfChIsoRhoCorr = 0.0;
        float pfNeuIsoRhoCorr = 0.0;
        float pfPhoIsoRhoCorr = 0.0;
        calc_corr_iso( pfChIso, pfPhoIso, pfNeuIso, rho, eta, pfChIsoRhoCorr, pfPhoIsoRhoCorr, pfNeuIsoRhoCorr);

        float pfChIsoPtRhoCorr  = pfChIsoRhoCorr;
        float pfNeuIsoPtRhoCorr = pfNeuIsoRhoCorr-0.04*pt;
        float pfPhoIsoPtRhoCorr = pfPhoIsoRhoCorr-0.005*pt;


        if( !config.PassFloat( "cut_pt"    , pt       ) ) continue;
        if( !config.PassFloat( "cut_abseta"    , fabs(sceta)       ) ) continue;
        if( !config.PassFloat( "cut_abseta_crack"    , fabs(sceta)       ) ) continue;
        if( !config.PassBool ( "cut_eveto"     , eleVeto) ) continue;
        if( !config.PassBool ( "cut_drToTrk"     , drToTrk ) ) continue;

        bool pass_loose         = true;
        bool pass_loose_nosieie = true;
        bool pass_hovere        = true;
        bool pass_medium        = true;
        bool pass_tight         = true;
        bool pass_mva_presel        = true;

        bool pass_sieie_loose   = true;
        bool pass_sieie_medium   = true;
        bool pass_sieie_tight   = true;

        bool pass_chIsoCorr_loose   = true;
        bool pass_chIsoCorr_medium   = true;
        bool pass_chIsoCorr_tight   = true;

        bool pass_neuIsoCorr_loose   = true;
        bool pass_neuIsoCorr_medium   = true;
        bool pass_neuIsoCorr_tight   = true;

        bool pass_phoIsoCorr_loose   = true;
        bool pass_phoIsoCorr_medium   = true;
        bool pass_phoIsoCorr_tight   = true;

        bool pass_hovere_loose   = true;
        bool pass_hovere_medium   = true;
        bool pass_hovere_tight   = true;

        bool use_eval = eval_ph_tight || eval_ph_medium || eval_ph_loose;

        if( fabs(sceta) < 1.479 ) { // barrel

            //loose 
            if( !use_eval || eval_ph_loose ) {
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_loose"   , sigmaIEIE         ) ) {
                    pass_loose=false;
                    pass_sieie_loose=false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_barrel_loose"   , pfChIsoPtRhoCorr  ) ) {
                    pass_loose=false;
                    pass_chIsoCorr_loose = false;
                    pass_loose_nosieie=false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_barrel_loose"  , pfNeuIsoPtRhoCorr ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_neuIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_barrel_loose"  , pfPhoIsoPtRhoCorr ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_phoIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_loose"  , hovere12) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_hovere_loose = false;
                    if( eval_ph_loose ) continue;
                }

            }

            // medium
            if( !use_eval || eval_ph_medium ) {
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_medium"  , sigmaIEIE         ) ) {
                    pass_medium=false;
                    pass_sieie_medium=false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_barrel_medium"  , pfChIsoPtRhoCorr  ) ) {
                    pass_medium=false;
                    pass_chIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_barrel_medium" , pfNeuIsoPtRhoCorr ) ) {
                    pass_medium=false;
                    pass_neuIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_barrel_medium" , pfPhoIsoPtRhoCorr ) ) {
                    pass_medium=false;
                    pass_phoIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_medium" , hovere12) ) {
                    pass_medium=false;
                    pass_hovere_medium = false;
                    if( eval_ph_medium ) continue;
                }
            }

            // tight
            if( !use_eval || eval_ph_tight ) {
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_tight"   , sigmaIEIE         ) ) {
                    pass_tight=false;
                    pass_sieie_tight=false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_barrel_tight"   , pfChIsoPtRhoCorr  ) ) {
                    pass_tight=false;
                    pass_chIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_barrel_tight"  , pfNeuIsoPtRhoCorr ) ) {
                    pass_tight=false;
                    pass_neuIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_barrel_tight"  , pfPhoIsoPtRhoCorr ) ) {
                    pass_tight=false;
                    pass_phoIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_tight"  , hovere12) ) {
                    pass_tight=false;
                    pass_hovere_tight = false;
                    if( eval_ph_tight ) continue;
                }
            }

            // mva
            if( r9 <= 0.9 ) {
                if( !config.PassFloat( "cut_hovere12_barrel_mva_presel_smallr9" , hovere12 ) ) pass_mva_presel = false; 
                if( !config.PassFloat( "cut_hcalIsoEtCorr_barrel_mva_presel_smallr9" , hcalIsoDR03PtCorr) ) pass_mva_presel = false; 
                if( !config.PassFloat( "cut_trkIsoEtCorr_barrel_mva_presel_smallr9" , trkIsoHollowDR03PtCorr) ) pass_mva_presel = false; 
            }
            else {
                if( !config.PassFloat( "cut_hovere12_barrel_mva_presel_larger9" , hovere12 ) ) pass_mva_presel = false; 
                if( !config.PassFloat( "cut_hcalIsoEtCorr_barrel_mva_presel_larger9" , hcalIsoDR03PtCorr) ) pass_mva_presel = false; 
                if( !config.PassFloat( "cut_trkIsoEtCorr_barrel_mva_presel_larger9" , trkIsoHollowDR03PtCorr) ) pass_mva_presel = false; 
            }

            if( !config.PassFloat( "cut_sigmaIEIE_barrel_mva_presel" , sigmaIEIE ) ) pass_mva_presel = false; 
            if( !config.PassFloat( "cut_chgpfIso_barrel_mva_presel" , chgpfIsoDR02 ) ) pass_mva_presel = false; 

        }
        else { // endcap
            // loose
            if( !use_eval || eval_ph_loose ) {
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_loose"   , sigmaIEIE         ) ) {
                    pass_loose=false;
                    pass_sieie_loose=false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_endcap_loose"   , pfChIsoPtRhoCorr  ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_chIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_endcap_loose"  , pfNeuIsoPtRhoCorr ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_neuIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_endcap_loose"  , pfPhoIsoPtRhoCorr ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_phoIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_loose"  , hovere12) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_hovere_loose = false;
                    if( eval_ph_loose ) continue;
                }
            }

            // medium
            if( !use_eval || eval_ph_medium ) {
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_medium"  , sigmaIEIE         ) ) {
                    pass_medium=false;
                    pass_sieie_medium=false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_endcap_medium"  , pfChIsoPtRhoCorr  ) ) {
                    pass_medium=false;
                    pass_chIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_endcap_medium" , pfNeuIsoPtRhoCorr ) ) {
                    pass_medium=false;
                    pass_neuIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_endcap_medium" , pfPhoIsoPtRhoCorr ) ) {
                    pass_medium=false;
                    pass_phoIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_medium" , hovere12) ) {
                    pass_medium=false;
                    pass_hovere_medium = false;
                    if( eval_ph_medium ) continue;
                }
            }

            // tight
            if( !use_eval || eval_ph_tight ) {
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_tight"   , sigmaIEIE         ) ) {
                    pass_tight=false;
                    pass_sieie_tight=false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_endcap_tight"   , pfChIsoPtRhoCorr  ) ) {
                    pass_tight=false;
                    pass_chIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_endcap_tight"  , pfNeuIsoPtRhoCorr ) ) {
                    pass_tight=false;
                    pass_neuIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_endcap_tight"  , pfPhoIsoPtRhoCorr ) ) {
                    pass_phoIsoCorr_tight = false;
                    pass_tight=false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_tight"  , hovere12) ) {
                    pass_hovere_tight = false;
                    pass_tight=false;
                    if( eval_ph_tight ) continue;
                }
            }
            // mva
            if( r9 <= 0.9 ) {
                if( !config.PassFloat( "cut_hovere12_endcap_mva_presel_smallr9" , hovere12 ) ) pass_mva_presel = false; 
                if( !config.PassFloat( "cut_hcalIsoEtCorr_endcap_mva_presel_smallr9" , hcalIsoDR03PtCorr) ) pass_mva_presel = false; 
                if( !config.PassFloat( "cut_trkIsoEtCorr_endcap_mva_presel_smallr9" , trkIsoHollowDR03PtCorr) ) pass_mva_presel = false; 
            }
            else {
                if( !config.PassFloat( "cut_hovere12_endcap_mva_presel_larger9" , hovere12 ) ) pass_mva_presel = false; 
                if( !config.PassFloat( "cut_hcalIsoEtCorr_endcap_mva_presel_larger9" , hcalIsoDR03PtCorr) ) pass_mva_presel = false; 
                if( !config.PassFloat( "cut_trkIsoEtCorr_endcap_mva_presel_larger9" , trkIsoHollowDR03PtCorr) ) pass_mva_presel = false; 
            }

            if( !config.PassFloat( "cut_sigmaIEIE_endcap_mva_presel" , sigmaIEIE ) ) pass_mva_presel = false; 
            if( !config.PassFloat( "cut_chgpfIso_endcap_mva_presel" , chgpfIsoDR02 ) ) pass_mva_presel = false; 

        }


        if( !config.PassBool( "cut_pid_tight"    , pass_tight     ) ) continue;
        if( !config.PassBool( "cut_pid_medium"   , pass_medium    ) ) continue;
        if( !config.PassBool( "cut_pid_loose"    , pass_loose     ) ) continue;

        OUT::ph_n++;

        OUT::ph_pt                   -> push_back(pt);
        OUT::ph_eta                  -> push_back(eta);
        OUT::ph_sceta                -> push_back(sceta);
        OUT::ph_phi                  -> push_back(phi);
        OUT::ph_e                    -> push_back(pt*cosh(eta));
        OUT::ph_scE                  -> push_back(SCRawE);
        OUT::ph_pt_uncorr            -> push_back(IN::phoEt->at(idx));
        OUT::ph_HoverE               -> push_back(hovere);
        OUT::ph_HoverE12             -> push_back(hovere12);
        OUT::ph_sigmaIEIE            -> push_back(sigmaIEIE);
        OUT::ph_sigmaIEIP            -> push_back(sigmaIEIP);
        OUT::ph_r9                   -> push_back(r9);
        OUT::ph_E1x3                 -> push_back(E1x3);
        OUT::ph_E2x2                 -> push_back(E2x2);
        OUT::ph_E5x5                 -> push_back(E5x5);
        OUT::ph_E2x5Max              -> push_back(E2x5Max);
        OUT::ph_SCetaWidth           -> push_back(SCetaWidth);
        OUT::ph_SCphiWidth           -> push_back(SCphiWidth);
        OUT::ph_ESEffSigmaRR         -> push_back(ESEffSigmaRR);
        OUT::ph_hcalIsoDR03          -> push_back(hcalIsoDR03);
        OUT::ph_trkIsoHollowDR03     -> push_back(trkIsoHollowDR03);
        OUT::ph_chgpfIsoDR02         -> push_back(chgpfIsoDR02);
        OUT::ph_pfChIsoWorst         -> push_back(phoPFChIsoWorst);
        OUT::ph_chIso                -> push_back(pfChIso);
        OUT::ph_neuIso               -> push_back(pfNeuIso);
        OUT::ph_phoIso               -> push_back(pfPhoIso);
        OUT::ph_chIsoCorr            -> push_back(pfChIsoPtRhoCorr);
        OUT::ph_neuIsoCorr           -> push_back(pfNeuIsoPtRhoCorr);
        OUT::ph_phoIsoCorr           -> push_back(pfPhoIsoPtRhoCorr);
        OUT::ph_SCRChIso             -> push_back(IN::phoSCRChIso->at(idx));
        OUT::ph_SCRPhoIso            -> push_back(IN::phoSCRPhoIso->at(idx));
        OUT::ph_SCRNeuIso            -> push_back(IN::phoSCRNeuIso->at(idx));
        OUT::ph_SCRChIso04           -> push_back(IN::phoSCRChIso04->at(idx));
        OUT::ph_SCRPhoIso04          -> push_back(IN::phoSCRPhoIso04->at(idx));
        OUT::ph_SCRNeuIso04          -> push_back(IN::phoSCRNeuIso04->at(idx));
        OUT::ph_RandConeChIso        -> push_back(IN::phoRandConeChIso->at(idx));
        OUT::ph_RandConePhoIso       -> push_back(IN::phoRandConePhoIso->at(idx));
        OUT::ph_RandConeNeuIso       -> push_back(IN::phoRandConeNeuIso->at(idx));
        OUT::ph_RandConeChIso04      -> push_back(IN::phoRandConeChIso04->at(idx));
        OUT::ph_RandConePhoIso04     -> push_back(IN::phoRandConePhoIso04->at(idx));
        OUT::ph_RandConeNeuIso04     -> push_back(IN::phoRandConeNeuIso04->at(idx));

        OUT::ph_passTight            -> push_back(pass_tight);
        OUT::ph_passMedium           -> push_back(pass_medium);
        OUT::ph_passLoose            -> push_back(pass_loose);
        OUT::ph_passLooseNoSIEIE     -> push_back(pass_loose_nosieie);
        OUT::ph_passHOverELoose      -> push_back(pass_hovere_loose);
        OUT::ph_passHOverEMedium     -> push_back(pass_hovere_medium);
        OUT::ph_passHOverETight      -> push_back(pass_hovere_tight);
        OUT::ph_passSIEIELoose       -> push_back(pass_sieie_loose);
        OUT::ph_passSIEIEMedium      -> push_back(pass_sieie_medium);
        OUT::ph_passSIEIETight       -> push_back(pass_sieie_tight);
        OUT::ph_passChIsoCorrLoose   -> push_back(pass_chIsoCorr_loose);
        OUT::ph_passChIsoCorrMedium  -> push_back(pass_chIsoCorr_medium);
        OUT::ph_passChIsoCorrTight   -> push_back(pass_chIsoCorr_tight);
        OUT::ph_passNeuIsoCorrLoose  -> push_back(pass_neuIsoCorr_loose);
        OUT::ph_passNeuIsoCorrMedium -> push_back(pass_neuIsoCorr_medium);
        OUT::ph_passNeuIsoCorrTight  -> push_back(pass_neuIsoCorr_tight);
        OUT::ph_passPhoIsoCorrLoose  -> push_back(pass_phoIsoCorr_loose);
        OUT::ph_passPhoIsoCorrMedium -> push_back(pass_phoIsoCorr_medium);
        OUT::ph_passPhoIsoCorrTight  -> push_back(pass_phoIsoCorr_tight);
        OUT::ph_eleVeto              -> push_back(eleVeto);
        OUT::ph_hasPixSeed           -> push_back(pixseed);
        OUT::ph_drToTrk              -> push_back(drToTrk);

        bool iseb = false;
        bool isee = false;
        if( fabs(sceta) < 1.44 ) {
            iseb = true;
        }
        if( fabs(sceta) > 1.57 ) {
            isee = true;
        }
        OUT::ph_IsEB -> push_back( iseb );
        OUT::ph_IsEE -> push_back( isee );

        // Evaluate MVA
        if( TMVAReaderEB != 0 && TMVAReaderEE != 0 && pass_mva_presel ) {

            MVAVars::phoPhi           = phi;
            MVAVars::phoR9            = r9Corr;
            MVAVars::phoSigmaIEtaIEta = sigmaIEIE;
            MVAVars::phoSigmaIEtaIPhi = sigmaIEIP;
            MVAVars::s4ratio          = E2x2/E5x5;
            MVAVars::s13              = E1x3/E5x5;
            MVAVars::s25              = E2x5Max/E5x5;
            MVAVars::phoSCEta         = sceta;
            MVAVars::phoSCRawE        = SCRawE;
            MVAVars::phoSCEtaWidth    = SCetaWidth;
            MVAVars::phoSCPhiWidth    = SCphiWidth;
            MVAVars::rho2012          = rho;
            MVAVars::phoPFPhoIso      = pfPhoIso;
            MVAVars::phoPFChIso       = pfChIso;
            MVAVars::phoPFChIsoWorst  = phoPFChIsoWorst;
            MVAVars::phoESEnToRawE    = esE/SCRawE;
            MVAVars::phoESEffSigmaRR  = ESEffSigmaRR;

            OUT::ph_pass_mva_presel->push_back(true);

            if( iseb ) {
                OUT::ph_mvascore->push_back(TMVAReaderEB->EvaluateMVA("BDT"));
            }
            else if( isee ){
                OUT::ph_mvascore->push_back(TMVAReaderEE->EvaluateMVA("BDT"));
            }
            else {
                OUT::ph_mvascore->push_back(-99);
            }
        }
        else {
            OUT::ph_mvascore->push_back(-99);
            OUT::ph_pass_mva_presel->push_back(false);
        }


        // fill conversion info
        // the ntuples fill default values when the
        // photon is not converted, so just keep that

        OUT::ph_isConv           -> push_back(IN::phoIsConv->at(idx));
        OUT::ph_conv_nTrk        -> push_back(IN::phoConvNTrks->at(idx));
        OUT::ph_conv_vtx_x       -> push_back(IN::phoConvVtx_x->at(idx));
        OUT::ph_conv_vtx_y       -> push_back(IN::phoConvVtx_y->at(idx));
        OUT::ph_conv_vtx_z       -> push_back(IN::phoConvVtx_z->at(idx));
        OUT::ph_hasSLConv        -> push_back( (IN::SingleLegConv->at(idx) > 0 ) );
        // get the individual track pt
        // i'm not sure if its pt sorted, so lets
        // do that now to be sure
        float ptin_idx0 = IN::phoConvTrkPin_x->at(idx);
        float ptin_idx1 = IN::phoConvTrkPin_y->at(idx);
        float ptout_idx0 = IN::phoConvTrkPout_x->at(idx);
        float ptout_idx1 = IN::phoConvTrkPout_y->at(idx);
        if( ptin_idx0 > ptin_idx1 ) {
            OUT::ph_conv_ptin1 -> push_back(ptin_idx0);
            OUT::ph_conv_ptin2 -> push_back(ptin_idx1);
        }
        else {
            OUT::ph_conv_ptin2 -> push_back(ptin_idx0);
            OUT::ph_conv_ptin1 -> push_back(ptin_idx1);
        }
        if( ptout_idx0 > ptout_idx1 ) {
            OUT::ph_conv_ptout1 -> push_back(ptout_idx0);
            OUT::ph_conv_ptout2 -> push_back(ptout_idx1);
        }
        else {
            OUT::ph_conv_ptout2 -> push_back(ptout_idx0);
            OUT::ph_conv_ptout1 -> push_back(ptout_idx1);
        }

        TLorentzVector phlv;
        phlv.SetPtEtaPhiE( pt, eta, phi, en );
        std::vector<int> matchPID;
        matchPID.push_back(22);

        float minTruthDR = 100.0;
        TLorentzVector matchLV;
        int matchMotherPID=0;
        bool match = HasTruthMatch( phlv, matchPID, 0.2, minTruthDR, matchLV, matchMotherPID );
        OUT::ph_truthMatch_ph->push_back( match  );
        OUT::ph_truthMinDR_ph->push_back( minTruthDR );
        OUT::ph_truthMatchPt_ph->push_back( matchLV.Pt() );
        OUT::ph_truthMatchMotherPID_ph->push_back( matchMotherPID );

        std::vector<int> matchPIDEl;
        matchPIDEl.push_back(11);
        matchPIDEl.push_back(-11);

        minTruthDR = 100.0;
        matchLV.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);
        match = HasTruthMatch( phlv, matchPIDEl, 0.2, minTruthDR, matchLV );
        OUT::ph_truthMatch_el->push_back( match  );
        OUT::ph_truthMinDR_el->push_back( minTruthDR );
        OUT::ph_truthMatchPt_el->push_back( matchLV.Pt() );
    }
#endif 
            
}        

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;
    if( !config.PassInt("cut_el_n", OUT::el_n ) ) keep_event = false;
    if( !config.PassInt("cut_mu_n", OUT::mu_n ) ) keep_event = false;

    return keep_event;

    
}

void RunModule::WeightEvent( ModuleConfig & config ) const {

    #ifdef EXISTS_isData
    if( IN::isData ) {
        OUT::PUWeight = 1.0;
        OUT::PUWeightDN5 = 1.0;
        OUT::PUWeightDN10 = 1.0;

        OUT::PUWeightUP5 = 1.0;
        OUT::PUWeightUP6 = 1.0;
        OUT::PUWeightUP7 = 1.0;
        OUT::PUWeightUP8 = 1.0;
        OUT::PUWeightUP9 = 1.0;
        OUT::PUWeightUP10 = 1.0;
        OUT::PUWeightUP11 = 1.0;
        OUT::PUWeightUP12 = 1.0;
        OUT::PUWeightUP13 = 1.0;
        OUT::PUWeightUP14 = 1.0;
        OUT::PUWeightUP15 = 1.0;
        OUT::PUWeightUP16 = 1.0;
        OUT::PUWeightUP17 = 1.0;
        return;
    }
    #endif

    if( !puweight_data_hist || !puweight_sample_hist ) {
        std::cout << "WeightEvent::ERROR - Needed histogram does not exist! " << std::endl;
        return;
    }
    float puval = -1;
    #ifdef EXISTS_puTrue
    puval = IN::puTrue->at(0);
    #endif
    //#ifdef EXISTS_nVtx
    //puval = IN::nVtx;
    //#endif

    
    OUT::PUWeight = calc_pu_weight( puval );

    OUT::PUWeightUP5 = calc_pu_weight( puval, 1.05 );
    OUT::PUWeightUP6 = calc_pu_weight( puval, 1.06 );
    OUT::PUWeightUP7 = calc_pu_weight( puval, 1.07 );
    OUT::PUWeightUP8 = calc_pu_weight( puval, 1.08 );
    OUT::PUWeightUP9 = calc_pu_weight( puval, 1.09 );
    OUT::PUWeightUP10 = calc_pu_weight( puval, 1.10 );
    OUT::PUWeightUP11 = calc_pu_weight( puval, 1.11 );
    OUT::PUWeightUP12 = calc_pu_weight( puval, 1.12 );
    OUT::PUWeightUP13 = calc_pu_weight( puval, 1.13 );
    OUT::PUWeightUP14 = calc_pu_weight( puval, 1.14 );
    OUT::PUWeightUP15 = calc_pu_weight( puval, 1.15 );
    OUT::PUWeightUP16 = calc_pu_weight( puval, 1.16 );
    OUT::PUWeightUP17 = calc_pu_weight( puval, 1.17 );

    OUT::PUWeightDN5 = calc_pu_weight( puval, 0.95 );
    OUT::PUWeightDN10 = calc_pu_weight( puval, 0.9 );
    
}

float RunModule::calc_pu_weight( float puval, float mod ) const {

    float tot_data   = puweight_data_hist->Integral();
    float tot_sample = puweight_sample_hist->Integral();

    int bin_sample = puweight_sample_hist->FindBin(puval);
    int bin_data = puweight_data_hist->FindBin(mod*puval);

    float val_data = puweight_data_hist->GetBinContent( bin_data );
    float val_sample = puweight_sample_hist->GetBinContent( bin_sample );


    float num = val_data*mod/tot_data;
    float den = val_sample/tot_sample;

    float weight = num/den;

    if( weight < 0.005 ) {
        std::cout << "PUweight, " << weight << " is zero for PUVal " << puval << " will average over +- 2.5 to get non-zero value " << std::endl;

        int bin_min_sample = puweight_sample_hist->FindBin(puval-2.5);
        int bin_max_sample = puweight_sample_hist->FindBin(puval+2.5);
        int bin_min_data = puweight_data_hist->FindBin(puval*mod-2.5);
        int bin_max_data = puweight_data_hist->FindBin(puval*mod+2.5);

        val_data = puweight_data_hist->Integral(bin_min_data, bin_max_data);
        val_sample = puweight_sample_hist->Integral(bin_min_sample, bin_max_sample);

        num = val_data/tot_data;
        den = val_sample/tot_sample;

        weight = num/den;

        if( weight < 0.005 ) {
            std::cout << "PUweight is still zero!" << std::endl;
        }

    }
    return weight;
}

bool RunModule::HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR ) const {
    
    float minDR = 100.0;
    TLorentzVector matchLV;
    return HasTruthMatch( objlv, matchPID, maxDR, minDR, matchLV );

}

bool RunModule::HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR ) const {
    
    TLorentzVector matchLV;
    return HasTruthMatch( objlv, matchPID, maxDR, minDR, matchLV );

}

bool RunModule::HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR, TLorentzVector &matchLV ) const {
    
    int motherPID = 0;
    return HasTruthMatch( objlv, matchPID, maxDR, minDR, matchLV, motherPID );

}

bool RunModule::HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float & minDR, TLorentzVector & matchLV, int &matchMotherPID ) const {
   
    minDR = 100.0;
    matchLV.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);
    bool match=false;

    //std::cout << "CHECK for " << matchPID[0] << std::endl;
    #ifdef EXISTS_nMC
    for( int mcidx = 0; mcidx < IN::nMC; mcidx++ ) {
        
        if( std::find( matchPID.begin(), matchPID.end(), IN::mcPID->at(mcidx) ) == matchPID.end() ) continue;
        //std::cout << " Match PID " << IN::mcPID->at(mcidx) << " status " << IN::mcStatus->at(mcidx) << std::endl;

        #ifdef EXISTS_mcStatus
        if( IN::mcStatus->at(mcidx) != 1 ) continue;
        #endif

        TLorentzVector mclv;
        mclv.SetPtEtaPhiE( IN::mcPt->at(mcidx), IN::mcEta->at(mcidx), IN::mcPhi->at(mcidx), IN::mcE->at(mcidx) );
        float dr = mclv.DeltaR( objlv );
        //std::cout << "dr = " << dr << std::endl;
        if( dr < maxDR) {
            match = true;
            matchMotherPID = IN::mcMomPID->at(mcidx);
        }
        // store the minimum delta R
        if( dr < minDR ) {
            minDR = dr;
            matchLV = mclv;
        }
    }
    #endif

    return match;

}

void RunModule::calc_corr_iso( float chIso, float phoIso, float neuIso, float rho, float eta, float &chIsoCorr, float &phoIsoCorr, float &neuIsoCorr )  const
{

    float ea_ch=0.0;
    float ea_pho=0.0;
    float ea_neu=0.0;

    if( fabs( eta ) < 1.0 ) {
        ea_ch = 0.012;
        ea_neu = 0.03;
        ea_pho = 0.148;
    }
    else if( fabs(eta) >= 1.0 && fabs( eta ) < 1.479 ) {
        ea_ch = 0.01;
        ea_neu = 0.057;
        ea_pho = 0.13;
    }
    else if( fabs(eta) >= 1.479 && fabs( eta ) < 2.0 ) {
        ea_ch = 0.014;
        ea_neu = 0.039;
        ea_pho = 0.112;
    }
    else if( fabs(eta) >= 2.0 && fabs( eta ) < 2.2 ) {
        ea_ch = 0.012;
        ea_neu = 0.015;
        ea_pho = 0.216;
    }
    else if( fabs(eta) >= 2.2 && fabs( eta ) < 2.3 ) {
        ea_ch = 0.016;
        ea_neu = 0.024;
        ea_pho = 0.262;
    }
    else if( fabs(eta) >= 2.3 && fabs( eta ) < 2.4 ) {
        ea_ch = 0.02;
        ea_neu = 0.039;
        ea_pho = 0.260;
    }
    else if( fabs(eta) >= 2.4 ) {
        ea_ch = 0.012;
        ea_neu = 0.072;
        ea_pho = 0.266;
    }

    chIsoCorr  = chIso  - rho*ea_ch;
    phoIsoCorr = phoIso - rho*ea_pho;
    neuIsoCorr = neuIso - rho*ea_neu;

    if( chIsoCorr < 0 ) {
        chIsoCorr = 0;
    }
    if( phoIsoCorr < 0 ) {
        phoIsoCorr = 0;
    }
    if( neuIsoCorr < 0 ) {
        neuIsoCorr = 0;
    }

}

float RunModule::GetElectronMomentumCorrection( float pt, float sceta, float eta, float r9, bool isData, int run ) {

    bool isEB = (fabs(sceta) < 1.479);

    if( isData ) {

        if( !electron_corr_vals.size() ) {
            std::cout << "No values loaded for data corrections " << std::endl;
            return 1.0;
        }

        float scale = -1;
        bool set_scale = false;
        BOOST_FOREACH( const correctionValues & vals, electron_corr_vals ) {

            if ( (run >= vals.nRunMin ) && ( run <= vals.nRunMax ) ) {

                if ( isEB  && fabs(eta) < 1  && r9 <  0.94 ) scale = vals.corrCat0;
                if ( isEB  && fabs(eta) < 1  && r9 >= 0.94 ) scale = vals.corrCat1;
                if ( isEB  && fabs(eta) >= 1 && r9 <  0.94 ) scale = vals.corrCat2;
                if ( isEB  && fabs(eta) >= 1 && r9 >= 0.94 ) scale = vals.corrCat3;
                if ( !isEB && fabs(eta) < 2  && r9 <  0.94 ) scale = vals.corrCat4;
                if ( !isEB && fabs(eta) < 2  && r9 >= 0.94 ) scale = vals.corrCat5;
                if ( !isEB && fabs(eta) >= 2 && r9 <  0.94 ) scale = vals.corrCat6;
                if ( !isEB && fabs(eta) >= 2 && r9 >= 0.94 ) scale = vals.corrCat7;

                if( scale < 0 ) {
                    std::cout << "Did not get a scale " << std::endl;
                    break;
                }

                set_scale = true;
            }
        }

        if( !set_scale ) {
            std::cout << "Did not set a scale, check input vals " << std::endl;
            return 1.0;
        }
        else {
            return scale;
        }
    }
    else {

        float dsigMC = 0;
        if ( isEB  && fabs(eta) <  1 && r9 <  0.94 ) dsigMC = 0.0099;
        if ( isEB  && fabs(eta) <  1 && r9 >= 0.94 ) dsigMC = 0.0103;
        if ( isEB  && fabs(eta) >= 1 && r9 <  0.94 ) dsigMC = 0.0219;
        if ( isEB  && fabs(eta) >= 1 && r9 >= 0.94 ) dsigMC = 0.0158;
        if ( !isEB && fabs(eta) <  2 && r9 <  0.94 ) dsigMC = 0.0222;
        if ( !isEB && fabs(eta) <  2 && r9 >= 0.94 ) dsigMC = 0.0298;
        if ( !isEB && fabs(eta) >= 2 && r9 <  0.94 ) dsigMC = 0.0318;
        if ( !isEB && fabs(eta) >= 2 && r9 >= 0.94 ) dsigMC = 0.0302;   

        float corr = _rand.Gaus( 1.0, dsigMC );
        return corr; 
    }

}

void RunModule::extractElectronCorrections( const std::string & filename ) {

    ifstream file( filename.c_str() );

    if( !file ) {
        std::cout << "Could not open file " << filename << std::endl;
        return;
    }

    electron_corr_vals.clear();

    while( !file.eof() ) {

        std::string line;
        getline( file, line );
        if( line.empty() ) continue;
        std::vector<std::string> line_tok = Tokenize( line, ", " );
        if( line_tok.size() != 10 ) {
            std::cout << "Did not read the correct number of lines! " << std::endl;
            continue;
        }

        correctionValues vals;
        bool all_success = true;
        all_success &= Utils::stringToInt(line_tok[0], vals.nRunMin);
        all_success &= Utils::stringToInt(line_tok[1], vals.nRunMax);
        all_success &= Utils::stringToDouble(line_tok[2], vals.corrCat0);
        all_success &= Utils::stringToDouble(line_tok[3], vals.corrCat1);
        all_success &= Utils::stringToDouble(line_tok[4], vals.corrCat2);
        all_success &= Utils::stringToDouble(line_tok[5], vals.corrCat3);
        all_success &= Utils::stringToDouble(line_tok[6], vals.corrCat4);
        all_success &= Utils::stringToDouble(line_tok[7], vals.corrCat5);
        all_success &= Utils::stringToDouble(line_tok[8], vals.corrCat6);
        all_success &= Utils::stringToDouble(line_tok[9], vals.corrCat7);

        if( !all_success ) {
            std::cout << "Failed to set at least some electron correction values" << std::endl;
        }

        electron_corr_vals.push_back(vals);

    }

    file.close();

}


void RunModule::extractElectronLinCorrections( const std::string & filename ) {

    ifstream file( filename.c_str() );

    if( !file ) {
        std::cout << "Could not open file " << filename << std::endl;
        return;
    }

    electron_lincorr_vals.clear();
    while( !file.eof() ) {

        std::string line;
        getline( file, line );
        if( line.empty() ) continue;
        std::vector<std::string> line_tok = Tokenize( line, ", " );
        if( line_tok.size() != 8 ) {
            std::cout << "Did not read the correct number of lines! " << std::endl;
            continue;
        }

        linearityCorrectionValues vals;
        bool all_success=true;
        all_success &= Utils::stringToDouble(line_tok[0], vals.ptMin);
        all_success &= Utils::stringToDouble(line_tok[1], vals.ptMax);
        all_success &= Utils::stringToDouble(line_tok[2], vals.corrCat0);
        all_success &= Utils::stringToDouble(line_tok[3], vals.corrCat1);
        all_success &= Utils::stringToDouble(line_tok[4], vals.corrCat2);
        all_success &= Utils::stringToDouble(line_tok[5], vals.corrCat3);
        all_success &= Utils::stringToDouble(line_tok[6], vals.corrCat4);
        all_success &= Utils::stringToDouble(line_tok[7], vals.corrCat5);

        if( !all_success ) {
            std::cout << "Failed to set at least some electron linear correction values" << std::endl;
        }
        electron_lincorr_vals.push_back(vals);

    }

    file.close();

}

void RunModule::BuildTriggerBits( ModuleConfig & config ) const {

    OUT::passTrig_ele27WP80  = ( IN::HLT[IN::HLTIndex[17]] > 0 );
    OUT::passTrig_mu24eta2p1 = ( IN::HLT[IN::HLTIndex[18]] > 0 );
    OUT::passTrig_mu24       = ( IN::HLT[IN::HLTIndex[19]] > 0 );
    OUT::passTrig_mu17_mu8   = ( IN::HLT[IN::HLTIndex[13]] > 0 );
    OUT::passTrig_mu17_Tkmu8   = ( IN::HLT[IN::HLTIndex[14]] > 0 );
    OUT::passTrig_ele17_ele8_9   = ( IN::HLT[IN::HLTIndex[9]] > 0 );
    OUT::passTrig_ele17_ele8_22   = ( IN::HLT[IN::HLTIndex[22]] > 0 );
    
}

bool RunModule::FilterTrigger( ModuleConfig & config ) const {
    
//#ifdef EXISTS_HLT
    bool keep_evt = false;
    BOOST_FOREACH( const Cut & cut, config.GetCut("cut_trigger").GetCuts() ) {
       if( IN::HLT[IN::HLTIndex[cut.val_int] ] > 0 ) keep_evt = true;
    }

    return keep_evt;
//#else 
//    return true;
//#endif
}

void RunModule::finalize() {
    if( muCorr ) {
        delete muCorr;
        muCorr = 0;
   }
    if( eleCorr ) {
        delete eleCorr;
        eleCorr = 0;
   }
}

RunModule::RunModule() : TMVAReaderEB(0), TMVAReaderEE(0)
{
} 
    
