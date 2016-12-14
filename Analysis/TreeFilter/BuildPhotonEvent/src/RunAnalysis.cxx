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
#include "CalcPhotonEventVars.h"

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
    OUT::dr_leadLep_phot                         = 0;
    OUT::dr_sublLep_phot                         = 0;
    OUT::dphi_leadLep_phot                       = 0;
    OUT::dphi_sublLep_phot                       = 0;
    OUT::m_leplep_phot                           = 0;
    OUT::m_diphot                                = 0;
    OUT::dr_diphot                               = 0;
    OUT::dphi_diphot                             = 0;
    OUT::pt_diphot                               = 0;
    OUT::m_leplep_diphot                         = 0;


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
    OUT::ptSorted_ph_mediumNoChIsoNoSIEIENoEleVeto_idx  = 0;
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
    outtree->Branch("el_pt25_n"                    , &OUT::el_pt25_n                    , "el_pt25_n/I"                    );
    outtree->Branch("el_passtrig_n"                , &OUT::el_passtrig_n                , "el_passtrig_n/I"                );
    outtree->Branch("el_passtrig28_n"              , &OUT::el_passtrig28_n              , "el_passtrig28_n/I"              );
    outtree->Branch("ph_mediumNoEleVeto_n"         , &OUT::ph_mediumNoEleVeto_n         , "ph_mediumNoEleVeto_n/I"         );
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
    outtree->Branch("ph_mediumNoChIsoNoSIEIENoEleVeto_n"  , &OUT::ph_mediumNoChIsoNoSIEIENoEleVeto_n  , "ph_mediumNoChIsoNoSIEIENoEleVeto_n/I"  );
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

    outtree->Branch("mt_lep_met"            , &OUT::mt_lep_met    , "mt_lep_met/F"           );
    outtree->Branch("dphi_met_lep1"            , &OUT::dphi_met_lep1, "dphi_met_lep1/F"           );
    outtree->Branch("dphi_met_lep2"            , &OUT::dphi_met_lep2, "dphi_met_lep2/F"           );
    outtree->Branch("m_leplep"            , &OUT::m_leplep           , "m_leplep/F"           );
    outtree->Branch("m_mumu"            , &OUT::m_mumu           , "m_mumu/F"           );
    outtree->Branch("m_elel"            , &OUT::m_elel           , "m_elel/F"           );
    outtree->Branch("m_3lep"              , &OUT::m_3lep             , "m_3lep/F"             );
    outtree->Branch("m_4lep"              , &OUT::m_4lep             , "m_4lep/F"             );
    outtree->Branch("pt_leplep"           , &OUT::pt_leplep          , "pt_leplep/F"          );

    outtree->Branch("dphi_met_phot"        , &OUT::dphi_met_phot        );
    outtree->Branch("m_leadLep_phot"       , &OUT::m_leadLep_phot       );
    outtree->Branch("m_sublLep_phot"       , &OUT::m_sublLep_phot       );
    outtree->Branch("dr_leadLep_phot"      , &OUT::dr_leadLep_phot      );
    outtree->Branch("dr_sublLep_phot"      , &OUT::dr_sublLep_phot      );
    outtree->Branch("dphi_leadLep_phot"    , &OUT::dphi_leadLep_phot    );
    outtree->Branch("dphi_sublLep_phot"    , &OUT::dphi_sublLep_phot    );
    outtree->Branch("m_leplep_phot"        , &OUT::m_leplep_phot        );
    outtree->Branch("m_diphot"             , &OUT::m_diphot             );
    outtree->Branch("dr_diphot"            , &OUT::dr_diphot            );
    outtree->Branch("dphi_diphot"          , &OUT::dphi_diphot          );
    outtree->Branch("pt_diphot"            , &OUT::pt_diphot            );
    outtree->Branch("m_leplep_diphot"      , &OUT::m_leplep_diphot      );

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
    outtree->Branch("ptSorted_ph_mediumNoChIsoNoSIEIENoEleVeto_idx"  , &OUT::ptSorted_ph_mediumNoChIsoNoSIEIENoEleVeto_idx );
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

    bool keep_evt = true;

    if( config.GetName() == "FilterElectron" ) {
        FilterElectron( config );
    }
    if( config.GetName() == "FilterMuon" ) {
        FilterMuon( config );
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

void RunModule::FilterElectron( ModuleConfig & config ) const {

    #ifdef EXISTS_el_n
    OUT::el_n = 0;
    ClearOutputPrefix("el_");

    // save which photon overlaps with 
    // electrons
    std::vector<Bool_t> ph_matches_ele( OUT::ph_n, 0 );
    for( int idx = 0; idx < IN::el_n; idx++ ) {

        float elPt = IN::el_pt->at(idx);

        if( !config.PassFloat( "cut_el_pt", elPt) ) continue;

        if( !config.PassBool( "cut_el_loose", IN::el_passLoose->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_medium", IN::el_passMedium->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_tight", IN::el_passTight->at(idx)) ) continue;

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
    for( int idx = 0; idx < IN::ph_n; idx++ ) {
        ph_order.push_back(idx);
    }

    BOOST_FOREACH( int idx, ph_order )  {

        float phPt = IN::ph_pt->at(idx);
        float ph_sceta = fabs( IN::ph_sceta->at(idx) );

        if( !config.PassFloat( "cut_ph_pt", phPt) ) continue;
        if( !config.PassFloat( "cut_ph_abseta", ph_sceta) ) continue;
        if( !config.PassFloat( "cut_ph_abseta_crack", ph_sceta) ) continue;
        //if( !config.PassBool( "cut_ph_eleVeto", IN::ph_eleVeto->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_hasPixSeed", IN::ph_hasPixSeed->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_loose", IN::ph_passLoose->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_looseNoSIEIE", IN::ph_passLooseNoSIEIE->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_medium", IN::ph_passMedium->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_tight", IN::ph_passTight->at(idx)) ) continue;

        // electron overlap removal
        TLorentzVector phlv;
        phlv.SetPtEtaPhiE( IN::ph_pt->at(idx), 
                           IN::ph_eta->at(idx), 
                           IN::ph_phi->at(idx), 
                           IN::ph_e->at(idx) );

        float min_el_dr = 100.0;
        float min_trigel_dr = 100.0;
        //bool found_trigel = false;

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

        CopyPrefixIndexBranchesInToOut( "ph_", idx);
        OUT::ph_pt->pop_back();
        OUT::ph_pt->push_back(phPt);

        OUT::ph_n++;

    }
    #endif
}

void RunModule::FilterMuon( ModuleConfig & config ) const {

    #ifdef EXISTS_mu_n
    OUT::mu_n = 0;
    ClearOutputPrefix("mu_");

    for( int idx = 0; idx < IN::mu_n; idx++ ) {


        float muPt = IN::mu_pt->at(idx);

        if( !config.PassFloat( "cut_mu_pt", muPt) ) continue;
        if( !config.PassFloat( "cut_mu_eta", fabs(IN::mu_eta->at(idx) ) ) ) continue;
        //if( !config.PassFloat( "cut_mu_corriso", IN::mu_corrIso->at(idx)/IN::mu_pt->at(idx)) ) continue;
        if( !config.PassBool( "cut_mu_passTight", IN::mu_passTight->at(idx)) ) continue;
        //if( !config.PassBool( "cut_mu_passTightNoIso", IN::mu_passTightNoIso->at(idx)) ) continue;
        //if( !config.PassBool( "cut_mu_passTightNoD0", IN::mu_passTightNoD0->at(idx)) ) continue;
        //if( !config.PassBool( "cut_mu_passTightNoIsoNoD0", IN::mu_passTightNoIsoNoD0->at(idx)) ) continue;

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
    OUT::el_passtrig28_n              = 0;
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
    OUT::ph_mediumNoChIsoNoSIEIENoEleVeto_n  = 0;
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

    OUT::mt_lep_met                     = 0;
    OUT::dphi_met_lep1                     = 0;
    OUT::dphi_met_lep2                     = 0;
    OUT::m_leplep                     = 0;
    OUT::m_mumu                       = 0;
    OUT::m_elel                       = 0;
    OUT::m_3lep                       = 0;
    OUT::m_4lep                       = 0;
    OUT::pt_leplep                    = 0;

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
    OUT::ptSorted_ph_mediumNoChIsoNoSIEIENoEleVeto_idx->clear();
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

    //OUT::ph_trigMatch_el->clear();
    //OUT::ph_elMinDR     ->clear();
    OUT::EventWeight = 1.0;

    TLorentzVector metlv;
#ifdef EXISTS_METPt
    metlv.SetPxPyPzE( OUT::METPx->at(0), OUT::METPy->at(0), OUT::METPz->at(0), OUT::METE->at(0) );
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

        // diable trigger counting until trigger matching is implemented
        // // 2015-11-22

        //if( lv.Pt() > 25 ) {
        //    OUT::el_pt25_n++;
        //}
        //if( lv.Pt() > 28 && OUT::el_triggerMatch->at(idx) && OUT::el_passMvaTrig->at(idx) ) {
        //    OUT::el_passtrig28_n++;
        //}

        //if( lv.Pt() > 30 && OUT::el_triggerMatch->at(idx) && OUT::el_passMvaTrig->at(idx) ) {
        //    OUT::el_passtrig_n++;
        //    trigelectrons.push_back( lv );
        //   
        //}
        //if( lv.Pt() > 30 && OUT::el_triggerMatch->at(idx) && OUT::el_passLoose->at(idx) ) {
        //    OUT::el_passtrigL_n++;
        //}

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

        if( lv.Pt() > 25 ) {
            OUT::mu_pt25_n++;
        }
     //   if( lv.Pt() > 30 && fabs(lv.Eta()) < 2.1 && OUT::mu_triggerMatch->at(idx) ) {
     //       OUT::mu_passtrig_n++;
     //   }
     //   if( lv.Pt() > 25 && fabs(lv.Eta()) < 2.1 && OUT::mu_triggerMatch->at(idx) ) {
     //       OUT::mu_passtrig25_n++;
     //       trigmuons.push_back(lv);
     //   }
    }

    std::vector<TLorentzVector> photons;
    std::vector<std::pair<float, int> > sorted_photons;

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
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoNoSIEIENoEleVeto;
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
            //if( OUT::ph_eleVeto->at(idx)==0 ) {
            //    OUT::ph_mediumNoSIEIEPassCSEV_n++;
            //    sorted_photons_mediumNoSIEIEPassCSEV.push_back( sort_pair );
            //}
            //if( OUT::ph_eleVeto->at(idx)==1 ) {
            //    OUT::ph_mediumNoSIEIEFailCSEV_n++;
            //    sorted_photons_mediumNoSIEIEFailCSEV.push_back( sort_pair );
            //}
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
     //           if( OUT::ph_eleVeto->at(idx)==0 ) {
     //               OUT::ph_mediumPassCSEV_n++;
     //               sorted_photons_mediumPassCSEV.push_back( sort_pair );
     //           }
     //           if( OUT::ph_eleVeto->at(idx)==1 ) {
     //               OUT::ph_mediumFailCSEV_n++;
     //               sorted_photons_mediumFailCSEV.push_back( sort_pair );
     //           }
            }
        }
        if( OUT::ph_passHOverEMedium->at(idx)  && OUT::ph_passNeuIsoCorrMedium->at(idx) && OUT::ph_passPhoIsoCorrMedium->at(idx) ) {
            OUT::ph_mediumNoChIsoNoSIEIENoEleVeto_n++;
            sorted_photons_mediumNoChIsoNoSIEIENoEleVeto.push_back( sort_pair );

            if( OUT::ph_passSIEIEMedium->at(idx)  ) {

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
         //       if( OUT::ph_eleVeto->at(idx)==0 ) {
         //           OUT::ph_mediumNoChIsoPassCSEV_n++;
         //           sorted_photons_mediumNoChIsoPassCSEV.push_back( sort_pair );
         //       }
         //       if( OUT::ph_eleVeto->at(idx)==1 ) {
         //           OUT::ph_mediumNoChIsoFailCSEV_n++;
         //           sorted_photons_mediumNoChIsoFailCSEV.push_back( sort_pair );
         //       }
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
     //       if( OUT::ph_eleVeto->at(idx)==0 ) {
     //           OUT::ph_mediumNoNeuIsoPassCSEV_n++;
     //           sorted_photons_mediumNoNeuIsoPassCSEV.push_back( sort_pair );
     //       }
     //       if( OUT::ph_eleVeto->at(idx)==1 ) {
     //           OUT::ph_mediumNoNeuIsoFailCSEV_n++;
     //           sorted_photons_mediumNoNeuIsoFailCSEV.push_back( sort_pair );
     //       }
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
     //       if( OUT::ph_eleVeto->at(idx)==0 ) {
     //           OUT::ph_mediumNoPhoIsoPassCSEV_n++;
     //           sorted_photons_mediumNoPhoIsoPassCSEV.push_back( sort_pair );
     //       }
     //       if( OUT::ph_eleVeto->at(idx)==1 ) {
     //           OUT::ph_mediumNoPhoIsoFailCSEV_n++;
     //           sorted_photons_mediumNoPhoIsoFailCSEV.push_back( sort_pair );
     //       }
        }
        
        //bool match_eltrig = false;
        //for( int elidx = 0; elidx < IN::el_n; elidx++ ) {

        //    // use IN electrons so that 
        //    TLorentzVector ellv;
        //    ellv.SetPtEtaPhiE(  IN::el_pt->at(elidx),
        //                      IN::el_eta->at(elidx),
        //                      IN::el_phi->at(elidx),
        //                      IN::el_e->at(elidx)
        //                    );
        //    if( ellv.DeltaR( phot ) < 0.2 && IN::el_triggerMatch->at(elidx) ) {
        //        match_eltrig=true;
        //    }
        //}
        //OUT::ph_trigMatch_el->push_back(match_eltrig);

        //// electron overlap removal
        //// use OUT because we want to remove
        //// overlap with fully identified electrons
        //float min_dr = 100.0;
        //for( int eidx = 0; eidx < OUT::el_n; eidx++ ) {
        //    TLorentzVector ellv;
        //    ellv.SetPtEtaPhiE( OUT::el_pt->at(eidx), 
        //                       OUT::el_eta->at(eidx), 
        //                       OUT::el_phi->at(eidx), 
        //                       OUT::el_e->at(eidx) );

        //    float dr = phot.DeltaR( ellv );
        //    if( dr < min_dr ) {
        //        min_dr = dr;
        //    }
        //}
        //OUT::ph_elMinDR->push_back( min_dr );
    }

    std::map<std::string, float> results;
    std::map<std::string, std::vector<float> > vector_results;
    Phot::CalcEventVars( photons, electrons, muons, metlv, results, vector_results );

    CopyMapVarsToOut( results );
    CopyVectorMapVarsToOut( vector_results );

    // sort the list of photon momenta in descending order
    std::sort(sorted_photons.rbegin(), sorted_photons.rend());
    std::sort(sorted_leptons.rbegin(), sorted_leptons.rend());

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
    std::sort(sorted_photons_mediumNoChIsoNoSIEIENoEleVeto.rbegin()  , sorted_photons_mediumNoChIsoNoSIEIENoEleVeto.rend());
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
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoNoSIEIENoEleVeto.begin() ; itr != sorted_photons_mediumNoChIsoNoSIEIENoEleVeto.end(); ++itr ) {
        OUT::ptSorted_ph_mediumNoChIsoNoSIEIENoEleVeto_idx->push_back( itr->second );
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

     //   if( OUT::mu_triggerMatch->at(i) ) {
     //       nLepTrigMatchSoft++;
     //       if( OUT::mu_pt->at(i) > 25 ) {
     //           nLepTrigMatch++;
     //       }
     //   }
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

        //if( OUT::el_triggerMatch->at(i) && OUT::el_passMvaTrig->at(i) ) {
        //    nLepTrigMatchSoft++;
        //    if( OUT::el_pt->at(i) > 30 ) {
        //        nLepTrigMatch++;
        //        nElTrigMatch++;
        //    }
        //}
    }

    for( int i = 0; i < OUT::ph_n; ++i ) {
        nElPh++;
        TLorentzVector tlv;
        tlv.SetPtEtaPhiM( OUT::ph_pt->at(i), 
                          OUT::ph_eta->at(i), 
                          OUT::ph_phi->at(i), 
                          0.0);

        photons.push_back(tlv);
     //   if( OUT::ph_truthMatch_el->at(i) ) {
     //       nPhTruthMatchEl++;
     //   }
     //   if( OUT::ph_passSIEIEMedium->at(i) && OUT::ph_eleVeto->at(i)== 0 ) {
     //       nPhPassSIEIEAndEVeto++;
     //   }
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

    if( !config.PassBool( "cut_SingleLepTrig", (OUT::passTrig_TkMu24_eta2p1 || OUT::passTrig_IsoTkMu24_eta2p1 || OUT::passTrig_IsoMu24_eta2p1 || OUT::passTrig_Ele27_WPLoose_eta2p1 ) ) ) keep_event = false;
    if( !config.PassBool( "cut_DiLepTrig", (OUT::passTrig_Ele17_Ele12_DZ || OUT::passTrig_Mu17_Mu8_DZ || OUT::passTrig_Mu17_TkMu8_DZ ) ) ) keep_event = false;
    if( !config.PassBool( "cut_DiMuTrig", (OUT::passTrig_Mu17_Mu8_DZ || OUT::passTrig_Mu17_TkMu8_DZ ) ) ) keep_event = false;
    if( !config.PassBool( "cut_DiElTrig", (OUT::passTrig_Ele17_Ele12_DZ) ) ) keep_event = false;

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

    //if( !config.PassFloat( "cut_m_lepph1", OUT::m_lepph1 ) ) keep_event = false;
    //if( !config.PassFloat( "cut_m_lepph2", OUT::m_lepph2 ) ) keep_event = false;
    //if( !config.PassFloat( "cut_m_lep2ph1", OUT::m_lep2ph1 ) ) keep_event = false;
    //if( !config.PassFloat( "cut_m_lep2ph2", OUT::m_lep2ph2 ) ) keep_event = false;


    #endif //el_n
    #endif //mu_n
    #endif //ph_n
    return keep_event;
}

bool RunModule::FilterBlind( ModuleConfig & config ) const {

    bool keep_event = true;

    bool pass_blind = true;

    int n_medPhot_pt50 = 0;
    for( int idx = 0; idx < OUT::ph_n ; ++idx ) {
        if( OUT::ph_passMedium->at(idx) && OUT::ph_pt->at(idx) > 50 ) {
            n_medPhot_pt50++;
        }
    }
    if( !config.PassInt( "cut_nPhPassMediumPt50", n_medPhot_pt50 ) ) pass_blind=false;

    if( !pass_blind ) {
        OUT::isBlinded=true;
        if( IN::EvtIsRealData ) keep_event=false;
    }
    else {
        OUT::isBlinded=false;
    }
    
    return keep_event;

}

void RunModule::FilterJet( ModuleConfig & config ) const {

    //#ifdef EXISTS_jet_n

    //OUT::jet_n = 0;
    //ClearOutputPrefix( "jet_" );

    //for( int idx = 0; idx < IN::jet_n; idx++ ) {

    //    bool keep_jet = true;

    //    if( !config.PassInt( "cut_jet_n_constituents", IN::jet_Nconstitutents->at(idx) ) )keep_jet =false;
    //    if( !config.PassInt( "cut_jet_nch", IN::jet_NCH->at(idx) ) )   keep_jet = false;
    //    if( !config.PassFloat( "cut_jet_nhf", IN::jet_NHF->at(idx) ) ) keep_jet = false;
    //    if( !config.PassFloat( "cut_jet_nef", IN::jet_NEF->at(idx) ) ) keep_jet = false;
    //    if( !config.PassFloat( "cut_jet_chf", IN::jet_CHF->at(idx) ) ) keep_jet = false;
    //    if( !config.PassFloat( "cut_jet_cef", IN::jet_CEF->at(idx) ) ) keep_jet = false;

    //    // don't continue if the jet should be rejected
    //    if( !keep_jet ) continue;

    //    TLorentzVector jetlv;
    //    jetlv.SetPtEtaPhiE( IN::jet_pt->at(idx), 
    //                        IN::jet_eta->at(idx),
    //                        IN::jet_phi->at(idx),
    //                        IN::jet_e->at(idx)
    //                       );

    //    for( int eidx = 0; eidx < OUT::el_n; eidx++ ) {
    //        TLorentzVector ellv;
    //        ellv.SetPtEtaPhiE( OUT::el_pt->at(eidx), 
    //                           OUT::el_eta->at(eidx),
    //                           OUT::el_phi->at(eidx),
    //                           OUT::el_e->at(eidx)
    //                          );

    //        //delta R 
    //        float dr = ellv.DeltaR( jetlv );
    //        if( !config.PassFloat( "cut_jet_ele_dr", dr ) ) keep_jet = false;
    //    }

    //    // don't continue if the jet should be rejected
    //    if( !keep_jet ) continue;

    //    for( int pidx = 0; pidx < OUT::ph_n; pidx++ ) {

    //        TLorentzVector phlv;
    //        phlv.SetPtEtaPhiE( OUT::ph_pt->at(pidx), 
    //                           OUT::ph_eta->at(pidx),
    //                           OUT::ph_phi->at(pidx),
    //                           OUT::ph_e->at(pidx)
    //                          );

    //        //delta R 
    //        float dr = phlv.DeltaR( jetlv );
    //        if( !config.PassFloat( "cut_jet_ph_dr", dr ) ) keep_jet = false;
    //    }

    //    // don't continue if the jet should be rejected
    //    if( !keep_jet ) continue;

    //    for( int midx = 0; midx < OUT::mu_n; midx++ ) {
    //        TLorentzVector mulv;
    //        mulv.SetPtEtaPhiE( OUT::mu_pt->at(midx), 
    //                           OUT::mu_eta->at(midx),
    //                           OUT::mu_phi->at(midx),
    //                           OUT::mu_e->at(midx)
    //                          );

    //        //delta R 
    //        float dr = mulv.DeltaR( jetlv );
    //        if( !config.PassFloat( "cut_jet_mu_dr", dr ) ) keep_jet = false;
    //    }

    //    if( !keep_jet ) continue;

    //    OUT::jet_n++;
    //    CopyPrefixIndexBranchesInToOut( "jet_", idx, true );

    //}
    //#endif
}
