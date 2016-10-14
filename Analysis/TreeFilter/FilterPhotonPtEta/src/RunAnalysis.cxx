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

    _n_saved = 0;

    _useCSEV = false;
    _usePSV  = true;
    _useNom = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
    
    
        std::map<std::string, std::string>::const_iterator eitr;
        if( mod_conf.GetName() == "FilterEvent" ) { 
            eitr = mod_conf.GetInitData().find( "eveto" );
            if( eitr != mod_conf.GetInitData().end() ) {
                if( eitr->second == "CSEV" ) {
                    _useCSEV = true;
                    _usePSV  = false;
                }
                else if( eitr->second == "PSV" ) {
                    _useCSEV = false;
                    _usePSV  = true;
                }
            }
            eitr = mod_conf.GetInitData().find( "type" );
            if( eitr != mod_conf.GetInitData().end() ) {
                if( eitr->second == "inv" ) {
                    _useNom  = false;
                }
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

    if( save_event ) _n_saved++;

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    // This bool is used for filtering
    // If a module implements an event filter
    // update this variable and return it
    // to apply the filter
    bool keep_evt = true;

    if( config.GetName() == "FilterPhoton" ) {
        FilterPhoton( config );
    }

    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }


    return keep_evt;

}

void RunModule::FilterPhoton( ModuleConfig & config ) const {

    OUT::ph_n = 0;
    ClearOutputPrefix("ph_");

    for( int idx=0; idx < IN::ph_n; ++idx ) {

        if( !config.PassBool( "cut_ph_CSEV", IN::ph_eleVeto->at(idx ) ) ) continue;
        if( !config.PassBool( "cut_ph_PSV", IN::ph_hasPixSeed->at(idx ) ) ) continue;

        CopyPrefixIndexBranchesInToOut( "ph_", idx );
        OUT::ph_n++;
    }
}

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    if( !config.PassInt("cut_save_max", _n_saved ) ) {
        return false;
    }

    //if( _useCSEV ) {
    //    if( _useNom ) {
    //        if( !config.PassInt("cut_Nph", OUT::ph_mediumPassCSEV_n ) ) keep_event = false;
    //        if( keep_event ) {
    //            if( !config.PassFloat("cut_ph_pt", OUT::ph_pt->at( OUT::ptSorted_ph_mediumPassCSEV_idx->at(0)) ) ) keep_event = false;
    //            if( !config.PassFloat("cut_abs_ph_eta", fabs( OUT::ph_eta->at(OUT::ptSorted_ph_mediumPassCSEV_idx->at(0)) ) ) ) keep_event = false;
    //        }
    //    }
    //    else {
    //        if( !config.PassInt("cut_Nph", OUT::ph_mediumFailCSEV_n ) ) keep_event = false;
    //        if( keep_event ) {
    //            if( !config.PassFloat("cut_ph_pt", OUT::ph_pt->at( OUT::ptSorted_ph_mediumFailCSEV_idx->at(0)) ) ) keep_event = false;
    //            if( !config.PassFloat("cut_abs_ph_eta", fabs( OUT::ph_eta->at(OUT::ptSorted_ph_mediumFailCSEV_idx->at(0)) ) ) ) keep_event = false;
    //        }
    //    }
    //}
    //else {
    //    if( _useNom ) {
    //        if( !config.PassInt("cut_Nph", OUT::ph_mediumPassPSV_n ) ) keep_event = false;
    //        if( keep_event ) {
    //            if( !config.PassFloat("cut_ph_pt", OUT::ph_pt->at( OUT::ptSorted_ph_mediumPassPSV_idx->at(0)) ) ) keep_event = false;
    //            if( !config.PassFloat("cut_abs_ph_eta", fabs( OUT::ph_eta->at(OUT::ptSorted_ph_mediumPassPSV_idx->at(0)) ) ) ) keep_event = false;
    //        }
    //    }
    //    else {
    //        if( !config.PassInt("cut_Nph", OUT::ph_mediumFailPSV_n ) ) keep_event = false;
    //        if( keep_event ) {
    //            if( !config.PassFloat("cut_ph_pt", OUT::ph_pt->at( OUT::ptSorted_ph_mediumFailPSV_idx->at(0)) ) ) keep_event = false;
    //            if( !config.PassFloat("cut_abs_ph_eta", fabs( OUT::ph_eta->at(OUT::ptSorted_ph_mediumFailPSV_idx->at(0)) ) ) ) keep_event = false;
    //        }
    //    }
    //}
    if( !config.PassInt("cut_Nph", OUT::ph_n ) ) keep_event = false;
    if( keep_event ) {
        if( !config.PassFloat("cut_ph_pt", OUT::ph_pt->at( 0) ) ) keep_event = false;
        if( !config.PassFloat("cut_abs_ph_eta", fabs( OUT::ph_eta->at(0) ) ) ) keep_event = false;
    }

    std::vector<TLorentzVector> trigele;
    for( int i = 0; i < OUT::el_n; ++i ) {
        TLorentzVector lv;
        lv.SetPtEtaPhiE(  OUT::el_pt->at(i),
                          OUT::el_eta->at(i),
                          OUT::el_phi->at(i),
                          OUT::el_e->at(i)
                        );
        if( lv.Pt() > 30 && OUT::el_triggerMatch->at(i) && OUT::el_passMvaTrig->at(i) ) {
            trigele.push_back(lv);
        }
    }


    std::vector<TLorentzVector> photons;
    for( int i = 0; i < OUT::ph_n; ++i ) {
        TLorentzVector lv;
        lv.SetPtEtaPhiE(  OUT::ph_pt->at(i),
                          OUT::ph_eta->at(i),
                          OUT::ph_phi->at(i),
                          OUT::ph_e->at(i)
                        );
        photons.push_back(lv);
    }

    //if( trigele.size() > 0 && photons.size() > 0 ) {
    //    OUT::m_trigelph1 = (trigele[0] + photons[0]).M();
    //}

    return keep_event;
    
}


