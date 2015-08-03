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

#ifdef MODULE_AddMETUncert
    outtree->Branch("pfType01METUncertMuonUP", &OUT::pfType01METUncertMuonUP, "pfType01METUncertMuonUP/F" );
    outtree->Branch("pfType01METUncertMuonDN", &OUT::pfType01METUncertMuonDN, "pfType01METUncertMuonDN/F" );
    outtree->Branch("pfType01METUncertEMUP", &OUT::pfType01METUncertEMUP, "pfType01METUncertEMUP/F" );
    outtree->Branch("pfType01METUncertEMDN", &OUT::pfType01METUncertEMDN, "pfType01METUncertEMDN/F" );
    outtree->Branch("pfType01METUncertJESUP", &OUT::pfType01METUncertJESUP, "pfType01METUncertJESUP/F" );
    outtree->Branch("pfType01METUncertJESDN", &OUT::pfType01METUncertJESDN, "pfType01METUncertJESDN/F" );
    outtree->Branch("pfType01METUncertJERUP", &OUT::pfType01METUncertJERUP, "pfType01METUncertJERUP/F" );
    outtree->Branch("pfType01METUncertJERDN", &OUT::pfType01METUncertJERDN, "pfType01METUncertJERDN/F" );
    outtree->Branch("pfType01METUncertUnClusUP", &OUT::pfType01METUncertUnClusUP, "pfType01METUncertUnClusUP/F" );
    outtree->Branch("pfType01METUncertUnClusDN", &OUT::pfType01METUncertUnClusDN, "pfType01METUncertUnClusDN/F" );

    outtree->Branch("mt_lep_metUncertMuonUP", &OUT::mt_lep_metUncertMuonUP, "mt_lep_metUncertMuonUP/F" );
    outtree->Branch("mt_lep_metUncertMuonDN", &OUT::mt_lep_metUncertMuonDN, "mt_lep_metUncertMuonDN/F" );
    outtree->Branch("mt_lep_metUncertEMUP", &OUT::mt_lep_metUncertEMUP, "mt_lep_metUncertEMUP/F" );
    outtree->Branch("mt_lep_metUncertEMDN", &OUT::mt_lep_metUncertEMDN, "mt_lep_metUncertEMDN/F" );
    outtree->Branch("mt_lep_metUncertJESUP", &OUT::mt_lep_metUncertJESUP, "mt_lep_metUncertJESUP/F" );
    outtree->Branch("mt_lep_metUncertJESDN", &OUT::mt_lep_metUncertJESDN, "mt_lep_metUncertJESDN/F" );
    outtree->Branch("mt_lep_metUncertJERUP", &OUT::mt_lep_metUncertJERUP, "mt_lep_metUncertJERUP/F" );
    outtree->Branch("mt_lep_metUncertJERDN", &OUT::mt_lep_metUncertJERDN, "mt_lep_metUncertJERDN/F" );
    outtree->Branch("mt_lep_metUncertUnClusUP", &OUT::mt_lep_metUncertUnClusUP, "mt_lep_metUncertUnClusUP/F" );
    outtree->Branch("mt_lep_metUncertUnClusDN", &OUT::mt_lep_metUncertUnClusDN, "mt_lep_metUncertUnClusDN/F" );
#endif

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {

        if( mod_conf.GetName() == "VaryEGammaScale" ) {
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "Direction" );
            if( itr != mod_conf.GetInitData().end() ) {
                _egamma_var = itr->second;
            }
        }
        if( mod_conf.GetName() == "VaryMuonScale" ) {
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "Direction" );
            if( itr != mod_conf.GetInitData().end() ) {
                _muon_var = itr->second;
            }
        }
	
    }

    // -------------------------------------
    // To get the resolution information
    // in cases where the reco jet isnt 
    // matched to a gen jet
    // -------------------------------------
    std::string ak5CHSTag = "external/CMSSW_5_3_28/src/CondFormats/JetMETObjects/data/JetResolutionInputAK5PFCHS.txt"; 
    std::string ak5Tag = "external/CMSSW_5_3_28/src/CondFormats/JetMETObjects/data/JetResolutionInputAK5PF.txt"; 
    AK5PFCHSPar = new JetCorrectorParameters(ak5CHSTag);
    AK5PFPar    = new JetCorrectorParameters(ak5Tag);

    ak5PFResolution =  new SimpleJetResolution(*AK5PFPar);
    ak5PFCHSResolution =  new SimpleJetResolution(*AK5PFCHSPar);

    // -------------------------------------
    // Jet resolution binned in eta
    // -------------------------------------
    jet_res_corr_dn.push_back( std::make_pair( std::make_pair( 0.0, 0.5 ), 1.053 ) );
    jet_res_corr_dn.push_back( std::make_pair( std::make_pair( 0.5, 1.1 ), 1.071 ) );
    jet_res_corr_dn.push_back( std::make_pair( std::make_pair( 1.1, 1.7 ), 1.092 ) );
    jet_res_corr_dn.push_back( std::make_pair( std::make_pair( 1.7, 2.3 ), 1.162 ) );
    jet_res_corr_dn.push_back( std::make_pair( std::make_pair( 2.3, 2.8 ), 1.192 ) );
    jet_res_corr_dn.push_back( std::make_pair( std::make_pair( 2.8, 3.2 ), 1.332 ) );
    jet_res_corr_dn.push_back( std::make_pair( std::make_pair( 3.2, 5.0 ), 0.865 ) );

    jet_res_corr_up.push_back( std::make_pair( std::make_pair( 0.0, 0.5 ), 1.105 ) );
    jet_res_corr_up.push_back( std::make_pair( std::make_pair( 0.5, 1.1 ), 1.127 ) );
    jet_res_corr_up.push_back( std::make_pair( std::make_pair( 1.1, 1.7 ), 1.150 ) );
    jet_res_corr_up.push_back( std::make_pair( std::make_pair( 1.7, 2.3 ), 1.254 ) );
    jet_res_corr_up.push_back( std::make_pair( std::make_pair( 2.3, 2.8 ), 1.316 ) );
    jet_res_corr_up.push_back( std::make_pair( std::make_pair( 2.8, 3.2 ), 1.458 ) );
    jet_res_corr_up.push_back( std::make_pair( std::make_pair( 3.2, 5.0 ), 1.247 ) );

    rand = new TRandom3(0);

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

    if( config.GetName() == "AddMETUncert" ) {
        AddMETUncert( config );
    }
    if( config.GetName() == "VaryEGammaScale" ) {
        VaryEGammaScale( config );
    }
    if( config.GetName() == "VaryMuonScale" ) {
        VaryMuonScale( config );
    }
    
    return keep_evt;

}

void RunModule::VaryMuonScale( ModuleConfig & /*config*/ ) const {

#ifdef MODULE_VaryMuonScale

    ClearOutputPrefix("mu_");
    for( int midx = 0 ; midx < IN::mu_n; ++midx ) {

        float pt  = IN::mu_pt->at(midx);
        float eta = IN::mu_eta->at(midx);
        float phi = IN::mu_phi->at(midx);
        float en  = IN::mu_e->at(midx);

        TLorentzVector lvorig;
        lvorig.SetPtEtaPhiE( pt, eta, phi, en );

        float mass = lvorig.M();

        float unc=0.002;

        if( _muon_var == "UP" ) {
            pt = pt + pt*unc;
        }
        else if( _muon_var == "DN" ) {
            pt = pt - pt*unc;
        }
        else {
            std::cout << "VaryMuonScale : ERROR -- variation direction must be UP or DN" << std::endl;
        }

        TLorentzVector lvnew;
        lvnew.SetPtEtaPhiM( pt, eta, phi, mass );

        CopyPrefixIndexBranchesInToOut( "mu_", midx );
        OUT::mu_pt->pop_back();
        OUT::mu_e ->pop_back();
        OUT::mu_pt->push_back(lvnew.Pt());
        OUT::mu_e ->push_back(lvnew.E());
    }
#endif
}

void RunModule::VaryEGammaScale( ModuleConfig & /*config*/ ) const {

    std::cout << "IN VARYEGAMMA" << std::endl;

#ifdef MODULE_VaryEGammaScale
    std::cout << "IN VARYEGAMMA2" << std::endl;

    // remove the output variables so we can 
    // write new ones
    ClearOutputPrefix("el_");

    for( int eidx = 0 ; eidx < IN::el_n; ++eidx ) {

        float pt  = IN::el_pt->at(eidx);
        float eta = IN::el_eta->at(eidx);
        float phi = IN::el_phi->at(eidx);
        float en  = IN::el_e->at(eidx);

        TLorentzVector lvorig;
        lvorig.SetPtEtaPhiE( pt, eta, phi, en );

        float mass = lvorig.M();

        float unc;
        if( fabs( eta ) < 1.44 ) {
            unc = 0.006;
        }
        else {
            unc = 0.015;
        }

        if( _egamma_var == "UP" ) {
            pt = pt + pt*unc;
        }
        else if( _egamma_var == "DN" ) {
            pt = pt - pt*unc;
        }
        else {
            std::cout << "VaryEGammaScale : ERROR -- variation direction must be UP or DN" << std::endl;
        }

        TLorentzVector lvnew;
        lvnew.SetPtEtaPhiM( pt, eta, phi, mass );

        CopyPrefixIndexBranchesInToOut( "el_", eidx );
        OUT::el_pt->pop_back();
        OUT::el_e ->pop_back();
        OUT::el_pt->push_back(lvnew.Pt());
        OUT::el_e ->push_back(lvnew.E());
    }

    // remove the output variables so we can 
    // write new ones
    ClearOutputPrefix("ph_");

    for( int pidx = 0 ; pidx < IN::ph_n; ++pidx ) {

        float pt  = IN::ph_pt->at(pidx);
        float eta = IN::ph_eta->at(pidx);
        float phi = IN::ph_phi->at(pidx);

        TLorentzVector lvorig;
        lvorig.SetPtEtaPhiM( pt, eta, phi, 0.0 );

        float unc;
        if( fabs( eta ) < 1.44 ) {
            unc = 0.006;
        }
        else {
            unc = 0.015;
        }

        if( _egamma_var == "UP" ) {
            pt = pt + pt*unc;
        }
        else if( _egamma_var == "DN" ) {
            pt = pt - pt*unc;
        }
        else {
            std::cout << "VaryEGammaScale : ERROR -- variation direction must be UP or DN" << std::endl;
        }

        TLorentzVector lvnew;
        lvnew.SetPtEtaPhiM( pt, eta, phi, 0. );

        CopyPrefixIndexBranchesInToOut( "ph_", pidx );
        OUT::ph_pt->pop_back();
        OUT::ph_pt->push_back(lvnew.Pt());
    }

    // also do it for leading / subleading
    if( OUT::isEB_leadph12 ) {
        if( _egamma_var == "UP" ) {
            OUT::pt_leadph12 = OUT::pt_leadph12 * ( 1 + 0.006 );
        }
        else {
            OUT::pt_leadph12 = OUT::pt_leadph12 * ( 1 - 0.006 );
        }
    }
    if( OUT::isEE_leadph12 ) {
        if( _egamma_var == "UP" ) {
            OUT::pt_leadph12 = OUT::pt_leadph12 * ( 1 + 0.015 );
        }
        else {
            OUT::pt_leadph12 = OUT::pt_leadph12 * ( 1 - 0.015 );
        }
    }

    std::cout << OUT::isEB_sublph12  << std::endl;

    if( OUT::isEB_sublph12 ) {
        if( _egamma_var == "UP" ) {
            std::cout << OUT::pt_sublph12 << std::endl;
            OUT::pt_sublph12 = OUT::pt_sublph12 * ( 1 + 0.006 );
            std::cout << OUT::pt_sublph12 << std::endl;
        }
        
        else {
            OUT::pt_sublph12 = OUT::pt_sublph12 * ( 1 - 0.006 );
        }
    }
    if( OUT::isEE_sublph12 ) {
        if( _egamma_var == "UP" ) {
            OUT::pt_sublph12 = OUT::pt_sublph12 * ( 1 + 0.015 );
        }
        else {
            OUT::pt_sublph12 = OUT::pt_sublph12 * ( 1 - 0.015 );
        }
    }


#endif

}

void RunModule::AddMETUncert( ModuleConfig & /*config*/ ) const {

#ifdef MODULE_AddMETUncert
    OUT::pfType01METUncertMuonUP   = OUT::pfType01MET;
    OUT::pfType01METUncertMuonDN   = OUT::pfType01MET;
    OUT::pfType01METUncertEMUP     = OUT::pfType01MET;
    OUT::pfType01METUncertEMDN     = OUT::pfType01MET;
    OUT::pfType01METUncertJESUP    = OUT::pfType01MET;
    OUT::pfType01METUncertJESDN    = OUT::pfType01MET;
    OUT::pfType01METUncertJERUP    = OUT::pfType01MET;
    OUT::pfType01METUncertJERDN    = OUT::pfType01MET;
    OUT::pfType01METUncertUnClusUP = OUT::pfType01MET;
    OUT::pfType01METUncertUnClusDN = OUT::pfType01MET;

    OUT::mt_lep_metUncertMuonUP    = OUT::mt_lep_met;
    OUT::mt_lep_metUncertMuonDN    = OUT::mt_lep_met;
    OUT::mt_lep_metUncertEMUP      = OUT::mt_lep_met;
    OUT::mt_lep_metUncertEMDN      = OUT::mt_lep_met;
    OUT::mt_lep_metUncertJESUP     = OUT::mt_lep_met;
    OUT::mt_lep_metUncertJESDN     = OUT::mt_lep_met;
    OUT::mt_lep_metUncertJERUP     = OUT::mt_lep_met;
    OUT::mt_lep_metUncertJERDN     = OUT::mt_lep_met;
    OUT::mt_lep_metUncertUnClusUP  = OUT::mt_lep_met;
    OUT::mt_lep_metUncertUnClusDN  = OUT::mt_lep_met;

    TLorentzVector metlv_orig;
    metlv_orig.SetPtEtaPhiM( IN::pfType01MET, 0.0, IN::pfType01METPhi, 0.0 );

    TLorentzVector metlv_jer_up( metlv_orig );
    TLorentzVector metlv_jer_dn( metlv_orig );

    TLorentzVector metlv_jes_up( metlv_orig );
    TLorentzVector metlv_jes_dn( metlv_orig );

    TLorentzVector metlv_em_up( metlv_orig );
    TLorentzVector metlv_em_dn( metlv_orig );

    TLorentzVector metlv_mu_up( metlv_orig );
    TLorentzVector metlv_mu_dn( metlv_orig );

    TLorentzVector metlv_unclus_up( metlv_orig );
    TLorentzVector metlv_unclus_dn( metlv_orig );

    // Get the jets of interest
    std::vector<int> jets_index;
    std::vector<TLorentzVector> jets_orig;
    for( int idx = 0; idx < IN::jet_n; ++idx ) {

        float pt  = IN::jet_pt ->at(idx);

        if( pt < 10 ) continue;

        float eta = IN::jet_eta->at(idx);
        float phi = IN::jet_phi->at(idx);
        float en  = IN::jet_e  ->at(idx);


        TLorentzVector jetlv;
        jetlv.SetPtEtaPhiE( pt, eta, phi, en );

        jets_orig.push_back( jetlv );
        jets_index.push_back( idx );

    }

    // Get the photons and electrons of interest
    std::vector<int> phots_index;
    std::vector<TLorentzVector> phots_orig;
    for(int idx = 0 ; idx < IN::ph_n; ++idx ) {

        float pt = IN::ph_pt->at(idx);
        if( pt < 10 ) continue;

        float eta = IN::ph_eta->at(idx);
        float phi = IN::ph_phi->at(idx);
        float en  = IN::ph_e ->at(idx);

        TLorentzVector phlv;
        phlv.SetPtEtaPhiE( pt, eta, phi, en );

        phots_index.push_back( idx );
        phots_orig.push_back( phlv );

    }

    // for mT calc
    std::vector<TLorentzVector> leptons;

    std::vector<int> eles_index;
    std::vector<TLorentzVector> eles_orig;
    for(int idx = 0 ; idx < IN::el_n; ++idx ) {

        float pt = IN::el_pt->at(idx);
        if( pt < 10 ) continue;

        float eta = IN::el_eta->at(idx);
        float phi = IN::el_phi->at(idx);
        float en  = IN::el_e ->at(idx);

        TLorentzVector ellv;
        ellv.SetPtEtaPhiE( pt, eta, phi, en );

        //if( pt >= 30 ) {
            leptons.push_back( ellv );
        //}



        eles_index.push_back( idx );
        eles_orig.push_back( ellv );

    }
   
    std::vector<int> muons_index;
    std::vector<TLorentzVector> muons_orig;
    for(int idx = 0 ; idx < IN::mu_n; ++idx ) {

        float pt = IN::mu_pt->at(idx);
        if( pt < 10 ) continue;

        float eta = IN::mu_eta->at(idx);
        float phi = IN::mu_phi->at(idx);
        float en  = IN::mu_e ->at(idx);

        TLorentzVector mulv;
        mulv.SetPtEtaPhiE( pt, eta, phi, en );

        //if( pt >= 25 ) {
            leptons.push_back( mulv );
       // }
        muons_index.push_back( idx );
        muons_orig.push_back( mulv );

    }
   
    std::vector<TLorentzVector> jets_jer_up;
    std::vector<TLorentzVector> jets_jer_dn;
    std::vector<TLorentzVector> jets_jes_up;
    std::vector<TLorentzVector> jets_jes_dn;

    GetJetsJER( jets_index, "up", jets_jer_up );
    GetJetsJER( jets_index, "dn", jets_jer_dn );

    GetJetsJES( jets_index, "up", jets_jes_up );
    GetJetsJES( jets_index, "dn", jets_jes_dn );

    std::vector<TLorentzVector> phots_up;
    std::vector<TLorentzVector> phots_dn;
    GetPhotonsScaled( phots_index, "up", phots_up ); 
    GetPhotonsScaled( phots_index, "dn", phots_dn ); 

    std::vector<TLorentzVector> eles_up;
    std::vector<TLorentzVector> eles_dn;
    GetElectronsScaled( eles_index, "up", eles_up ); 
    GetElectronsScaled( eles_index, "dn", eles_dn ); 

    std::vector<TLorentzVector> muons_up;
    std::vector<TLorentzVector> muons_dn;
    GetMuonsScaled( muons_index, "up", muons_up ); 
    GetMuonsScaled( muons_index, "dn", muons_dn ); 

    std::vector<TLorentzVector> hard_objs;
    hard_objs.insert(hard_objs.begin(), jets_orig.begin(), jets_orig.end());
    hard_objs.insert(hard_objs.begin(), phots_orig.begin(), phots_orig.end());
    hard_objs.insert(hard_objs.begin(), eles_orig.begin(), eles_orig.end());
    hard_objs.insert(hard_objs.begin(), muons_orig.begin(), muons_orig.end());

    GetUnClusNewMet( hard_objs, 1.1, metlv_unclus_up );
    GetUnClusNewMet( hard_objs, 0.9, metlv_unclus_dn );

    GetNewMet( jets_orig, jets_jer_up, metlv_jer_up );
    GetNewMet( jets_orig, jets_jer_dn, metlv_jer_dn );

    GetNewMet( jets_orig, jets_jes_up, metlv_jes_up );
    GetNewMet( jets_orig, jets_jes_dn, metlv_jes_dn );

    // electrons and photons should be correlated
    GetNewMet( eles_orig, eles_up, metlv_em_up );
    GetNewMet( phots_orig, phots_up, metlv_em_up );

    GetNewMet( eles_orig, eles_dn, metlv_em_dn );
    GetNewMet( phots_orig, phots_dn, metlv_em_dn );

    GetNewMet( muons_orig, muons_up, metlv_mu_up );
    GetNewMet( muons_orig, muons_dn, metlv_mu_dn );
    
    OUT::pfType01METUncertMuonUP   = metlv_mu_up    .Pt();
    OUT::pfType01METUncertMuonDN   = metlv_mu_dn    .Pt();
    OUT::pfType01METUncertEMUP     = metlv_em_up    .Pt();
    OUT::pfType01METUncertEMDN     = metlv_em_dn    .Pt();
    OUT::pfType01METUncertJESUP    = metlv_jes_up   .Pt();
    OUT::pfType01METUncertJESDN    = metlv_jes_dn   .Pt();
    OUT::pfType01METUncertJERUP    = metlv_jer_up   .Pt();
    OUT::pfType01METUncertJERDN    = metlv_jer_dn   .Pt();
    OUT::pfType01METUncertUnClusUP = metlv_unclus_up.Pt();
    OUT::pfType01METUncertUnClusDN = metlv_unclus_dn.Pt();


    if( leptons.size() > 0 ) {
        OUT::mt_lep_metUncertMuonUP    = Utils::calc_mt( leptons[0], metlv_mu_up    );
        OUT::mt_lep_metUncertMuonDN    = Utils::calc_mt( leptons[0], metlv_mu_dn    );
        OUT::mt_lep_metUncertEMUP      = Utils::calc_mt( leptons[0], metlv_em_up    );
        OUT::mt_lep_metUncertEMDN      = Utils::calc_mt( leptons[0], metlv_em_dn    );
        OUT::mt_lep_metUncertJESUP     = Utils::calc_mt( leptons[0], metlv_jes_up   );
        OUT::mt_lep_metUncertJESDN     = Utils::calc_mt( leptons[0], metlv_jes_dn   );
        OUT::mt_lep_metUncertJERUP     = Utils::calc_mt( leptons[0], metlv_jer_up   );
        OUT::mt_lep_metUncertJERDN     = Utils::calc_mt( leptons[0], metlv_jer_dn   );
        OUT::mt_lep_metUncertUnClusUP  = Utils::calc_mt( leptons[0], metlv_unclus_up);
        OUT::mt_lep_metUncertUnClusDN  = Utils::calc_mt( leptons[0], metlv_unclus_dn);
    }
    else { 
        std::cout << "No LEPTON " << std::endl;
        OUT::mt_lep_metUncertMuonUP    = OUT::mt_lep_met;
        OUT::mt_lep_metUncertMuonDN    = OUT::mt_lep_met;
        OUT::mt_lep_metUncertEMUP      = OUT::mt_lep_met;
        OUT::mt_lep_metUncertEMDN      = OUT::mt_lep_met;
        OUT::mt_lep_metUncertJESUP     = OUT::mt_lep_met;
        OUT::mt_lep_metUncertJESDN     = OUT::mt_lep_met;
        OUT::mt_lep_metUncertJERUP     = OUT::mt_lep_met;
        OUT::mt_lep_metUncertJERDN     = OUT::mt_lep_met;
        OUT::mt_lep_metUncertUnClusUP  = OUT::mt_lep_met;
        OUT::mt_lep_metUncertUnClusDN  = OUT::mt_lep_met;
    }

#endif
}

void RunModule::GetJetsJER( const std::vector<int> &jets_index, const std::string &var, std::vector<TLorentzVector> & out_jets ) const {
#ifdef MODULE_AddMETUncert

    for( std::vector<int>::const_iterator idxitr = jets_index.begin(); idxitr != jets_index.end(); ++idxitr ) {

        int idx = *(idxitr);

        bool matched = (IN::jet_genIndex->at(idx) > 0);

        float pt  = IN::jet_pt ->at(idx);
        float eta = IN::jet_eta->at(idx);
        float phi = IN::jet_phi->at(idx);
        float en  = IN::jet_e->at(idx);

        TLorentzVector lvorig;
        lvorig.SetPtEtaPhiE( pt, eta, phi, en );
        float mass = lvorig.M();

        if( !matched ) {

            std::vector<float> fx, fY;
            fx.push_back(IN::jet_eta->at(idx));  // Jet Eta
            fY.push_back(IN::jet_pt->at(idx)); // Jet PT
            fY.push_back(IN::puTrue->at(0)); // Number of truth pileup
            float res = ak5PFResolution->resolution(fx,fY);
            float sf = FindJetJERCorr( var, eta );

            // this smearing can't improve the
            // resolution -- therefore only the 
            // worsened resolution should count 
            // and we keep the original value here
            if( sf < 1 ) {
                TLorentzVector newjet;
                newjet.SetPtEtaPhiM( pt, eta, phi, mass );
                out_jets.push_back(newjet);
            }
            else {

                float gauss_width_var = sqrt( sf*sf - 1 ) * res;

                float smear = rand->Gaus( 1, gauss_width_var );

                TLorentzVector newjet;
                newjet.SetPtEtaPhiM( pt*smear, eta, phi, mass );

                out_jets.push_back(newjet);
            }

        }
        else {


            float ptGen  = IN::jet_genPt ->at(idx);

            float sf = FindJetJERCorr( var, eta );

            float ptnew = ptGen + sf*( pt - ptGen );

            if( ptnew < 0 ) ptnew = 0;

            TLorentzVector newjet;
            newjet.SetPtEtaPhiM( ptnew, eta, phi, mass );

            out_jets.push_back(newjet);
               
        }
    }
#endif
}

float RunModule::FindJetJERCorr( const std::string &up_dn, float eta ) const {

    if( up_dn == "up" ) {
        return FindJetJERCorr( jet_res_corr_up, eta );
    }
    else if( up_dn == "dn" || up_dn == "down" ) {
        return FindJetJERCorr( jet_res_corr_dn, eta );
    }
    else {
        std::cout << "first argument must be 'up' or 'dn'" << std::endl;
        return -1;
    }
}


float RunModule::FindJetJERCorr( const std::vector<std::pair< std::pair<float, float>, float > > &corrs, float eta ) const {

    float abseta = fabs( eta );

    for( std::vector<std::pair< std::pair<float, float>, float > >::const_iterator itr = corrs.begin(); itr != corrs.end(); ++itr) {
        float eta1 = itr->first.first;
        float eta2 = itr->first.second;

        if( abseta > eta1 && abseta < eta2 ) {
            return itr->second;
        }
    }
    std::cout << "No correction factor found for eta = " << eta << std::endl;
    return -1;
}

void RunModule::GetJetsJES( const std::vector<int> &jets_index, const std::string &var, std::vector<TLorentzVector> & out_jets ) const {

#ifdef MODULE_AddMETUncert
    for( std::vector<int>::const_iterator idxitr = jets_index.begin(); idxitr != jets_index.end(); ++idxitr ) {

        int idx = *(idxitr);

        float pt  = IN::jet_pt ->at(idx);
        float eta = IN::jet_eta->at(idx);
        float phi = IN::jet_phi->at(idx);
        float en  = IN::jet_e->at(idx);

        TLorentzVector lvorig;
        lvorig.SetPtEtaPhiE( pt, eta, phi, en );
        float mass = lvorig.M();

        float unc = IN::jet_JECUnc->at(idx);

        float ptnew = 0.0;
        if( var == "up" ) {
            ptnew = pt + pt*unc;
        }
        else if( var == "dn" ) {
            ptnew = pt - pt*unc;
        }
        else {
            std::cout << "RunModule::GetJetJES -- ERROR : var should be 'up' or 'dn' " << std::endl;
        }

        TLorentzVector newlv;
        newlv.SetPtEtaPhiM( ptnew, eta, phi, mass);

        out_jets.push_back(newlv);
    }
#endif
}

void RunModule::GetElectronsScaled( const std::vector<int> &eles_index, const std::string &var, std::vector<TLorentzVector> & out_eles ) const {

#ifdef MODULE_AddMETUncert
    for( std::vector<int>::const_iterator idxitr = eles_index.begin(); idxitr != eles_index.end(); ++idxitr ) {

        int idx = *(idxitr);

        float pt  = IN::el_pt ->at(idx);
        float eta = IN::el_eta->at(idx);
        float phi = IN::el_phi->at(idx);
        float en  = IN::el_e->at(idx);

        TLorentzVector lvorig;
        lvorig.SetPtEtaPhiE( pt, eta, phi, en );
        float mass = lvorig.M();
        
        float unc = 0.0;
        if( fabs( eta ) < 1.44 )  unc = 0.006;
        else {
            unc = 0.015;
        }
        float ptnew = 0.0;

        if( var=="up") {
            ptnew = pt + pt*unc;
        }
        else if( var == "dn" ) {
            ptnew = pt - pt*unc;
        }
        else {
            std::cout << "RunModule::GetElectronsScaled -- ERROR : var should be 'up' or 'dn' " << std::endl;
        }

        TLorentzVector newlv;
        newlv.SetPtEtaPhiM( ptnew, eta, phi, mass );

        out_eles.push_back(newlv);

    }

#endif
}


void RunModule::GetPhotonsScaled( const std::vector<int> &phots_index, const std::string &var, std::vector<TLorentzVector> & out_phots ) const {

#ifdef MODULE_AddMETUncert
    for( std::vector<int>::const_iterator idxitr = phots_index.begin(); idxitr != phots_index.end(); ++idxitr ) {

        int idx = *(idxitr);

        float pt  = IN::ph_pt ->at(idx);
        float eta = IN::ph_eta->at(idx);
        float phi = IN::ph_phi->at(idx);
        
        float unc = 0.0;
        if( fabs( eta ) < 1.44 )  unc = 0.006;
        else {
            unc = 0.015;
        }
        float ptnew = 0.0;

        if( var=="up") {
            ptnew = pt + pt*unc;
        }
        else if( var == "dn" ) {
            ptnew = pt - pt*unc;
        }
        else {
            std::cout << "RunModule::GetPhotonsScaled -- ERROR : var should be 'up' or 'dn' " << std::endl;
        }

        TLorentzVector newlv;
        newlv.SetPtEtaPhiM( ptnew, eta, phi, 0.0 );

        out_phots.push_back(newlv);


    }

#endif
}


void RunModule::GetMuonsScaled( const std::vector<int> &muons_index, const std::string &var, std::vector<TLorentzVector> & out_muons ) const {

#ifdef MODULE_AddMETUncert
    for( std::vector<int>::const_iterator idxitr = muons_index.begin(); idxitr != muons_index.end(); ++idxitr ) {

        int idx = *(idxitr);

        float pt  = IN::mu_pt ->at(idx);
        float eta = IN::mu_eta->at(idx);
        float phi = IN::mu_phi->at(idx);
        float en  = IN::mu_e->at(idx);
        
        TLorentzVector lvorig;
        lvorig.SetPtEtaPhiE( pt, eta, phi, en );
        float mass = lvorig.M();

        float unc = 0.002;

        float ptnew=0.;
        if( var=="up") {
            ptnew = pt + pt*unc;
        }
        else if( var == "dn" ) {
            ptnew = pt - pt*unc;
        }
        else {
            std::cout << "RunModule::GetMuonsScaled -- ERROR : var should be 'up' or 'dn' " << std::endl;
        }

        TLorentzVector newlv;
        newlv.SetPtEtaPhiM( ptnew, eta, phi, mass );

        out_muons.push_back( newlv );

    }

#endif
}


void RunModule::GetNewMet( const std::vector<TLorentzVector> &objs_to_remove, const std::vector<TLorentzVector> &objs_to_add, TLorentzVector &met_orig ) const {

    if( objs_to_remove.size() != objs_to_add.size() ) {
        std::cout << "RunModule::GetNewMet -- ERROR : vectors of objects to remove and objects to add must be the same length!" << std::endl;
        return;
    }

    for( unsigned idx = 0; idx < objs_to_remove.size(); ++idx ) {
        met_orig += objs_to_remove[idx]; // remove objects from met by adding them
        met_orig -= objs_to_add[idx]; // add objects from met by subtracting them
    }

}

void RunModule::GetUnClusNewMet( const std::vector<TLorentzVector> &hard_objs, float var, TLorentzVector &met_orig ) const {

    TLorentzVector unclus(met_orig);

    BOOST_FOREACH( const TLorentzVector & obj, hard_objs ) {
        unclus += obj;
    }

    float pt_unclus = unclus.Pt();
    pt_unclus *= var;

    TLorentzVector unclus_var;
    unclus_var.SetPtEtaPhiM( pt_unclus, 0.0, unclus.Phi(), 0.0 );

    met_orig += unclus;
    met_orig -= unclus_var;

}

