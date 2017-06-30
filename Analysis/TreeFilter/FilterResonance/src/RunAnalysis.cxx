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
    // Examples :
    OUT::m_lep_ph        = 0;
    OUT::m_lep_met_ph        = 0;
    OUT::dphi_lep_ph        = 0;
    OUT::dr_lep_ph        = 0;
    OUT::mt_lep_met      = 0;
    OUT::m_lep_met      = 0;
    OUT::pt_lep_met      = 0;
    OUT::dphi_lep_met      = 0;
    OUT::mt_lep_met_ph   = 0;
    OUT::mt_lep_met_ph_inv   = 0;
    OUT::RecoWMass       = 0;
    OUT::recoM_lep_nu_ph = 0;
    OUT::recoMet_eta= 0;
    OUT::recoW_pt= 0;
    OUT::recoW_eta= 0;
    OUT::recoW_phi= 0;
    OUT::nu_z_solution_success = 0;
    OUT::m_ll = 0;
    OUT::isBlinded = 0;

    // *************************
    // Declare Branches
    // *************************

    outtree->Branch("m_lep_ph"        , &OUT::m_lep_ph        , "m_lep_ph/F"  );
    outtree->Branch("m_lep_met_ph"        , &OUT::m_lep_met_ph        , "m_lep_met_ph/F"  );
    outtree->Branch("m_mt_lep_met_ph"        , &OUT::m_mt_lep_met_ph        , "m_mtlep_met_ph/F"  );
    outtree->Branch("m_mt_lep_met_ph_forcewmass"        , &OUT::m_mt_lep_met_ph_forcewmass        , "m_mt_lep_met_ph_forcewmass/F"  );
    outtree->Branch("mt_w"        , &OUT::mt_w        , "mt_w/F"  );
    outtree->Branch("mt_res"        , &OUT::mt_res        , "mt_res/F"  );
    outtree->Branch("mt_lep_ph"        , &OUT::mt_lep_ph        , "mt_lep_ph/F"  );
    outtree->Branch("dphi_lep_ph"        , &OUT::dphi_lep_ph        , "dphi_lep_ph/F"  );
    outtree->Branch("dr_lep_ph"        , &OUT::dr_lep_ph        , "dr_lep_ph/F"  );
    outtree->Branch("mt_lep_met"      , &OUT::mt_lep_met      , "mt_lep_met/F" );
    outtree->Branch("m_lep_met"       , &OUT::m_lep_met       , "m_lep_met/F" );
    outtree->Branch("pt_lep_met"      , &OUT::pt_lep_met      , "pt_lep_met/F" );
    outtree->Branch("dphi_lep_met"    , &OUT::dphi_lep_met    , "dphi_lep_met/F" );
    outtree->Branch("mt_lep_met_ph"   , &OUT::mt_lep_met_ph   , "mt_lep_met_ph/F");
    outtree->Branch("mt_lep_met_ph_inv"   , &OUT::mt_lep_met_ph_inv   , "mt_lep_met_ph_inv/F");
    outtree->Branch("RecoWMass"       , &OUT::RecoWMass       , "RecoWMass/F");
    outtree->Branch("recoM_lep_nu_ph" , &OUT::recoM_lep_nu_ph , "recoM_lep_nu_ph/F");
    outtree->Branch("recoMet_eta" , &OUT::recoMet_eta, "recoMet_eta/F");
    outtree->Branch("recoW_pt" , &OUT::recoW_pt, "recoW_pt/F");
    outtree->Branch("recoW_eta" , &OUT::recoW_eta, "recoW_eta/F");
    outtree->Branch("recoW_phi" , &OUT::recoW_phi, "recoW_phi/F");
    outtree->Branch("m_ll" , &OUT::m_ll, "m_ll/F");
    outtree->Branch("nu_z_solution_success" , &OUT::nu_z_solution_success, "nu_z_solution_success/O");

    outtree->Branch("leadjet_pt", &OUT::leadjet_pt, "leadjet_pt/F" );
    outtree->Branch("subljet_pt", &OUT::subljet_pt, "subljet_pt/F" );
    outtree->Branch("leaddijet_m", &OUT::leaddijet_m, "leaddijet_m/F" );
    outtree->Branch("leaddijet_pt", &OUT::leaddijet_pt, "leaddijet_pt/F" );
    outtree->Branch("massdijet_m", &OUT::massdijet_m, "massdijet_m/F" );
    outtree->Branch("massdijet_pt", &OUT::massdijet_pt, "massdijet_pt/F" );




    outtree->Branch("isBlinded" , &OUT::isBlinded, "isBlinded/O");

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

    _selectedMuons.clear();
    _selectedElectrons.clear();
    _selectedPhotons.clear();

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

    bool keep_evt = true;

    if( config.GetName() == "FilterMuon" ) {
        FilterMuon( config );
    }
    if( config.GetName() == "FilterElectron" ) {
        FilterElectron( config );
    }
    if( config.GetName() == "FilterPhoton" ) {
        FilterPhoton( config );
    }
    if( config.GetName() == "FilterJet" ) {
        FilterJet( config );
    }
    if( config.GetName() == "BuildEventVars" ) {
        BuildEventVars( config );
    }
    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }
    if( config.GetName() == "FilterBlind" ) {
        keep_evt &= FilterBlind( config );
    }

    return keep_evt;

}

void RunModule::FilterMuon( ModuleConfig & config ) {

    OUT::mu_n          = 0;
    ClearOutputPrefix("mu_");

    for( int idx = 0; idx < IN::mu_n; ++idx ) {

        //std::cout << "Muon pt = " << IN::mu_pt->at(idx) << std::endl;

        if( !config.PassFloat( "cut_pt", IN::mu_pt->at(idx) ) ) {
            //std::cout << "FAIL" << std::endl;
            continue;
        } 
       // else {
       //     std::cout << "PASS" << std::endl;
       // }
        if( !config.PassFloat( "cut_eta", fabs(IN::mu_eta->at(idx)) ) ) continue;
        if( !config.PassBool( "cut_tight", IN::mu_passTight->at(idx) ) ) continue;

        TLorentzVector mulv;
        mulv.SetPtEtaPhiE( IN::mu_pt->at(idx), 
                           IN::mu_eta->at(idx),
                           IN::mu_phi->at(idx),
                           IN::mu_e->at(idx)
                           );

        _selectedMuons.push_back( mulv );

        CopyPrefixIndexBranchesInToOut( "mu_", idx );
        OUT::mu_n++;

    }


}

void RunModule::FilterElectron( ModuleConfig & config ) {

    OUT::el_n          = 0;
    ClearOutputPrefix("el_");

    for( int idx = 0; idx < IN::el_n; ++idx ) {

        if( !config.PassFloat( "cut_pt", IN::el_pt->at(idx) ) ) continue;
        if( !config.PassFloat( "cut_eta", fabs(IN::el_eta->at(idx)) ) ) continue;
        if( !config.PassBool( "cut_tight", IN::el_passTight->at(idx) ) ) continue;

        TLorentzVector ellv;
        ellv.SetPtEtaPhiE( IN::el_pt->at(idx), 
                           IN::el_eta->at(idx),
                           IN::el_phi->at(idx),
                           IN::el_e->at(idx)
                           );

        float min_mu_dr = 100.0;
        for( unsigned muidx=0; muidx < _selectedMuons.size(); ++muidx ) {

            float dr = _selectedMuons[muidx].DeltaR( ellv );

            if( dr < min_mu_dr ) {
                min_mu_dr = dr;
            }
        }

        if( !config.PassFloat( "cut_muon_dr", min_mu_dr ) ) continue;

        _selectedElectrons.push_back( ellv );

        CopyPrefixIndexBranchesInToOut( "el_", idx );
        OUT::el_n++;

    }

}

void RunModule::FilterPhoton( ModuleConfig & config ) {

    OUT::ph_n          = 0;
    ClearOutputPrefix("ph_");

    for( int idx = 0; idx < IN::ph_n; ++idx ) {

        if( !config.PassFloat( "cut_pt", IN::ph_pt->at(idx) ) ) continue;
        if( !config.PassFloat( "cut_eta", fabs(IN::ph_eta->at(idx)) ) ) continue;
        if( !config.PassBool( "cut_loose", IN::ph_passLoose->at(idx) ) ) continue;
        if( !config.PassBool( "cut_medium", IN::ph_passMedium->at(idx) ) ) continue;
        if( !config.PassBool( "cut_tight", IN::ph_passTight->at(idx) ) ) continue;

        TLorentzVector phlv;
        phlv.SetPtEtaPhiE( IN::ph_pt->at(idx), 
                           IN::ph_eta->at(idx),
                           IN::ph_phi->at(idx),
                           IN::ph_e->at(idx) 
                           );

        float min_mu_dr = 100.0;
        for( unsigned muidx=0; muidx < _selectedMuons.size(); ++muidx ) {

            float dr = _selectedMuons[muidx].DeltaR( phlv );

            if( dr < min_mu_dr ) {
                min_mu_dr = dr;
            }
        }

        if( !config.PassFloat( "cut_muon_dr", min_mu_dr ) ) continue;

        float min_el_dr = 100.0;
        for( unsigned elidx=0; elidx < _selectedElectrons.size(); ++elidx ) {

            float dr = _selectedElectrons[elidx].DeltaR( phlv );

            if( dr < min_el_dr ) {
                min_el_dr = dr;
            }
        }

        if( !config.PassFloat( "cut_electron_dr", min_el_dr ) ) continue;


        _selectedPhotons.push_back( phlv );

        CopyPrefixIndexBranchesInToOut( "ph_", idx );
        OUT::ph_n++;

    }
}

void RunModule::FilterJet( ModuleConfig & config ) const {

    OUT::jet_n          = 0;
    ClearOutputPrefix("jet_");

    for( int idx = 0; idx < IN::jet_n; ++idx ) {

        TLorentzVector jetlv;
        jetlv.SetPtEtaPhiE( IN::jet_pt->at(idx), 
                            IN::jet_eta->at(idx),
                            IN::jet_phi->at(idx),
                            IN::jet_e->at(idx) 
                            );

        if( !config.PassFloat( "cut_pt", IN::jet_pt->at(idx) ) ) continue;

        float min_mu_dr = 100.0;
        for( unsigned muidx=0; muidx < _selectedMuons.size(); ++muidx ) {

            float dr = _selectedMuons[muidx].DeltaR( jetlv );

            if( dr < min_mu_dr ) {
                min_mu_dr = dr;
            }
        }

        if( !config.PassFloat( "cut_muon_dr", min_mu_dr ) ) continue;

        float min_el_dr = 100.0;
        for( unsigned elidx=0; elidx < _selectedElectrons.size(); ++elidx ) {

            float dr = _selectedElectrons[elidx].DeltaR( jetlv );

            if( dr < min_el_dr ) {
                min_el_dr = dr;
            }
        }

        if( !config.PassFloat( "cut_electron_dr", min_el_dr ) ) continue;

        float min_ph_dr = 100.0;
        for( unsigned phidx=0; phidx < _selectedPhotons.size(); ++phidx ) {

            float dr = _selectedPhotons[phidx].DeltaR( jetlv );

            if( dr < min_ph_dr ) {
                min_ph_dr = dr;
            }
        }

        if( !config.PassFloat( "cut_photon_dr", min_ph_dr ) ) continue;


        CopyPrefixIndexBranchesInToOut( "jet_", idx );
        OUT::jet_n++;

    }
}

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    int n_mu = 0;
    int n_mu_pt30 = 0;
    for( int midx = 0; midx < OUT::mu_n; ++midx ) {
        n_mu++;
        if( OUT::mu_pt->at(midx) > 30 ) {
            n_mu_pt30++;
        }
    }

    int n_el = 0;
    int n_el_pt30 = 0;
    for( int eidx = 0; eidx < OUT::el_n; ++eidx ) {
        n_el++;
        if( OUT::el_pt->at(eidx) > 30 ) {
            n_el_pt30++;
        }
    }


    if( !config.PassInt( "cut_el_n", n_el   ) ) keep_event=false;
    if( !config.PassInt( "cut_el_pt30_n", n_el_pt30   ) ) keep_event=false;
    if( !config.PassInt( "cut_mu_n", n_mu   ) ) keep_event=false;
    if( !config.PassInt( "cut_mu_pt30_n", n_mu_pt30   ) ) keep_event=false;
    if( !config.PassInt( "cut_ph_n", OUT::ph_n   ) ) keep_event=false;
    if( !config.PassInt( "cut_jet_n", OUT::jet_n ) ) keep_event=false;
    
    if( !config.PassBool( "cut_trig_Ele27_eta2p1_tight", IN::passTrig_HLT_Ele27_eta2p1_WPTight_Gsf) ) keep_event=false;
    if( !config.PassBool( "cut_trig_Mu27_IsoORIsoTk", (IN::passTrig_HLT_IsoMu27 | IN::passTrig_HLT_IsoTkMu27) ) ) keep_event=false;

    return keep_event;
    
}

void RunModule::BuildEventVars( ModuleConfig & config ) const {


    OUT::m_lep_ph = 0;
    OUT::m_lep_met_ph = 0;
    OUT::m_mt_lep_met_ph = 0;
    OUT::m_mt_lep_met_ph_forcewmass = 0;
    OUT::mt_w = 0;
    OUT::mt_res = 0;
    OUT::mt_lep_ph = 0;
    OUT::dphi_lep_ph = 0;
    OUT::dr_lep_ph = 0;
    OUT::m_lep_met = 0;
    OUT::mt_lep_met = 0;
    OUT::pt_lep_met = 0;
    OUT::dphi_lep_met = 0;
    OUT::mt_lep_met_ph = 0;
    OUT::mt_lep_met_ph_inv = 0;
    OUT::RecoWMass = 0;
    OUT::recoM_lep_nu_ph = 0;
    OUT::recoMet_eta= 0;
    OUT::recoW_pt= 0;
    OUT::recoW_eta= 0;
    OUT::recoW_phi= 0;
    OUT::m_ll = 0;

    OUT::leadjet_pt = 0;
    OUT::subljet_pt = 0;
    OUT::leaddijet_m = 0;
    OUT::leaddijet_pt = 0;
    OUT::massdijet_m = 0;
    OUT::massdijet_pt = 0;

    std::vector<TLorentzVector> leptons;
    std::vector<TLorentzVector> photons;

    for( int idx = 0; idx < OUT::mu_n; ++idx ) {
        TLorentzVector tlv;
        tlv.SetPtEtaPhiE( OUT::mu_pt->at(idx), 
                          OUT::mu_eta->at(idx), 
                          OUT::mu_phi->at(idx), 
                          OUT::mu_e->at(idx) );

        leptons.push_back(tlv);
    }

    for( int idx = 0; idx < OUT::el_n; ++idx ) {
        TLorentzVector tlv;
        tlv.SetPtEtaPhiE( OUT::el_pt->at(idx), 
                          OUT::el_eta->at(idx), 
                          OUT::el_phi->at(idx), 
                          OUT::el_e->at(idx) );

        leptons.push_back(tlv);
    }


    for( int idx = 0; idx < OUT::ph_n; ++idx ) {
        TLorentzVector tlv;
        tlv.SetPtEtaPhiE( OUT::ph_pt->at(idx), 
                          OUT::ph_eta->at(idx), 
                          OUT::ph_phi->at(idx), 
                          OUT::ph_e->at(idx) );

        photons.push_back(tlv);
    }

    TLorentzVector metlv;
    metlv.SetPtEtaPhiM( OUT::met_pt, 0.0, OUT::met_phi, 0.0 );
    TLorentzVector metlvOrig( metlv );

    if( leptons.size() > 0 ) {
        OUT::mt_lep_met = Utils::calc_mt( leptons[0], metlvOrig );
        OUT::m_lep_met = (leptons[0]+metlvOrig).M();
        OUT::pt_lep_met = (leptons[0]+metlvOrig).Pt();
        OUT::dphi_lep_met = leptons[0].DeltaPhi( metlvOrig );

        bool success = get_constriained_nu_pz( leptons[0], metlv );
        OUT::nu_z_solution_success = success;

        OUT::RecoWMass = ( leptons[0] + metlv ).M();

        if( leptons.size() > 1 ) {
            OUT::m_ll = (leptons[0] + leptons[1]).M();
        }

    }

    if( photons.size() > 0 ) {

        if( leptons.size() > 0 ) {

            OUT::m_lep_ph = ( leptons[0] + photons[0] ).M();
            OUT::m_lep_met_ph = ( leptons[0] + photons[0] + metlvOrig ).M();
            OUT::dphi_lep_ph = leptons[0].DeltaPhi(photons[0] );
            OUT::dr_lep_ph = leptons[0].DeltaR(photons[0] );
            OUT::recoM_lep_nu_ph = ( leptons[0] + metlv + photons[0] ).M();
            OUT::recoMet_eta = metlv.Eta() ;
            OUT::mt_lep_met_ph = Utils::calc_mt( leptons[0] + metlvOrig, photons[0]);
            OUT::mt_lep_met_ph_inv = Utils::calc_mt( leptons[0] + photons[0], metlvOrig);

            TLorentzVector recoW = leptons[0] + metlv;

            OUT::recoW_pt = recoW.Pt() ;
            OUT::recoW_eta = recoW.Eta() ;
            OUT::recoW_phi = recoW.Phi() ;

            float mt = Utils::calc_mt( leptons[0], metlvOrig );

            TLorentzVector wlv;
            wlv.SetXYZM( leptons[0].Px() + metlvOrig.Px(), leptons[0].Py() + metlvOrig.Py(), leptons[0].Pz(), mt );

            TLorentzVector wlv_force;
            wlv_force.SetXYZM( leptons[0].Px() + metlvOrig.Px(), leptons[0].Py() + metlvOrig.Py(), leptons[0].Pz(), _m_w );
            OUT::m_mt_lep_met_ph = ( wlv + photons[0] ).M();
            OUT::m_mt_lep_met_ph_forcewmass = ( wlv_force + photons[0] ).M();
            OUT::mt_w = mt;

            
            TLorentzVector lep_trans; 
            TLorentzVector ph_trans; 
            lep_trans.SetPtEtaPhiM( leptons[0].Pt(), 0.0, leptons[0].Phi(), leptons[0].M() );
            ph_trans.SetPtEtaPhiM( photons[0].Pt(), 0.0, photons[0].Phi(), photons[0].M() );

            OUT::mt_res = ( lep_trans + ph_trans + metlvOrig ).M();
            OUT::mt_lep_ph = ( lep_trans + ph_trans ).M();
            

        }
    }

    std::vector<std::pair<float, int> > sorted_jets;
    std::vector<TLorentzVector> jet_lvs;

    for( int jeti = 0; jeti < OUT::jet_n; ++jeti ) {
        sorted_jets.push_back( std::make_pair( OUT::jet_pt->at(jeti ), jeti ) );

        TLorentzVector lv;
        lv.SetPtEtaPhiE( OUT::jet_pt->at(jeti),
                        OUT::jet_eta->at(jeti),
                        OUT::jet_phi->at(jeti),
                        OUT::jet_e->at(jeti)
                );
        jet_lvs.push_back( lv );
    }


    std::sort(sorted_jets.rbegin(), sorted_jets.rend());

    if( OUT::jet_n > 0 ) {
        OUT::leadjet_pt = OUT::jet_pt->at(0);

        if( OUT::jet_n > 1 ) {
            OUT::leadjet_pt = OUT::jet_pt->at(sorted_jets[0].second);
            OUT::subljet_pt = OUT::jet_pt->at(sorted_jets[1].second);

            OUT::leaddijet_m  = (jet_lvs[sorted_jets[0].second]+jet_lvs[sorted_jets[1].second]).M();
            OUT::leaddijet_pt = (jet_lvs[sorted_jets[0].second]+jet_lvs[sorted_jets[1].second]).Pt();

            float min_mass = 100000000.;
            int min_idx1 = -1;
            int min_idx2 = -1;
            for( unsigned i = 0 ; i < jet_lvs.size(); ++i ) {
                for( unsigned j = i+1 ; j < jet_lvs.size(); ++j ) {

                    float mass = ( jet_lvs[i] + jet_lvs[j] ).M();
                    float diff = fabs( 91.2 - mass );

                    if( diff < min_mass ) {
                        min_mass = diff;
                        min_idx1 = i;
                        min_idx2 = j;
                    }
                }
            }

            OUT::massdijet_m  = ( jet_lvs[min_idx1] + jet_lvs[min_idx2] ).M();
            OUT::massdijet_pt = ( jet_lvs[min_idx1] + jet_lvs[min_idx2] ).Pt();
        }

    }

}

bool RunModule::FilterBlind( ModuleConfig & config ) const {

    bool keep_event = true;

    bool pass_blind = true;
    if( OUT::ph_n > 0 ) {
        if( !config.PassFloat( "cut_ph_pt_lead", OUT::ph_pt->at(0)) ) pass_blind=false;
    }
    if( !config.PassFloat( "cut_mt_lep_met_ph", OUT::mt_lep_met_ph) ) pass_blind=false;
    if( !config.PassFloat( "cut_mt_res", OUT::mt_res) ) pass_blind=false;

    if( OUT::jet_n > 1 ) {
        if( !config.PassFloat( "cut_abs_dijet_m_from_z", fabs(OUT::leaddijet_m-91.2)) ) pass_blind=false;
    }



    if( !pass_blind ) {
        OUT::isBlinded=true;
        if( OUT::EvtIsRealData ) keep_event=false;
    }
    else {
        OUT::isBlinded=false;
    }

    return keep_event;

}


bool RunModule::get_constriained_nu_pz( const TLorentzVector lepton, TLorentzVector &metlv ) const {

    float solved_pz = -1;

    bool desc_pos = calc_constrained_nu_momentum( lepton, metlv, solved_pz );
    if( desc_pos ) {
        metlv.SetXYZM( metlv.Px(), metlv.Py(), solved_pz, 0.0 );
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
        metlv_sol1.SetPtEtaPhiM( OUT::met_pt*scale1, 0.0, OUT::met_phi, 0.0 );
        metlv_sol2.SetPtEtaPhiM( OUT::met_pt*scale2, 0.0, OUT::met_phi, 0.0 );

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
    _isData = false;
}

