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
    OUT::el_SF_trig           = 0;
    OUT::el_SF_id             = 0;
    OUT::mu_SF_trig           = 0;
    OUT::mu_SF_id             = 0;
    OUT::mu_SF_iso            = 0;
    OUT::ph_SF_id             = 0;
    OUT::ph_SF_eveto          = 0;

    // *************************
    // Declare Branches
    // *************************

    // Examples :
    outtree->Branch("ph_n"             , &OUT::ph_n                                      );

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {

        if( mod_conf.GetName() == "AddMuonSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;

            itr = mod_conf.GetInitData().find( "FilePathIso" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_iso = ROOT::TFile::Open( (itr->second).c_str(), "READ" );
                _sfgraph_mu_iso_barrel  = _sffile_mu_iso->Get( "DATA_over_MC_combRelIsoPF04dBeta<02_Tight_pt_abseta<0.9" );
                _sfgraph_mu_iso_trans   = _sffile_mu_iso->Get( "DATA_over_MC_combRelIsoPF04dBeta<02_Tight_pt_abseta0.9-1.2" );
                _sfgraph_mu_iso_endcap1 = _sffile_mu_iso->Get( "DATA_over_MC_combRelIsoPF04dBeta<02_Tight_pt_abseta1.2-2.1" );
                _sfgraph_mu_iso_endcap2 = _sffile_mu_iso->Get( "DATA_over_MC_combRelIsoPF04dBeta<02_Tight_pt_abseta2.1-2.4" );
            }
            itr = mod_conf.GetInitData().find( "FilePathId" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_id = ROOT::TFile::Open( (itr->second).c_str(), "READ" );
                _sfgraph_mu_id_barrel  = _sffile_mu_id->Get( "DATA_over_MC_Tight_pt_abseta<0.9" );
                _sfgraph_mu_id_trans   = _sffile_mu_id->Get( "DATA_over_MC_Tight_pt_abseta0.9-1.2" );
                _sfgraph_mu_id_endcap1 = _sffile_mu_id->Get( "DATA_over_MC_Tight_pt_abseta1.2-2.1" );
                _sfgraph_mu_id_endcap2 = _sffile_mu_id->Get( "DATA_over_MC_Tight_pt_abseta2.1-2.4" );
            }
            itr = mod_conf.GetInitData().find( "FilePathTrig" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_trig = ROOT::TFile::Open( (itr->second).c_str(), "READ" );
                _sfgraph_mu_trig_barrel = _sffile_mu_trig->Get( "IsoMu24_eta2p1_DATA_over_MC_TightID_IsodB_PT_ABSETA_Barrel_0to0p9_pt25-500_2012ABCD" );
                _sfgraph_mu_trig_trans  = _sffile_mu_trig->Get( "IsoMu24_eta2p1_DATA_over_MC_TightID_IsodB_PT_ABSETA_Transition_0p9to1p2_pt25-500_2012ABCD" );
                _sfgraph_mu_trig_endcap = _sffile_mu_trig->Get( "IsoMu24_eta2p1_DATA_over_MC_TightID_IsodB_PT_ABSETA_Endcaps_1p2to2p1_pt25-500_2012ABCD" );
            }
        }
        if( mod_conf.GetName() == "AddElectronSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "HistPathId" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_el_id = ROOT::TFile::Open( (itr->second).c_str(), "READ" );
            }
            itr = mod_conf.GetInitData().find( "HistPathTrig" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_el_trig = ROOT::TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_el_trig = _sffile_el_trig->Get( "electronsDATAMCratio_FO_ID_ISO" )
            }
        }
        if( mod_conf.GetName() == "AddPhotonSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "HistPathId" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_id = ROOT::TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_ph_id = _sffile_el_trig->Get( "PhotonIDSF_MediumWP_Jan22rereco_Full2012_S10_MC_V01" )
            }
            itr = mod_conf.GetInitData().find( "HistPathEveto" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_eveto = ROOT::TFile::Open( (itr->second).c_str(), "READ" );
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

    if( config.GetName() == "AddElectronSF" ) {
        AddElectronDF( config );
    }
    if( config.GetName() == "AddMuonSF" ) {
        AddElectronDF( config );
    }
    if( config.GetName() == "AddPhotonSF" ) {
        AddElectronDF( config );
    }

    return keep_evt;

}

void RunModule::AddElectronSF( ModuleConfig & /*config*/ ) const {

    OUT::el_trigSF  = 0;
    OUT::el_idSF    = 0;

    for( int idx = 0; idx < OUT::el_n; ++idx ) {

        if( OUT::el_triggerMatch->at(idx) && OUT::el_passMVATrig->at(idx) ) {

            float pt = el_pt->at(idx);
            float eta = fabs( el_eta->at(idx) );
            // histogram ends at 200, if pT is above
            // 200, get the value just below
            if( pt < 200 ) {
                OUT::el_trigSF = _sfhist_el_trig->GetBinContent( _sfhist_el_trig->FindBin( eta, pt ) );
                OUT::el_trigSF = _sfhist_el_trig->GetBinContent( _sfhist_el_trig->FindBin( eta, pt ) );
            }
            else {
                OUT::el_trigSF = _sfhist_el_trig->GetBinContent( _sfhist_el_trig->FindBin( eta, 199. ) );
                OUT::el_trigSF = _sfhist_el_trig->GetBinContent( _sfhist_el_trig->FindBin( eta, 199. ) );
            }

        }
    }


}

void RunModule::AddMuonSF( ModuleConfig & /*config*/ ) const { 

    OUT::mu_trigSF = 0;
    OUT::mu_IdSF   = 0;
    OUT::mu_IsoSF  = 0;

    for( int idx = 0; idx < OUT::mu_n; ++idx ) {
        if( OUT::mu_triggerMatch->at(idx) ) {
            OUT::mu_trigSF = _sfhist_mu_



        

