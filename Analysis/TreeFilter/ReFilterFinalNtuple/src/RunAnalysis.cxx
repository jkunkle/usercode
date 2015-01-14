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

    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }
    if( config.GetName() == "FilterBlind" ) {
        keep_evt &= FilterBlind( config );
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

    for( int idx = 0; idx < IN::ph_n ; ++idx ) {

        if( !config.PassBool( "cut_ph_medium", IN::ph_passMedium->at(idx) ) ) continue;

        CopyPrefixIndexBranchesInToOut( "ph_", idx );
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

// This is an example of a module that applies an
// event filter.  Note that it returns a bool instead
// of a void.  In principle the modules can return any
// type of variable, you just have to handle it
// in the ApplyModule function

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    int nPh = OUT::ph_n;
    if( !config.PassInt("cut_nPh", nPh ) ) keep_event = false;

    if( OUT::ph_n > 1 ) {
        if( OUT::ph_pt->at(0) > OUT::ph_pt->at(1) ) {
            if( !config.PassBool( "cut_hasPixSeed_leadph12", OUT::ph_hasPixSeed->at(0) ) ) keep_event = false;
            if( !config.PassBool( "cut_hasPixSeed_sublph12", OUT::ph_hasPixSeed->at(1) ) ) keep_event = false;
            if( !config.PassBool( "cut_csev_leadph12", OUT::ph_eleVeto->at(0) ) ) keep_event = false;
            if( !config.PassBool( "cut_csev_sublph12", OUT::ph_eleVeto->at(1) ) ) keep_event = false;
        }
        else {
            if( !config.PassBool( "cut_hasPixSeed_leadph12", OUT::ph_hasPixSeed->at(1) ) ) keep_event = false;
            if( !config.PassBool( "cut_hasPixSeed_sublph12", OUT::ph_hasPixSeed->at(0) ) ) keep_event = false;
            if( !config.PassBool( "cut_csev_leadph12", OUT::ph_eleVeto->at(1) ) ) keep_event = false;
            if( !config.PassBool( "cut_csev_sublph12", OUT::ph_eleVeto->at(0) ) ) keep_event = false;
        }
    }

    return keep_event;
    
}

bool RunModule::FilterBlind( ModuleConfig & config ) const { 

    bool keep_event = true;

    bool pass_blind = true;
    if( !config.PassInt( "cut_nPhPassMedium", OUT::ph_medium_n ) ) pass_blind=false;
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


