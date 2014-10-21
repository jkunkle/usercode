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

    // *************************
    // Declare Branches
    // *************************
    outtree->Branch("isBlinded", &OUT::isBlinded );
    outtree->Branch("EventWeight", &OUT::EventWeight, "EventWeight/F" );

    outtree->Branch("mu_pt25_n"                   , &OUT::mu_pt25_n                   , "mu_pt25_n/I"        );
    outtree->Branch("mu_passtrig_n"               , &OUT::mu_passtrig_n               , "mu_passtrig_n/I"        );
    outtree->Branch("mu_passtrig25_n"             , &OUT::mu_passtrig25_n             , "mu_passtrig25_n/I"        );
    outtree->Branch("el_pt25_n"                   , &OUT::el_pt25_n                   , "el_pt25_n/I"        );
    outtree->Branch("el_passtrig_n"               , &OUT::el_passtrig_n               , "el_passtrig_n/I"        );
    outtree->Branch("el_passtrig28_n"             , &OUT::el_passtrig28_n             , "el_passtrig28_n/I"        );
    outtree->Branch("ph_mediumNoSIEIE_n"          , &OUT::ph_mediumNoSIEIE_n          , "ph_mediumNoSIEIE_n/I" );
    outtree->Branch("ph_medium_n"                 , &OUT::ph_medium_n                 , "ph_medium_n/I" );
    outtree->Branch("ph_mediumNoEleVeto_n"        , &OUT::ph_mediumNoEleVeto_n        , "ph_mediumNoEleVeto_n/I" );
    outtree->Branch("ph_mediumNoSIEIENoEleVeto_n" , &OUT::ph_mediumNoSIEIENoEleVeto_n , "ph_mediumNoSIEIENoEleVeto_n/I" );
    outtree->Branch("ph_mediumNoIso_n"            , &OUT::ph_mediumNoIso_n            , "ph_mediumNoIso_n/I" );
    outtree->Branch("ph_mediumNoChIso_n"          , &OUT::ph_mediumNoChIso_n          , "ph_mediumNoChIso_n/I" );
    outtree->Branch("ph_mediumNoNeuIso_n"         , &OUT::ph_mediumNoNeuIso_n         , "ph_mediumNoNeuIso_n/I" );
    outtree->Branch("ph_mediumNoPhoIso_n"         , &OUT::ph_mediumNoPhoIso_n         , "ph_mediumNoPhoIso_n/I" );
    outtree->Branch("ph_mediumNoChIsoNoNeuIso_n"  , &OUT::ph_mediumNoChIsoNoNeuIso_n  , "ph_mediumNoChIsoNoNeuIso_n/I" );
    outtree->Branch("ph_mediumNoChIsoNoPhoIso_n"  , &OUT::ph_mediumNoChIsoNoPhoIso_n  , "ph_mediumNoChIsoNoPhoIso_n/I" );
    outtree->Branch("ph_mediumNoNeuIsoNoPhoIso_n" , &OUT::ph_mediumNoNeuIsoNoPhoIso_n , "ph_mediumNoNeuIsoNoPhoIso_n/I" );
    outtree->Branch("ph_iso533_n"                 , &OUT::ph_iso533_n                 , "ph_iso533_n/I" );
    outtree->Branch("ph_iso855_n"                 , &OUT::ph_iso855_n                 , "ph_iso855_n/I" );
    outtree->Branch("ph_iso1077_n"                , &OUT::ph_iso1077_n                , "ph_iso1077_n/I" );
    outtree->Branch("ph_iso1299_n"                , &OUT::ph_iso1299_n                , "ph_iso1299_n/I" );
    outtree->Branch("ph_iso151111_n"              , &OUT::ph_iso151111_n              , "ph_iso151111_n/I" );
    outtree->Branch("ph_iso201616_n"              , &OUT::ph_iso201616_n              , "ph_iso201616_n/I" );
    outtree->Branch("ph_trigMatch_el"             , &OUT::ph_trigMatch_el             );
    outtree->Branch("ph_elMinDR"                  , &OUT::ph_elMinDR                  );
    
    outtree->Branch("leadPhot_pt"         , &OUT::leadPhot_pt         , "leadPhot_pt/F"       );
    outtree->Branch("sublPhot_pt"         , &OUT::sublPhot_pt        , "sublPhot_pt/F"        );
    outtree->Branch("leadPhot_lepDR"      , &OUT::leadPhot_lepDR     , "leadPhot_lepDR/F"     );
    outtree->Branch("sublPhot_lepDR"      , &OUT::sublPhot_lepDR     , "sublPhot_lepDR/F"     );
    outtree->Branch("ph_phDR"             , &OUT::ph_phDR            , "ph_phDR/F"            );
    outtree->Branch("phPhot_lepDR"        , &OUT::phPhot_lepDR       , "phPhot_lepDR/F"       );
    outtree->Branch("leadPhot_lepDPhi"    , &OUT::leadPhot_lepDPhi   , "leadPhot_lepDPhi/F"   );
    outtree->Branch("sublPhot_lepDPhi"    , &OUT::sublPhot_lepDPhi   , "sublPhot_lepDPhi/F"   );
    outtree->Branch("ph_phDPhi"           , &OUT::ph_phDPhi          , "ph_phDPhi/F"          );
    outtree->Branch("phPhot_lepDPhi"      , &OUT::phPhot_lepDPhi     , "phPhot_lepDPhi/F"     );
    outtree->Branch("dphi_met_lep1"       , &OUT::dphi_met_lep1      , "dphi_met_lep1/F"      );
    outtree->Branch("dphi_met_lep2"       , &OUT::dphi_met_lep2      , "dphi_met_lep2/F"      );
    outtree->Branch("dphi_met_ph1"        , &OUT::dphi_met_ph1       , "dphi_met_ph1/F"       );
    outtree->Branch("dphi_met_ph2"        , &OUT::dphi_met_ph2       , "dphi_met_ph2/F"       );
    outtree->Branch("mt_lep_met"          , &OUT::mt_lep_met         , "mt_lep_met/F"         );
    outtree->Branch("mt_lepph1_met"       , &OUT::mt_lepph1_met      , "mt_lepph1_met/F"      );
    outtree->Branch("mt_lepph2_met"       , &OUT::mt_lepph2_met      , "mt_lepph2_met/F"      );
    outtree->Branch("mt_lepphph_met"      , &OUT::mt_lepphph_met     , "mt_lepphph_met/F"     );
    outtree->Branch("m_leplep"            , &OUT::m_leplep           , "m_leplep/F"           );
    outtree->Branch("m_leplep_uncorr"     , &OUT::m_leplep_uncorr    , "m_leplep_uncorr/F"    );
    outtree->Branch("m_lepph1"            , &OUT::m_lepph1           , "m_lepph1/F"           );
    outtree->Branch("m_lepph2"            , &OUT::m_lepph2           , "m_lepph2/F"           );
    outtree->Branch("m_leplepph"          , &OUT::m_leplepph         , "m_leplepph/F"         );
    outtree->Branch("m_lepphph"           , &OUT::m_lepphph          , "m_lepphph/F"          );
    outtree->Branch("m_leplepZ"           , &OUT::m_leplepZ          , "m_leplepZ/F"          );
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
    outtree->Branch("dr_ph1_leadLep"      , &OUT::dr_ph1_leadLep     , "dr_ph1_leadLep/F"     );
    outtree->Branch("dr_ph1_sublLep"      , &OUT::dr_ph1_sublLep     , "dr_ph1_sublLep/F"     );
    outtree->Branch("dr_ph2_leadLep"      , &OUT::dr_ph2_leadLep     , "dr_ph2_leadLep/F"     );
    outtree->Branch("dr_ph2_sublLep"      , &OUT::dr_ph2_sublLep     , "dr_ph2_sublLep/F"     );
    outtree->Branch("m_ph1_ph2"           , &OUT::m_ph1_ph2          , "m_ph1_ph2/F"          );
    outtree->Branch("dr_ph1_ph2"          , &OUT::dr_ph1_ph2         , "dr_ph1_ph2/F"         );
    outtree->Branch("dphi_ph1_ph2"        , &OUT::dphi_ph1_ph2       , "dphi_ph1_ph2/F"       );
    outtree->Branch("pt_ph1_ph2"          , &OUT::pt_ph1_ph2         , "pt_ph1_ph2/F"         );
    outtree->Branch("m_leadLep_ph1_ph2"   , &OUT::m_leadLep_ph1_ph2  , "m_leadLep_ph1_ph2/F"  );
    outtree->Branch("m_leadLep_ph1"       , &OUT::m_leadLep_ph1      , "m_leadLep_ph1/F"      );
    outtree->Branch("m_leadLep_ph2"       , &OUT::m_leadLep_ph2      , "m_leadLep_ph2/F"      );
    outtree->Branch("pt_leadph12"         , &OUT::pt_leadph12        , "pt_leadph12/F"        );
    outtree->Branch("pt_sublph12"         , &OUT::pt_sublph12        , "pt_sublph12/F"        );
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

    outtree->Branch("m_nearestToZ"   , &OUT::m_nearestToZ   , "m_nearestToZ/F"     );
    outtree->Branch("m_minZdifflepph", &OUT::m_minZdifflepph, "m_minZdifflepph/F"     );

    outtree->Branch("truelep_n", &OUT::truelep_n, "truelep_n/I" );
    outtree->Branch("trueph_n", &OUT::trueph_n, "tureph_n/I"  );
    outtree->Branch("trueph_wmother_n", &OUT::trueph_wmother_n, "trueph_wmother_n/I"  );
    outtree->Branch("truegenph_n", &OUT::truegenph_n, "truegenph_n/I"  );
    outtree->Branch("truegenphpt15_n", &OUT::truegenphpt15_n, "truegenphpt15_n/I"  );

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
    outtree->Branch("trueleadlep_leadPhotDR"   , &OUT::trueleadlep_leadPhotDR, "trueleadlep_leadPhotDR/F"     );
    outtree->Branch("trueleadlep_sublPhotDR"   , &OUT::trueleadlep_sublPhotDR, "trueleadlep_sublPhotDR/F"     );
    outtree->Branch("truesubllep_leadPhotDR"   , &OUT::truesubllep_leadPhotDR, "truesubllep_leadPhotDR/F"     );
    outtree->Branch("truesubllep_sublPhotDR"   , &OUT::truesubllep_sublPhotDR, "truesubllep_sublPhotDR/F"     );

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

        if( mod_conf.GetName() == "FilterPhoton" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "sort_by_id" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string data = eitr->second;
                std::transform(data.begin(), data.end(), data.begin(), ::tolower);
                if( data=="true") sort_photons_by_id=true;
                else              sort_photons_by_id=false;
            }
        }
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

    for( int idx = 0; idx < IN::el_n; idx++ ) {

        if( !config.PassFloat( "cut_el_pt", IN::el_pt->at(idx)) ) continue;

        if( !config.PassBool( "cut_el_loose", IN::el_passLoose->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_medium", IN::el_passMedium->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_tight", IN::el_passTight->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_tightTrig", IN::el_passTightTrig->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_mvaTrig", IN::el_passMvaTrig->at(idx)) ) continue;
        if( !config.PassBool( "cut_el_mvaNonTrig", IN::el_passMvaNonTrig->at(idx)) ) continue;

        // Remove electrons that overlap with muons
        float mindr = 100.;
        TLorentzVector el;
        el.SetPtEtaPhiE( IN::el_pt->at(idx), IN::el_eta->at(idx), IN::el_phi->at(idx), IN::el_e->at(idx ) );
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
        OUT::el_n++;

    }
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

        if( !config.PassFloat( "cut_ph_pt", IN::ph_pt->at(idx)) ) continue;
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
        float min_dr = 100.0;
        for( int eidx = 0; eidx < OUT::el_n; eidx++ ) {
            TLorentzVector ellv;
            ellv.SetPtEtaPhiE( OUT::el_pt->at(eidx), 
                               OUT::el_eta->at(eidx), 
                               OUT::el_phi->at(eidx), 
                               OUT::el_e->at(eidx) );

            float dr = phlv.DeltaR( ellv );
            if( dr < min_dr ) {
                min_dr = dr;
            }
        }

        if( !config.PassFloat( "cut_el_ph_dr", min_dr ) ) continue;

        CopyPrefixIndexBranchesInToOut( "ph_", idx );
        
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

        if( !config.PassFloat( "cut_mu_pt", IN::mu_pt->at(idx)) ) continue;

        CopyPrefixIndexBranchesInToOut( "mu_", idx );
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

    OUT::trueleadlep_leadPhotDR    = 0;
    OUT::trueleadlep_sublPhotDR    = 0;
    OUT::truesubllep_leadPhotDR    = 0;
    OUT::truesubllep_sublPhotDR    = 0;

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
    std::vector< TLorentzVector > leptons;
    std::vector< TLorentzVector > photons;
    int lepidx = 0;
    int phidx = 0;
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
            if( abs(IN::mcMomPID->at(idx)) < 25  ) OUT::truegenph_n++;
            if( abs(IN::mcMomPID->at(idx)) < 25 && IN::mcPt->at(idx)>15 ) OUT::truegenphpt15_n++;

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

                float dr = qrklv.DeltaR( phlv );
                if( dr < qrkminDR ) {
                    qrkminDR = dr;
                }
            }

            OUT::trueph_nearestQrkDR-> push_back( qrkminDR );




            OUT::trueph_n++;
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

    // calculate event variables
    if( leptons.size() > 0 ) {
        OUT::trueleadlep_pt = sorted_leptons[0].first;

        if( photons.size() > 0 ) {
            OUT::trueleadlep_leadPhotDR = leptons[sorted_leptons[0].second].DeltaR(photons[sorted_photons[0].second]);
        }
        if( photons.size() > 1 ) {
            OUT::trueleadlep_sublPhotDR = leptons[sorted_leptons[0].second].DeltaR(photons[sorted_photons[1].second]);
        }
        if( leptons.size() > 1 ) {
            OUT::truesubllep_pt = sorted_leptons[1].first;
            if( photons.size() > 0 ) {
                OUT::truesubllep_leadPhotDR = leptons[sorted_leptons[1].second].DeltaR(photons[sorted_photons[0].second]);
            }
            if( photons.size() > 1 ) {
                OUT::truesubllep_sublPhotDR = leptons[sorted_leptons[1].second].DeltaR(photons[sorted_photons[1].second]);
            }
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

    OUT::mu_pt25_n                   = 0;
    OUT::mu_passtrig_n               = 0;
    OUT::mu_passtrig25_n             = 0;
    OUT::el_pt25_n                   = 0;
    OUT::el_passtrig_n               = 0;
    OUT::el_passtrig28_n             = 0;
    OUT::ph_mediumNoSIEIE_n          = 0;
    OUT::ph_medium_n                 = 0;
    OUT::ph_mediumNoEleVeto_n        = 0;
    OUT::ph_mediumNoSIEIENoEleVeto_n = 0;
    OUT::ph_mediumNoIso_n            = 0;
    OUT::ph_mediumNoChIso_n          = 0;
    OUT::ph_mediumNoNeuIso_n         = 0;
    OUT::ph_mediumNoPhoIso_n         = 0;
    OUT::ph_mediumNoChIsoNoNeuIso_n  = 0;
    OUT::ph_mediumNoChIsoNoPhoIso_n  = 0;
    OUT::ph_mediumNoNeuIsoNoPhoIso_n = 0;
    OUT::ph_iso533_n                 = 0;
    OUT::ph_iso855_n                 = 0;
    OUT::ph_iso1077_n                = 0;
    OUT::ph_iso1299_n                = 0;
    OUT::ph_iso151111_n              = 0;
    OUT::ph_iso201616_n              = 0;
    OUT::ph_trigMatch_el->clear();
    OUT::ph_elMinDR     ->clear();
    OUT::leadPhot_pt                 = 0;
    OUT::sublPhot_pt                 = 0;
    OUT::leadPhot_lepDR              = 0;
    OUT::sublPhot_lepDR              = 0;
    OUT::ph_phDR                     = 0;
    OUT::phPhot_lepDR                = 0;
    OUT::leadPhot_lepDPhi            = 0;
    OUT::sublPhot_lepDPhi            = 0;
    OUT::ph_phDPhi                   = 0;
    OUT::phPhot_lepDPhi              = 0;
    OUT::dphi_met_lep1               = 0;
    OUT::dphi_met_lep2               = 0;
    OUT::dphi_met_ph1                = 0;
    OUT::dphi_met_ph2                = 0;
    OUT::mt_lep_met                  = 0;
    OUT::mt_lepph1_met               = 0;
    OUT::mt_lepph2_met               = 0;
    OUT::mt_lepphph_met              = 0;
    OUT::m_leplep                    = 0;
    OUT::m_leplep_uncorr             = 0;
    OUT::m_lepph1                    = 0;
    OUT::m_lepph2                    = 0;
    OUT::m_lepphph                   = 0;
    OUT::m_leplepph                  = 0;
    OUT::m_leplepZ                   = 0;
    OUT::m_3lep                      = 0;
    OUT::m_4lep                      = 0;
    OUT::pt_leplep                   = 0;
    OUT::pt_lepph1                   = 0;
    OUT::pt_lepph2                   = 0;
    OUT::pt_lepphph                  = 0;
    OUT::pt_leplepph                 = 0;
    OUT::pt_secondLepton             = 0;
    OUT::pt_thirdLepton              = 0;
    OUT::m_nearestToZ                = 0;
    OUT::m_minZdifflepph             = 0;

    OUT::EventWeight = 1.0;

    TLorentzVector metlv;
#ifdef EXISTS_pfMET
    metlv.SetPtEtaPhiM( OUT::pfMET, 0.0, OUT::pfMETPhi, 0.0 );
#endif

    #ifdef EXISTS_el_n
    #ifdef EXISTS_mu_n
    #ifdef EXISTS_ph_n
    std::vector<TLorentzVector> leptons;
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
        }

    }

    for( int idx = 0; idx < OUT::mu_n; idx++ ) {

        TLorentzVector lv;
        lv.SetPtEtaPhiE(  OUT::mu_pt->at(idx),
                          OUT::mu_eta->at(idx),
                          OUT::mu_phi->at(idx),
                          OUT::mu_e->at(idx)
                        );
        leptons.push_back(lv);
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
        if( lv.Pt() > 30 && OUT::mu_triggerMatch->at(idx) ) {
            OUT::mu_passtrig_n++;
        }
        if( lv.Pt() > 25 && OUT::mu_triggerMatch->at(idx) ) {
            OUT::mu_passtrig25_n++;
        }
    }

    std::vector<TLorentzVector> photons;
    std::vector<std::pair<float, int> > sorted_photons;
    for( int idx = 0; idx < OUT::ph_n; ++idx ) {
        TLorentzVector phot;
        phot.SetPtEtaPhiE(  OUT::ph_pt->at(idx), 
                            OUT::ph_eta->at(idx),
                            OUT::ph_phi->at(idx),
                            OUT::ph_e->at(idx)
                        );
        photons.push_back(phot);
        sorted_photons.push_back(std::make_pair( phot.Pt(), idx ));

        if( OUT::ph_HoverE12->at(idx) < 0.05 ) {

            if( OUT::ph_chIsoCorr->at(idx) < 5   && 
                OUT::ph_neuIsoCorr->at(idx) < 3  && 
                OUT::ph_phoIsoCorr->at(idx) < 3 ) {
                OUT::ph_iso533_n++;
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 8  && 
                OUT::ph_neuIsoCorr->at(idx) < 5 && 
                OUT::ph_phoIsoCorr->at(idx) < 5 ) {
                OUT::ph_iso855_n++;
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 10 && 
                OUT::ph_neuIsoCorr->at(idx) < 7  && 
                OUT::ph_phoIsoCorr->at(idx) < 7 ) {
                OUT::ph_iso1077_n++;
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 12 && 
                OUT::ph_neuIsoCorr->at(idx) < 9  && 
                OUT::ph_phoIsoCorr->at(idx) < 9 ) {
                OUT::ph_iso1299_n++;
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 15 && 
                OUT::ph_neuIsoCorr->at(idx) < 11 && 
                OUT::ph_phoIsoCorr->at(idx) < 11 ) {
                OUT::ph_iso151111_n++;
            }
            
            if( OUT::ph_chIsoCorr->at(idx) < 20 && 
                OUT::ph_neuIsoCorr->at(idx) < 16 && 
                OUT::ph_phoIsoCorr->at(idx) < 16 ) {
                OUT::ph_iso201616_n++;
            }
        }
        if( OUT::ph_passSIEIEMedium->at(idx) && OUT::ph_hasPixSeed->at(idx) == 0 && OUT::ph_HoverE12->at(idx) < 0.05 ) { // replace with ph_passHOverEMedium 
            if( OUT::ph_passChIsoCorrMedium->at(idx) ) {
                  OUT::ph_mediumNoNeuIsoNoPhoIso_n++;
            }
            if( OUT::ph_passNeuIsoCorrMedium->at(idx) ) {
                  OUT::ph_mediumNoChIsoNoPhoIso_n++;
            }
            if( OUT::ph_passPhoIsoCorrMedium->at(idx) ) {
                  OUT::ph_mediumNoChIsoNoNeuIso_n++;
            }
            if( OUT::ph_passChIsoCorrMedium->at(idx)  && OUT::ph_passNeuIsoCorrMedium->at(idx) ) {
                OUT::ph_mediumNoPhoIso_n++;
            }
            if( OUT::ph_passPhoIsoCorrMedium->at(idx)  && OUT::ph_passNeuIsoCorrMedium->at(idx) ) {
                OUT::ph_mediumNoChIso_n++;
            }
            if( OUT::ph_passChIsoCorrMedium->at(idx)  && OUT::ph_passPhoIsoCorrMedium->at(idx) ) {
                OUT::ph_mediumNoNeuIso_n++;
            }
        }
        if( OUT::ph_HoverE12->at(idx) < 0.05 && OUT::ph_passChIsoCorrMedium->at(idx)  && OUT::ph_passNeuIsoCorrMedium->at(idx) && OUT::ph_passPhoIsoCorrMedium->at(idx) ) { // replace with ph_passHOverEMedium 
            OUT::ph_mediumNoSIEIENoEleVeto_n++;

            if( OUT::ph_hasPixSeed->at(idx)==0 ) {
                OUT::ph_mediumNoSIEIE_n++;
            }
            if( OUT::ph_passSIEIEMedium->at(idx) ) {
                OUT::ph_mediumNoEleVeto_n++;
            }
            if( OUT::ph_passSIEIEMedium->at(idx) && OUT::ph_hasPixSeed->at(idx)==0 ) {
                OUT::ph_medium_n++;
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


    // sort the list of photon momenta in descending order
    std::sort(sorted_photons.rbegin(), sorted_photons.rend());
    std::sort(sorted_leptons.rbegin(), sorted_leptons.rend());

    // fill variables for pT sorted photons
    if( sorted_photons.size() > 0 ) { 
        if( sorted_leptons.size() > 0 ) {
            OUT::leadPhot_leadLepDR = photons[sorted_photons[0].second].DeltaR(leptons[sorted_leptons[0].second.second]);
            if( sorted_leptons.size() > 1 ) {
                OUT::leadPhot_sublLepDR = photons[sorted_photons[0].second].DeltaR(leptons[sorted_leptons[1].second.second]);
            }
        }
        if( sorted_photons.size() > 1 ) {
            OUT::ph_phDR    = photons[sorted_photons[0].second].DeltaR(photons[sorted_photons[1].second]);
            OUT::ph_phDPhi    = photons[sorted_photons[0].second].DeltaPhi(photons[sorted_photons[1].second]);
            if( sorted_leptons.size() > 0 ) {
                OUT::sublPhot_leadLepDR = photons[sorted_photons[1].second].DeltaR(leptons[sorted_leptons[0].second.second]);
                if( sorted_leptons.size() > 1 ) {
                    OUT::sublPhot_sublLepDR = photons[sorted_photons[1].second].DeltaR(leptons[sorted_leptons[1].second.second]);
                    OUT::sublPhot_sublLepDR = photons[sorted_photons[1].second].DeltaR(leptons[sorted_leptons[1].second.second]);
                }
            }
        }
    }
    // fill variables for default sorted photons
    if( photons.size() > 0 ) { 
        if( sorted_leptons.size() > 0 ) {
            OUT::dr_ph1_leadLep = photons[0].DeltaR(leptons[sorted_leptons[0].second.second]);
            OUT::m_leadLep_ph1 = ( photons[0] + leptons[sorted_leptons[0].second.second] ).M();
            if( sorted_leptons.size() > 1 ) {
                OUT::dr_ph1_sublLep = photons[0].DeltaR(leptons[sorted_leptons[1].second.second]);
            }
        }
        if( photons.size() > 1 ) {

            OUT::dr_ph1_ph2 = photons[0].DeltaR(photons[1]);
            OUT::dphi_ph1_ph2 = photons[0].DeltaPhi(photons[1]);
            OUT::m_ph1_ph2 = (photons[0] + photons[1]).M();
            OUT::pt_ph1_ph2 = (photons[0] + photons[1]).Pt();
            if( photons[0].Pt() > photons[1].Pt() ) {
                OUT::pt_leadph12 = photons[0].Pt();
                OUT::pt_sublph12 = photons[1].Pt();
                OUT::sieie_leadph12 = OUT::ph_sigmaIEIE->at(0);
                OUT::sieie_sublph12 = OUT::ph_sigmaIEIE->at(1);
                OUT::chIsoCorr_leadph12 = OUT::ph_chIsoCorr->at(0);
                OUT::chIsoCorr_sublph12 = OUT::ph_chIsoCorr->at(1);
                OUT::neuIsoCorr_leadph12 = OUT::ph_neuIsoCorr->at(0);
                OUT::neuIsoCorr_sublph12 = OUT::ph_neuIsoCorr->at(1);
                OUT::phoIsoCorr_leadph12 = OUT::ph_phoIsoCorr->at(0);
                OUT::phoIsoCorr_sublph12 = OUT::ph_phoIsoCorr->at(1);
                OUT::isEB_leadph12 = OUT::ph_IsEB->at(0);
                OUT::isEB_sublph12 = OUT::ph_IsEB->at(1);
                OUT::isEE_leadph12 = OUT::ph_IsEE->at(0);
                OUT::isEE_sublph12 = OUT::ph_IsEE->at(1);
            }
            else {
                OUT::pt_leadph12 = photons[1].Pt();
                OUT::pt_sublph12 = photons[0].Pt();
                OUT::sieie_leadph12 = OUT::ph_sigmaIEIE->at(1);
                OUT::sieie_sublph12 = OUT::ph_sigmaIEIE->at(0);
                OUT::chIsoCorr_leadph12 = OUT::ph_chIsoCorr->at(1);
                OUT::chIsoCorr_sublph12 = OUT::ph_chIsoCorr->at(0);
                OUT::neuIsoCorr_leadph12 = OUT::ph_neuIsoCorr->at(1);
                OUT::neuIsoCorr_sublph12 = OUT::ph_neuIsoCorr->at(0);
                OUT::phoIsoCorr_leadph12 = OUT::ph_phoIsoCorr->at(1);
                OUT::phoIsoCorr_sublph12 = OUT::ph_phoIsoCorr->at(0);
                OUT::isEB_leadph12 = OUT::ph_IsEB->at(1);
                OUT::isEB_sublph12 = OUT::ph_IsEB->at(0);
                OUT::isEE_leadph12 = OUT::ph_IsEE->at(1);
                OUT::isEE_sublph12 = OUT::ph_IsEE->at(0);
            }

            if( sorted_leptons.size() > 0 ) {
                OUT::dr_ph1_leadLep = photons[0].DeltaR( leptons[sorted_leptons[0].second.second]);
                OUT::m_leadLep_ph1_ph2 = ( photons[0] + photons[1] + leptons[sorted_leptons[0].second.second] ).M();
                OUT::m_leadLep_ph2 = ( photons[1] + leptons[sorted_leptons[0].second.second] ).M();

                if( sorted_leptons.size() > 1 ) {
                    OUT::dr_ph2_sublLep = photons[1].DeltaR(leptons[sorted_leptons[1].second.second]);
                }
            }
        }
    }
    if( photons.size() > 1 ) { 
        OUT::leadPhot_pt = sorted_photons[0].first;
        OUT::sublPhot_pt = sorted_photons[1].first;

        int leadidx = sorted_photons[0].second;
        int sublidx = sorted_photons[1].second;

        OUT::dphi_met_ph1 = photons[leadidx].DeltaPhi( metlv );
        OUT::dphi_met_ph2 = photons[sublidx].DeltaPhi( metlv );

    }
    else if ( photons.size() == 1 ) {
        OUT::leadPhot_pt = sorted_photons[0].first;
        OUT::sublPhot_pt = 0;
        OUT::dphi_met_ph1 = photons[sorted_photons[0].second].DeltaPhi( metlv );
        OUT::dphi_met_ph2 = -99; 
    }

    if( leptons.size() == 2 ) {
        OUT::pt_secondLepton = sorted_leptons[1].first;
    }
    if( leptons.size() == 3 ) {
        OUT::pt_thirdLepton = sorted_leptons[2].first;
    }

    if( leptons.size() > 1 ) {
        OUT::m_leplep = ( leptons[0] + leptons[1] ).M();
        OUT::pt_leplep = ( leptons[0] + leptons[1] ).Pt();
        if (leptons_uncorr.size() > 1) {
            OUT::m_leplep_uncorr = ( leptons_uncorr[0] + leptons_uncorr[1] ).M();
        }

        int leadidx = sorted_leptons[0].second.second;
        int sublidx = sorted_leptons[1].second.second;

        OUT::dphi_met_lep1 = leptons[leadidx].DeltaPhi( metlv );
        OUT::dphi_met_lep2 = leptons[sublidx].DeltaPhi( metlv );

        if( photons.size() > 0 ) { 
            OUT::m_leplepph  = (leptons[0] + leptons[1] + photons[0] ).M();
            OUT::pt_leplepph  = (leptons[0] + leptons[1] + photons[0] ).Pt();
        }
    }

    if( leptons.size() == 1 ) {
       
        OUT::mt_lep_met = Utils::calc_mt( leptons[0], metlv );
        OUT::dphi_met_lep1 = leptons[sorted_leptons[0].second.second].DeltaPhi( metlv );

        if( photons.size() > 1 ) { 

            int leadidx = sorted_photons[0].second;
            int sublidx = sorted_photons[1].second;

            OUT::leadPhot_lepDR = photons[leadidx].DeltaR(leptons[0]);
            OUT::sublPhot_lepDR = photons[sublidx].DeltaR(leptons[0]);
            OUT::phPhot_lepDR = (photons[leadidx]+photons[sublidx]).DeltaR(photons[sublidx]);
            
            OUT::leadPhot_lepDPhi = photons[leadidx].DeltaPhi(leptons[0]);
            OUT::sublPhot_lepDPhi = photons[sublidx].DeltaPhi(leptons[0]);
            OUT::phPhot_lepDPhi = (photons[leadidx]+photons[sublidx]).DeltaPhi(photons[sublidx]);
            
            OUT::mt_lepph1_met = Utils::calc_mt( leptons[0] + photons[leadidx], metlv );
            OUT::mt_lepph2_met = Utils::calc_mt( leptons[0] + photons[sublidx], metlv );

            OUT::mt_lepphph_met =Utils::calc_mt( leptons[0] + photons[leadidx] + photons[sublidx], metlv );

            OUT::m_lepph1 = ( leptons[0] + photons[leadidx] ).M();
            OUT::m_lepph2 = ( leptons[0] + photons[sublidx] ).M();
            OUT::m_lepphph = ( leptons[0] + photons[leadidx] + photons[sublidx] ).M();

            OUT::pt_lepph1 = ( leptons[0] + photons[leadidx] ).Pt();
            OUT::pt_lepph2 = ( leptons[0] + photons[sublidx] ).Pt();
            OUT::pt_lepphph = ( leptons[0] + photons[leadidx] + photons[sublidx] ).Pt();

            float zmass = 91.2;
            float leaddiff = fabs( OUT::m_lepph1 - zmass);
            float subldiff = fabs( OUT::m_lepph2 - zmass);
            if( leaddiff < subldiff ) {
                OUT::m_minZdifflepph = leaddiff;
            }
            else {
                OUT::m_minZdifflepph = subldiff;
            }
        }
        else if( photons.size() == 1 ) {

            int leadidx = sorted_photons[0].second;
            OUT::leadPhot_lepDR = photons[leadidx].DeltaR(leptons[0]);

            OUT::mt_lepph1_met = Utils::calc_mt( leptons[0] + photons[leadidx], metlv );

            OUT::m_lepph1 = ( leptons[0] + photons[leadidx] ).M();
            OUT::pt_lepph1 = ( leptons[0] + photons[leadidx] ).Pt();

        }
            
            
    }
    if( leptons.size() > 2 ) {
        std::vector< std::pair<float, float> > lep_pair_masses;
        for( unsigned i = 0; i < leptons.size() ; i++ ) {
            for( unsigned j = i+1; j < leptons.size() ; j++ ) {
                lep_pair_masses.push_back( std::make_pair( fabs(91.1876 - (leptons[i]+leptons[j]).M() ),(leptons[i]+leptons[j]).M())  );
            }
       }
        //sort from smallest to greatest
        std::sort( lep_pair_masses.begin(), lep_pair_masses.end() );

        OUT::m_leplepZ = lep_pair_masses[0].second;
    }
    if( leptons.size() == 3 ) {
        OUT::m_3lep = ( leptons[0] + leptons[1] + leptons[2] ).M();
    }

    if( leptons.size() == 4 ) {
        OUT::m_4lep = ( leptons[0] + leptons[1] + leptons[2] + leptons[3] ).M();
    }

    std::vector<TLorentzVector> objects;
    objects.insert(objects.begin(), leptons.begin(), leptons.end() );
    objects.insert(objects.begin(), photons.begin(), photons.end() );

    if( objects.size() > 2 ) {
        std::vector<float> masses;
        for( unsigned i = 0; i < objects.size(); ++i ) {
            for( unsigned j = i+1; j < objects.size(); ++j ) {
                masses.push_back( (objects[i] + objects[j]).M() );
            }
        }
        masses.push_back( (objects[0]+objects[1]+objects[2]).M() );

        std::vector<std::pair<float, int > > sorted_masses;
        for( unsigned i = 0; i < masses.size() ; ++i ) {
            sorted_masses.push_back( std::make_pair( std::fabs( 91.1876 - masses[i] ), i ) );
        }
        //sort with the smallest first
        std::sort(sorted_masses.begin(), sorted_masses.end());
        int nearestZidx = sorted_masses[0].second;
        OUT::m_nearestToZ = masses[nearestZidx];

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
    int nLepTrigMatch = 0;
    int nElTrigMatch = 0;
    int nElPh = 0;
    int nEl = 0;
    int nPhTruthMatchEl = 0;
    int nPhPassSIEIEAndEVeto =0;

    for( int i = 0; i < OUT::mu_n; ++i ) {
        nLep++;
        if( OUT::mu_pt->at(i) > 25 ) {
            nLep25++;
        }

        if( OUT::mu_pt->at(i) > 24 && OUT::mu_triggerMatch->at(i) ) {
            nLepTrigMatch++;
        }
    }
    for( int i = 0; i < OUT::el_n; ++i ) {
        nLep++;
        nElPh++;
        nEl++;
        if( OUT::el_pt->at(i) > 25 ) {
            nLep25++;
        }

        if( OUT::el_pt->at(i) > 27 && OUT::el_triggerMatch->at(i) && OUT::el_passMvaTrig->at(i) ) {
            nLepTrigMatch++;
            nElTrigMatch++;
        }
    }

    for( int i = 0; i < OUT::ph_n; ++i ) {
        nElPh++;
        if( OUT::ph_truthMatch_el->at(i) ) {
            nPhTruthMatchEl++;
        }
        if( OUT::ph_passSIEIEMedium->at(i) && OUT::ph_eleVeto->at(i)== 0 ) {
            nPhPassSIEIEAndEVeto++;
        }
    }

    if( !config.PassInt( "cut_nLep", nLep ) ) keep_event=false;
    if( !config.PassInt( "cut_nLep25", nLep25 ) ) keep_event=false;
    if( !config.PassInt( "cut_nLepTrigMatch", nLepTrigMatch ) ) keep_event=false;
    if( !config.PassInt( "cut_nElTrigMatch", nElTrigMatch ) ) keep_event=false;
    if( !config.PassInt( "cut_nPh", nPh ) )   keep_event = false;
    if( !config.PassInt( "cut_nElPh", nElPh ) )   keep_event = false;
    if( !config.PassInt( "cut_nEl", nEl ) )   keep_event = false;
    if( !config.PassInt( "cut_nPhTruthMatchEl", nPhTruthMatchEl ) )   keep_event = false;
    if( !config.PassInt( "cut_nPhPassSIEIEAndEVeto", nPhPassSIEIEAndEVeto) )   keep_event = false;
    if( !config.PassInt( "cut_nPhPassMedium", OUT::ph_medium_n) )   keep_event = false;
    if( !config.PassInt( "cut_nPhPassMediumNoEleVeto", OUT::ph_mediumNoEleVeto_n) )   keep_event = false;
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

    #endif //el_n
    #endif //mu_n
    #endif //ph_n
    return keep_event;
}

bool RunModule::FilterBlind( ModuleConfig & config ) const {

    bool keep_event = true;

    bool pass_blind = true;
    if( !config.PassInt( "cut_nPhPassMedium", OUT::ph_medium_n ) ) pass_blind=false;
    if( !config.PassInt( "cut_ph_pt_lead", OUT::leadPhot_pt) ) pass_blind=false;

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
        CopyPrefixIndexBranchesInToOut( "jet_", idx );

    }
    #endif
}

