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

#include "include/BranchInit.h"

#include "Core/Util.h"
#include "CalcWggEventVars.h"

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

    //OUT::ph_eleMatch = 0;

#ifdef MODULE_CalcDiJetVars
    outtree->Branch("zeppenfeld_w"         , &OUT::zeppenfeld_w         , "zeppenfeld_w/F"       );
    outtree->Branch("zeppenfeld_w_pos_desc"         , &OUT::zeppenfeld_w_pos_desc         , "zeppenfeld_w_pos_desc/O"       );
    outtree->Branch("zeppenfeld_z"         , &OUT::zeppenfeld_z         , "zeppenfeld_z/F"       );

    outtree->Branch("dphi_wg_jj"         , &OUT::dphi_wg_jj         , "dphi_wg_jj/F"       );
    outtree->Branch("dphi_zg_jj"         , &OUT::dphi_zg_jj         , "dphi_zg_jj/F"       );

    outtree->Branch("deta_j_j"         , &OUT::deta_j_j         , "deta_j_j/F"       );
    outtree->Branch("m_j_j"         , &OUT::m_j_j         , "m_j_j/F"       );
    outtree->Branch("dr_j_j"        , &OUT::dr_j_j        , "dr_j_j/F"      );
    outtree->Branch("dphi_j1_met"   , &OUT::dphi_j1_met   , "dphi_j1_met/F"      );
    outtree->Branch("dphi_j2_met"   , &OUT::dphi_j2_met   , "dphi_j2_met/F"      );
    outtree->Branch("dr_ph_j1"      , &OUT::dr_ph_j1      , "dr_ph_j1/F"      );
    outtree->Branch("dr_ph_j2"      , &OUT::dr_ph_j2      , "dr_ph_j2/F"      );
    outtree->Branch("dr_lep_j1"     , &OUT::dr_lep_j1     , "dr_lep_j1/F"      );
    outtree->Branch("dr_lep_j2"     , &OUT::dr_lep_j2     , "dr_lep_j2/F"      );

#endif

    //outtree->Branch("ph_eleMatch"   , &OUT::ph_eleMatch   );
    
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

    bool keep_evt = true;

    if( config.GetName() == "FilterPhoton" ) {
        FilterPhoton( config );
    }

    if( config.GetName() == "FilterMuon" ) {
        FilterMuon( config );
    }

    if( config.GetName() == "FilterElectron" ) {
        FilterElectron( config );
    }

    if( config.GetName() == "FilterJet" ) {
        FilterJet( config );
    }

    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }
    if( config.GetName() == "FilterBlind" ) {
        keep_evt &= FilterBlind( config );
    }
    if( config.GetName() == "CalcDiJetVars" ) {
        CalcDiJetVars( config );
    }
    if( config.GetName() == "CalcEventVars" ) {
        CalcEventVars( config );
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

void RunModule::FilterPhoton( ModuleConfig & config ) const {

    OUT::ph_n = 0;
    ClearOutputPrefix("ph_");
    //OUT::ph_eleMatch -> clear();

    for( int idx = 0; idx < IN::ph_n ; ++idx ) {

        if( !config.PassBool( "cut_ph_medium", IN::ph_passMedium->at(idx) ) ) continue;
        if( !config.PassFloat( "cut_ph_pt", IN::ph_pt->at(idx) ) ) continue;
        if( !config.PassBool( "cut_hasPixSeed", IN::ph_hasPixSeed->at(idx) ) ) continue;
        if( !config.PassBool( "cut_ph_csev", IN::ph_eleVeto->at(idx) ) ) continue;

        float min_el_dr = 100.0;

        TLorentzVector phlv;
        phlv.SetPtEtaPhiE( IN::ph_pt->at(idx), 
                           IN::ph_eta->at(idx), 
                           IN::ph_phi->at(idx), 
                           IN::ph_e->at(idx) );

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

        //OUT::ph_eleMatch->push_back(  ( min_el_dr < 0.4 ) );

        if( config.HasCut( "cut_el_ph_dr" ) ) { 
            if( !config.PassFloat( "cut_el_ph_dr", min_el_dr ) ) continue;
        }


        CopyPrefixIndexBranchesInToOut( "ph_", idx, false, "ph_ptSorted_" );
        OUT::ph_n++;

    }
}

void RunModule::FilterMuon( ModuleConfig & config ) const {

    OUT::mu_n = 0;
    ClearOutputPrefix("mu_");

    for( int idx = 0; idx < IN::mu_n ; ++idx ) {

        if( !config.PassFloat( "cut_mu_pt", IN::mu_pt->at(idx) ) ) continue;

        CopyPrefixIndexBranchesInToOut( "mu_", idx );
        OUT::mu_n++;

    }
}
void RunModule::FilterElectron( ModuleConfig & config ) const {

    OUT::el_n = 0;
    ClearOutputPrefix("el_");

    for( int idx = 0; idx < IN::el_n ; ++idx ) {

        if( !config.PassFloat( "cut_el_pt", IN::el_pt->at(idx) ) ) continue;

        CopyPrefixIndexBranchesInToOut( "el_", idx );
        OUT::el_n++;

    }
}

void RunModule::FilterJet( ModuleConfig & config ) const {

    OUT::jet_n = 0;
    ClearOutputPrefix("jet_");

    for( int idx = 0; idx < IN::jet_n ; ++idx ) {

        if( !config.PassFloat( "cut_jet_pt", IN::jet_pt->at(idx) ) ) continue;

        CopyPrefixIndexBranchesInToOut( "jet_", idx );
        OUT::jet_n++;

    }
}

// This is an example of a module that applies an
// event filter.  Note that it returns a bool instead
// of a void.  In principle the modules can return any
// type of variable, you just have to handle it
// in the ApplyModule function


void RunModule::CalcEventVars( ModuleConfig & config ) const {

    std::vector<TLorentzVector> photons;
    std::vector<TLorentzVector> muons;
    std::vector<TLorentzVector> electrons;
    std::vector<TLorentzVector> trigelectrons;
    std::vector<TLorentzVector> trigmuons;
    std::vector<std::pair<float, int> > sorted_photons;

    for( int idx = 0; idx < OUT::mu_n; idx++ ) {

        TLorentzVector lv;
        lv.SetPtEtaPhiM(  OUT::mu_pt->at(idx),
                          OUT::mu_eta->at(idx),
                          OUT::mu_phi->at(idx),
                          0.1057
                        );
        muons.push_back( lv );
        if( lv.Pt() > 25 && fabs(lv.Eta()) < 2.1 && OUT::mu_triggerMatch->at(idx) ) {
            trigmuons.push_back(lv);
        }
    }

    for( int idx = 0; idx < OUT::el_n; idx++ ) {

        TLorentzVector lv;
        lv.SetPtEtaPhiE(  OUT::el_pt->at(idx),
                          OUT::el_eta->at(idx),
                          OUT::el_phi->at(idx),
                          OUT::el_e->at(idx)
                        );
        electrons.push_back( lv );
        if( lv.Pt() > 30 && OUT::el_triggerMatch->at(idx) && OUT::el_passMvaTrig->at(idx) ) {
            trigelectrons.push_back( lv );
        }
    } 

    for( int idx = 0; idx < OUT::ph_n; idx++ ) {

        TLorentzVector lv;
        lv.SetPtEtaPhiE(  OUT::ph_pt->at(idx),
                          OUT::ph_eta->at(idx),
                          OUT::ph_phi->at(idx),
                          OUT::ph_e->at(idx)
                        );
        photons.push_back( lv );
        sorted_photons.push_back( std::make_pair( lv.Pt(), idx ) );
    } 

    TLorentzVector metlv;
    metlv.SetPtEtaPhiM( OUT::pfType01MET, 0.0, OUT::pfType01METPhi, 0.0 );

        
    std::map<std::string, float> results;
    std::map<std::string, std::vector<float> > vector_results;

    Wgg::CalcEventVars( photons, electrons, muons, trigelectrons, trigmuons, metlv, results, vector_results );

    CopyMapVarsToOut( results );
    CopyVectorMapVarsToOut( vector_results );

    // sort the list of photon momenta in descending order
    std::sort(sorted_photons.rbegin(), sorted_photons.rend());

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
}

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    int nPh = OUT::ph_n;
    if( !config.PassInt("cut_nPh", nPh ) ) keep_event = false;
    if( !config.PassInt("cut_nMuTrig", OUT::mu_passtrig25_n ) ) keep_event = false;
    if( !config.PassInt("cut_nElTrig", OUT::el_passtrig_n ) ) keep_event = false;
    if( !config.PassInt("cut_nLepTrig", (OUT::el_passtrig_n+OUT::mu_passtrig25_n) ) ) keep_event = false;
    if( !config.PassInt("cut_nEl", OUT::el_n ) ) keep_event = false;
    if( !config.PassInt("cut_nMu", OUT::mu_n ) ) keep_event = false;
    if( !config.PassInt("cut_nLep", (OUT::mu_n+OUT::el_n) ) ) keep_event = false;

    if( !config.PassFloat( "cut_mgg", OUT::m_ph1_ph2 ) )  keep_event=false;
    if( !config.PassFloat( "cut_dr_lep_ph1", OUT::dr_ph1_leadLep ) )  keep_event=false;
    if( !config.PassFloat( "cut_dr_lep_ph2", OUT::dr_ph2_leadLep ) )  keep_event=false;
    if( !config.PassFloat( "cut_dr_trigele_ph1", OUT::dr_ph1_trigEle ) )  keep_event=false;
    if( !config.PassFloat( "cut_dr_trigele_ph2", OUT::dr_ph2_trigEle ) )  keep_event=false;
    if( !config.PassFloat( "cut_dr_subllep_ph1", OUT::dr_ph1_sublLep ) )  keep_event=false;
    if( !config.PassFloat( "cut_dr_subllep_ph2", OUT::dr_ph2_sublLep ) )  keep_event=false;
    if( !config.PassFloat( "cut_leadPhot_trigElDR", OUT::leadPhot_trigElDR) )  keep_event=false;
    if( !config.PassFloat( "cut_sublPhot_trigElDR", OUT::sublPhot_trigElDR) )  keep_event=false;
    if( !config.PassFloat( "cut_leadPhot_trigMuDR", OUT::leadPhot_trigMuDR) )  keep_event=false;
    if( !config.PassFloat( "cut_sublPhot_trigMuDR", OUT::sublPhot_trigMuDR) )  keep_event=false;
    if( !config.PassFloat( "cut_dr_ph1_ph2", OUT::dr_ph1_ph2 ) )  keep_event=false;
    if( !config.PassFloat( "cut_m_lepphph", OUT::m_leadLep_ph1_ph2 ) )  keep_event=false;
    if( !config.PassFloat( "cut_m_lepph1", OUT::m_leadLep_ph1 ) )  keep_event=false;
    if( !config.PassFloat( "cut_m_lepph2", OUT::m_leadLep_ph2 ) )  keep_event=false;
    if( !config.PassFloat( "cut_m_trigelphph", OUT::m_trigelphph ) )  keep_event=false;
    if( !config.PassFloat( "cut_m_trigelph1" , OUT::m_trigelph1 ) )  keep_event=false;
    if( !config.PassFloat( "cut_m_trigelph2" , OUT::m_trigelph2 ) )  keep_event=false;
    if( !config.PassFloat( "cut_mt_lep_met", OUT::mt_lep_met) )  keep_event=false;
    if( !config.PassFloat( "cut_met", OUT::pfType01MET) )  keep_event=false;
    if( !config.PassFloat( "cut_m_leplep", OUT::m_leplep) )  keep_event=false;
    if( !config.PassFloat( "cut_m_mumu", OUT::m_mumu) )  keep_event=false;
    if( !config.PassFloat( "cut_m_elel", OUT::m_elel) )  keep_event=false;
    if( !config.PassFloat( "cut_mt_trigel_met", OUT::mt_trigel_met) )  keep_event=false;
    if( !config.PassFloat( "cut_mt_trigmu_met", OUT::mt_trigmu_met) )  keep_event=false;
    if( !config.PassFloat( "cut_sublPhot_leadLepDR", OUT::sublPhot_leadLepDR ) ) keep_event=false;
    if( !config.PassFloat( "cut_sublPhot_sublLepDR", OUT::sublPhot_sublLepDR ) ) keep_event=false;
    if( !config.PassFloat( "cut_leadPhot_leadLepDR", OUT::leadPhot_leadLepDR ) ) keep_event=false;
    if( !config.PassFloat( "cut_leadPhot_sublLepDR", OUT::leadPhot_sublLepDR ) ) keep_event=false;

    bool isEEEE = OUT::isEE_leadph12 && OUT::isEE_sublph12;
    if( !config.PassBool( "cut_isEEEE", isEEEE ) ) keep_event = false;

    if( !config.PassBool( "cut_MuTrig", (OUT::passTrig_mu24eta2p1 || OUT::passTrig_mu24 ) ) ) keep_event = false;
    if( !config.PassBool( "cut_ElTrig", (OUT::passTrig_ele27WP80) ) ) keep_event = false;
    if( !config.PassBool( "cut_DiMuTrig", (OUT::passTrig_mu17_mu8 || OUT::passTrig_mu17_Tkmu8 ) ) ) keep_event = false;
    if( !config.PassBool( "cut_DiElTrig", (OUT::passTrig_ele17_ele8_9 ) ) ) keep_event = false;


    
    // uncertainty variations
#ifdef EXISTS_mt_lep_metUncertMuonUP
    if( !config.PassFloat( "cut_mt_lep_metUncertMuonUP", OUT::mt_lep_metUncertMuonUP ) ) keep_event=false;
#endif
#ifdef EXISTS_mt_lep_metUncertMuonDN
    if( !config.PassFloat( "cut_mt_lep_metUncertMuonDN", OUT::mt_lep_metUncertMuonDN ) ) keep_event=false;
#endif
#ifdef EXISTS_mt_lep_metUncertEMUP
    if( !config.PassFloat( "cut_mt_lep_metUncertEMUP", OUT::mt_lep_metUncertEMUP ) ) keep_event=false;
#endif
#ifdef EXISTS_mt_lep_metUncertEMDN
    if( !config.PassFloat( "cut_mt_lep_metUncertEMDN", OUT::mt_lep_metUncertEMDN ) ) keep_event=false;
#endif
#ifdef EXISTS_mt_lep_metUncertJESUP
    if( !config.PassFloat( "cut_mt_lep_metUncertJESUP", OUT::mt_lep_metUncertJESUP ) ) keep_event=false;
#endif
#ifdef EXISTS_mt_lep_metUncertJESDN
    if( !config.PassFloat( "cut_mt_lep_metUncertJESDN", OUT::mt_lep_metUncertJESDN ) ) keep_event=false;
#endif
#ifdef EXISTS_mt_lep_metUncertJERUP
    if( !config.PassFloat( "cut_mt_lep_metUncertJERUP", OUT::mt_lep_metUncertJERUP ) ) keep_event=false;
#endif
#ifdef EXISTS_mt_lep_metUncertJERDN
    if( !config.PassFloat( "cut_mt_lep_metUncertJERDN", OUT::mt_lep_metUncertJERDN ) ) keep_event=false;
#endif
#ifdef EXISTS_mt_lep_metUncertUnClusUP
    if( !config.PassFloat( "cut_mt_lep_metUncertUnClusUP", OUT::mt_lep_metUncertUnClusUP ) ) keep_event=false;
#endif
#ifdef EXISTS_mt_lep_metUncertUnClusDN
    if( !config.PassFloat( "cut_mt_lep_metUncertUnClusDN", OUT::mt_lep_metUncertUnClusDN ) ) keep_event=false;
#endif
    
    if( OUT::ph_n > 1 ) {
        if( OUT::ph_pt->at(0) > OUT::ph_pt->at(1) ) {
            if( !config.PassBool( "cut_hasPixSeed_leadph12", OUT::ph_hasPixSeed->at(0) ) ) keep_event = false;
            if( !config.PassBool( "cut_hasPixSeed_sublph12", OUT::ph_hasPixSeed->at(1) ) ) keep_event = false;
            if( !config.PassBool( "cut_csev_leadph12", OUT::ph_eleVeto->at(0) ) ) keep_event = false;
            if( !config.PassBool( "cut_csev_sublph12", OUT::ph_eleVeto->at(1) ) ) keep_event = false;
            //if( !config.PassBool( "cut_overlapVeto_leadph12", OUT::ph_eleMatch->at(0) ) ) keep_event = false;
            //if( !config.PassBool( "cut_overlapVeto_sublph12", OUT::ph_eleMatch->at(1) ) ) keep_event = false;
        }
        else {
            if( !config.PassBool( "cut_hasPixSeed_leadph12", OUT::ph_hasPixSeed->at(1) ) ) keep_event = false;
            if( !config.PassBool( "cut_hasPixSeed_sublph12", OUT::ph_hasPixSeed->at(0) ) ) keep_event = false;
            if( !config.PassBool( "cut_csev_leadph12", OUT::ph_eleVeto->at(1) ) ) keep_event = false;
            if( !config.PassBool( "cut_csev_sublph12", OUT::ph_eleVeto->at(0) ) ) keep_event = false;
            //if( !config.PassBool( "cut_overlapVeto_leadph12", OUT::ph_eleMatch->at(1) ) ) keep_event = false;
            //if( !config.PassBool( "cut_overlapVeto_sublph12", OUT::ph_eleMatch->at(0) ) ) keep_event = false;
        }
    }

    // jet counting
    int n_jet30 = 0;
    int n_jet40 = 0;
    for( int i = 0; i < OUT::jet_n; ++i) {
        if( OUT::jet_pt->at( i ) > 30 ) {
            n_jet30++;
        }
        if( OUT::jet_pt->at( i ) > 40 ) {
            n_jet40++;
        }
    }

    if( !config.PassInt( "cut_nJet30", n_jet30 ) ) keep_event=false;
    if( !config.PassInt( "cut_nJet40", n_jet40 ) ) keep_event=false;

    return keep_event;
    
}

bool RunModule::FilterBlind( ModuleConfig & config ) const { 

    bool keep_event = true;

    bool pass_blind = true;
    if( !config.PassInt( "cut_nPhPassMedium", OUT::ph_mediumPassPSV_n ) ) pass_blind=false;
    if( !config.PassInt( "cut_ph_pt_lead", OUT::pt_leadph12) ) pass_blind=false;

    // electron channel mass
    if( OUT::el_passtrig_n > 0 ) {

        if( !config.PassFloat( "cut_m_lepphph", OUT::m_leadLep_ph1_ph2) && !config.PassFloat( "cut_m_lepph1", OUT::m_leadLep_ph1 ) && !config.PassFloat( "cut_m_lepph2", OUT::m_leadLep_ph2  ) )  pass_blind = false;

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

void RunModule::CalcDiJetVars( ModuleConfig & /*config*/ ) const {

#ifdef MODULE_CalcDiJetVars

    std::vector<TLorentzVector> leptons;
    for( int idx = 0; idx < OUT::mu_n ; ++idx ) {

        TLorentzVector mulv;
        mulv.SetPtEtaPhiM( OUT::mu_pt->at(idx),
                           OUT::mu_eta->at(idx),
                           OUT::mu_phi->at(idx),
                           0.105);

        leptons.push_back(mulv);

    }
    for( int idx = 0; idx < OUT::el_n ; ++idx ) {

        TLorentzVector ellv;
        ellv.SetPtEtaPhiM( OUT::el_pt->at(idx),
                           OUT::el_eta->at(idx),
                           OUT::el_phi->at(idx),
                           0.000511 );

        leptons.push_back(ellv);

    }

    TLorentzVector metlv;
    TLorentzVector metlvOrig;
    metlvOrig.SetPtEtaPhiM( OUT::pfType01MET, 0.0, OUT::pfType01METPhi, 0.0 );
    metlv.SetPtEtaPhiM( OUT::pfType01MET, 0.0, OUT::pfType01METPhi, 0.0 );

     
    OUT::zeppenfeld_w = 0.0;
    OUT::zeppenfeld_w_pos_desc = 0;
    OUT::dphi_wg_jj = 0.0;
    OUT::zeppenfeld_z = 0.0;
    OUT::dphi_zg_jj = 0.0;
    OUT::deta_j_j = 0.0;
    OUT::dr_j_j = 0.0;
    OUT::m_j_j = 0.0;

    OUT::dphi_j1_met = 0.0;
    OUT::dphi_j2_met = 0.0;
    OUT::dr_ph_j1 = 0.0;
    OUT::dr_ph_j2 = 0.0;
    OUT::dr_lep_j1 = 0.0;
    OUT::dr_lep_j2 = 0.0;

    if( OUT::jet_n > 1 ) {

        TLorentzVector jet1lv;
        TLorentzVector jet2lv;

        jet1lv.SetPtEtaPhiE( OUT::jet_pt->at(0), OUT::jet_eta->at(0), OUT::jet_phi->at(0), OUT::jet_e->at(0) );
        jet2lv.SetPtEtaPhiE( OUT::jet_pt->at(1), OUT::jet_eta->at(1), OUT::jet_phi->at(1), OUT::jet_e->at(1) );

        float rap_j1 = jet1lv.Rapidity();
        float rap_j2 = jet2lv.Rapidity();

        OUT::deta_j_j = jet1lv.Eta() - jet2lv.Eta();
        OUT::m_j_j = (jet1lv + jet2lv).M();
        OUT::dr_j_j = jet1lv.DeltaR(jet2lv);

        OUT::dphi_j1_met = jet1lv.DeltaPhi( metlv );
        OUT::dphi_j2_met = jet2lv.DeltaPhi( metlv );

        if( OUT::ph_n>0 ) {
            TLorentzVector phlv;
            phlv.SetPtEtaPhiM( OUT::ph_pt->at(0), OUT::ph_eta->at(0), OUT::ph_phi->at(0), 0.0 );

            OUT::dr_ph_j1 = phlv.DeltaR( jet1lv );
            OUT::dr_ph_j2 = phlv.DeltaR( jet2lv );

            if( leptons.size() > 0  ) {
                float solved_pz = -1;
                bool pos_desc = get_wgamma_nu_pz( leptons[0], metlv );
                //std::cout << "POS_DESC " << pos_desc << std::endl;
                OUT::zeppenfeld_w_pos_desc = pos_desc;

                if( metlv.Pt() < 0 ) {
                    std::cout << "ERROR IN CALCULATION -- Negative result returned " << solved_pz << std::endl;
                }
                else {
                    float rap_wg = ( leptons[0]+metlv+phlv).Rapidity();

                    OUT::zeppenfeld_w = fabs( rap_wg - ( rap_j1+rap_j2)/2.0 );

                }

                OUT::dphi_wg_jj = ( metlvOrig + leptons[0] + phlv ).DeltaPhi( jet1lv + jet2lv );
            }
            if( leptons.size() > 1 ) {

                OUT::dphi_zg_jj = ( phlv + leptons[0] + leptons[1] ).DeltaPhi( jet1lv + jet2lv );

                float rap_zg = ( leptons[0] + leptons[1] + phlv ).Rapidity();

                OUT::zeppenfeld_z = fabs( rap_zg - ( rap_j1 + rap_j2 )/2.0 );
            }
        } 
        if( leptons.size() > 0  ) {
            OUT::dr_lep_j1 = leptons[0].DeltaR( jet1lv );
            OUT::dr_lep_j2 = leptons[0].DeltaR( jet2lv );
        }
    }
#endif
}

bool RunModule::get_wgamma_nu_pz( const TLorentzVector lepton, TLorentzVector &metlv ) const {

    float solved_pz = -1;

    bool desc_pos = calc_constrained_nu_momentum( lepton, metlv, solved_pz );
    if( desc_pos ) {
        metlv.SetPz( solved_pz );
    }
    else {
        //std::cout << "DISCRIMINANT IS NEGATIVE" << std::endl;
        // require the discriminant to be zero
        // solve a second quadratic equation to 
        // rescale MET so that there is a solution

        float alpha = ( lepton.Px()*metlv.Px() + lepton.Py()*metlv.Py() )/ metlv.Pt();
        float delta = ( _m_w*_m_w - lepton.M()*lepton.M() );

        float Aval = 4*lepton.Pz()*lepton.Pz() - 4*lepton.E()*lepton.E() +4*alpha*alpha;
        float Bval = 4*alpha*delta;
        float Cval = delta*delta;

        float solution1=-1;
        float solution2=-1;

        bool success2 = solve_quadratic( Aval, Bval, Cval, solution1, solution2 );

        if( !success2 ) {
            std::cout << "SECOND FAILURE" << std::endl;
        }

        float scale1 = solution1/metlv.Pt();
        float scale2 = solution2/metlv.Pt();

        TLorentzVector metlv_sol1;
        TLorentzVector metlv_sol2;
        metlv_sol1.SetPtEtaPhiM( OUT::pfType01MET*scale1, 0.0, OUT::pfType01METPhi, 0.0 );
        metlv_sol2.SetPtEtaPhiM( OUT::pfType01MET*scale2, 0.0, OUT::pfType01METPhi, 0.0 );

        float pz_sol1 = -1;
        float pz_sol2 = -1;
        bool success_sol1 = calc_constrained_nu_momentum( lepton, metlv_sol1, pz_sol1 );
        bool success_sol2 = calc_constrained_nu_momentum( lepton, metlv_sol2, pz_sol2 );

        if( !success_sol1 ) {
            //std::cout << "FAILURE SOLUTION 1" << std::endl;
            metlv.SetPtEtaPhiM(-1, 0, 0, 0);
            return false;
        }

        if( !success_sol2 ) {
            //std::cout << "FAILURE SOLUTION 2" << std::endl;
            metlv.SetPtEtaPhiM(-1, 0, 0, 0);
            return false;
        }

        TVector3 solved_met3v_sol1;
        TVector3 solved_met3v_sol2;
        solved_met3v_sol1.SetXYZ(metlv_sol1.Px(), metlv_sol1.Py(), pz_sol1);
        solved_met3v_sol2.SetXYZ(metlv_sol2.Px(), metlv_sol2.Py(), pz_sol2);
        TLorentzVector solved_metlv_sol1;
        TLorentzVector solved_metlv_sol2;
        solved_metlv_sol1.SetVectM( solved_met3v_sol1 , 0.0 );
        solved_metlv_sol2.SetVectM( solved_met3v_sol2 , 0.0 );

        float wmass_sol1 = ( lepton + solved_metlv_sol1 ).M();
        float wmass_sol2 = ( lepton + solved_metlv_sol2 ).M();

        if( fabs( wmass_sol1 - _m_w ) < fabs( wmass_sol2 - _m_w ) ) {
            solved_pz = pz_sol1;
            metlv = metlv_sol1;
        }
        else {
            solved_pz = pz_sol2;
            metlv = metlv_sol2;
        }
        
    }
    return desc_pos;
}

bool RunModule::calc_constrained_nu_momentum( const TLorentzVector lepton, const TLorentzVector met, float & result ) const {

   float little_a = _m_w*_m_w - lepton.M()*lepton.M() + 2*( lepton.Px()*met.Px() + lepton.Py()*met.Py() );

   float Aval = ( 4*lepton.E()*lepton.E() ) - ( 4*lepton.Pz()*lepton.Pz() );
   float Bval = -4 * little_a * lepton.Pz();

   float Cval = 4*lepton.E()*lepton.E()*met.Pt()*met.Pt() - little_a*little_a;

   float solution1=-1;
   float solution2=-1;
   bool success = solve_quadratic( Aval, Bval, Cval, solution1, solution2 );

   if ( success ) {
      if( fabs(solution1 - lepton.Pz() ) < fabs( solution2 - lepton.Pz() ) ) {
          result = solution1;
      }
      else {
          result = solution2;
      }
   }
   return success;
}

bool RunModule::solve_quadratic( float Aval, float Bval, float Cval, float & solution1, float &solution2 ) const {

   float discriminant = Bval*Bval - 4*Aval*Cval;

   //std::cout << "DISCRIMINANT = " << discriminant << std::endl;

   if ( discriminant >= 0 ) {
      solution1 = ( -1*Bval + sqrt( discriminant ) ) / ( 2 * Aval ) ; 
      solution2 = ( -1*Bval - sqrt( discriminant ) ) / ( 2 * Aval ) ; 
      return true;
   }
   else {
       return false;
   }
}

RunModule::RunModule() {
    _m_w = 80.385;
}

