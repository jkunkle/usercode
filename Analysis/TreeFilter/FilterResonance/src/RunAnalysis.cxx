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
    OUT::RecoWMass       = 0;
    OUT::recoM_lep_nu_ph = 0;
    OUT::nu_z_solution_success = 0;

    // *************************
    // Declare Branches
    // *************************

    outtree->Branch("m_lep_ph"        , &OUT::m_lep_ph        , "m_lep_ph/F"  );
    outtree->Branch("m_lep_met_ph"        , &OUT::m_lep_met_ph        , "m_lep_met_ph/F"  );
    outtree->Branch("m_mt_lep_met_ph"        , &OUT::m_mt_lep_met_ph        , "m_mtlep_met_ph/F"  );
    outtree->Branch("dphi_lep_ph"        , &OUT::dphi_lep_ph        , "dphi_lep_ph/F"  );
    outtree->Branch("dr_lep_ph"        , &OUT::dr_lep_ph        , "dr_lep_ph/F"  );
    outtree->Branch("mt_lep_met"      , &OUT::mt_lep_met      , "mt_lep_met/F" );
    outtree->Branch("m_lep_met"       , &OUT::m_lep_met       , "m_lep_met/F" );
    outtree->Branch("pt_lep_met"      , &OUT::pt_lep_met      , "pt_lep_met/F" );
    outtree->Branch("dphi_lep_met"    , &OUT::dphi_lep_met    , "dphi_lep_met/F" );
    outtree->Branch("mt_lep_met_ph"   , &OUT::mt_lep_met_ph   , "mt_lep_met_ph/F");
    outtree->Branch("RecoWMass"       , &OUT::RecoWMass       , "RecoWMass/F");
    outtree->Branch("recoM_lep_nu_ph" , &OUT::recoM_lep_nu_ph , "recoM_lep_nu_ph/F");
    outtree->Branch("nu_z_solution_success" , &OUT::nu_z_solution_success, "nu_z_solution_success/O");

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

    if( config.GetName() == "FilterMuon" ) {
        FilterMuon( config );
    }
    if( config.GetName() == "FilterElectron" ) {
        FilterElectron( config );
    }
    if( config.GetName() == "FilterPhoton" ) {
        FilterPhoton( config );
    }
    if( config.GetName() == "BuildEventVars" ) {
        BuildEventVars( config );
    }
    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }

    return keep_evt;

}

void RunModule::FilterMuon( ModuleConfig & config ) const {

    OUT::mu_n          = 0;
    ClearOutputPrefix("mu_");

    for( int idx = 0; idx < IN::mu_n; ++idx ) {

        if( !config.PassFloat( "cut_pt", IN::mu_pt->at(idx) ) ) continue;
        if( !config.PassFloat( "cut_eta", fabs(IN::mu_eta->at(idx)) ) ) continue;
        if( !config.PassBool( "cut_tight", IN::mu_passTight->at(idx) ) ) continue;

        CopyPrefixIndexBranchesInToOut( "mu_", idx );
        OUT::mu_n++;

    }


}

void RunModule::FilterElectron( ModuleConfig & config ) const {

    OUT::el_n          = 0;
    ClearOutputPrefix("el_");

    for( int idx = 0; idx < IN::el_n; ++idx ) {

        if( !config.PassFloat( "cut_pt", IN::el_pt->at(idx) ) ) continue;
        if( !config.PassFloat( "cut_eta", fabs(IN::el_eta->at(idx)) ) ) continue;
        if( !config.PassBool( "cut_tight", IN::el_passTight->at(idx) ) ) continue;

        CopyPrefixIndexBranchesInToOut( "el_", idx );
        OUT::el_n++;

    }


}

void RunModule::FilterPhoton( ModuleConfig & config ) const {

    OUT::ph_n          = 0;
    ClearOutputPrefix("ph_");

    for( int idx = 0; idx < IN::ph_n; ++idx ) {

        if( !config.PassFloat( "cut_pt", IN::ph_pt->at(idx) ) ) continue;
        if( !config.PassFloat( "cut_eta", fabs(IN::ph_eta->at(idx)) ) ) continue;
        if( !config.PassBool( "cut_loose", IN::ph_passLoose->at(idx) ) ) continue;
        if( !config.PassBool( "cut_medium", IN::ph_passMedium->at(idx) ) ) continue;
        if( !config.PassBool( "cut_tight", IN::ph_passTight->at(idx) ) ) continue;

        CopyPrefixIndexBranchesInToOut( "ph_", idx );
        OUT::ph_n++;

    }



}

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    if( !config.PassInt( "cut_el_n", OUT::el_n ) ) keep_event=false;
    if( !config.PassInt( "cut_mu_n", OUT::mu_n ) ) keep_event=false;
    if( !config.PassInt( "cut_ph_n", OUT::ph_n ) ) keep_event=false;

    return keep_event;
    
}

void RunModule::BuildEventVars( ModuleConfig & config ) const {


    OUT::m_lep_ph = 0;
    OUT::m_lep_met_ph = 0;
    OUT::m_mt_lep_met_ph = 0;
    OUT::dphi_lep_ph = 0;
    OUT::dr_lep_ph = 0;
    OUT::m_lep_met = 0;
    OUT::mt_lep_met = 0;
    OUT::pt_lep_met = 0;
    OUT::dphi_lep_met = 0;
    OUT::mt_lep_met_ph = 0;
    OUT::RecoWMass = 0;
    OUT::recoM_lep_nu_ph = 0;

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

    //for( int idx = 0; idx < OUT::el_n; ++idx ) {
    //    TLorentzVector tlv;
    //    tlv.SetPtEtaPhiE( OUT::el_pt->at(idx), 
    //                      OUT::el_eta->at(idx), 
    //                      OUT::el_phi->at(idx), 
    //                      OUT::el_e->at(idx) );

    //    leptons.push_back(tlv);
    //}


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

    }

    if( photons.size() > 0 ) {

        if( leptons.size() > 0 ) {

            OUT::m_lep_ph = ( leptons[0] + photons[0] ).M();
            OUT::m_lep_met_ph = ( leptons[0] + photons[0] + metlvOrig ).M();
            OUT::dphi_lep_ph = leptons[0].DeltaPhi(photons[0] );
            OUT::dr_lep_ph = leptons[0].DeltaR(photons[0] );
            OUT::recoM_lep_nu_ph = ( leptons[0] + metlv + photons[0] ).M();
            //OUT::mt_lep_met_ph = Utils::calc_mt( leptons[0] + metlvOrig, photons[0]);
            OUT::mt_lep_met_ph = Utils::calc_mt( leptons[0] + photons[0], metlvOrig);

            float mt = Utils::calc_mt( leptons[0], metlvOrig );

            TLorentzVector wlv;
            wlv.SetXYZM( leptons[0].Px() + metlvOrig.Px(), leptons[0].Py() + metlvOrig.Py(), leptons[0].Pz(), mt );

            OUT::m_mt_lep_met_ph = ( wlv + photons[0] ).M();

        }
    }
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
}

