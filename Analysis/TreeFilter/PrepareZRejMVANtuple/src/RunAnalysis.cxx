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

    // *************************
    // Declare Branches
    // *************************
    outtree->Branch("m_lepphphMod", &OUT::m_lepphphMod, "m_lepphphMod/F" );
    outtree->Branch("m_lepph1Mod", &OUT::m_lepph1Mod, "m_lepph1Mod/F" );
    outtree->Branch("m_lepph2Mod", &OUT::m_lepph2Mod, "m_lepph2Mod/F" );
    outtree->Branch("m_lepph1Div", &OUT::m_lepph1Div, "m_lepph1Div/F" );
    outtree->Branch("m_lepph2Div", &OUT::m_lepph2Div, "m_lepph2Div/F" );
    outtree->Branch("mdiff_lepphph_lepph1", &OUT::mdiff_lepphph_lepph1, "mdiff_lepphph_lepph1/F" );

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        if( mod_conf.GetName() == "WeightEvent" ) { 
            std::map<std::string, std::string>::const_iterator citr = mod_conf.GetInitData().find( "Weight" );
            if( citr != mod_conf.GetInitData().end() ) {

                std::stringstream ss(citr->second);
                ss >> event_weight;
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
    // Example :

    // If the module applies a filter the filter decision
    // is passed back to here.  There is no requirement
    // that a function returns a bool, but
    // if you want the filter to work you need to do this
    //
    // Example :
    if( config.GetName() == "CalcVars" ) {
        CalcVars( config );
    }
    if( config.GetName() == "WeightEvent" ) {
        WeightEvent( config );
    }
    if( config.GetName() == "FilterPhoton" ) {
        FilterPhoton( config );
    }
    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
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

void RunModule::WeightEvent( ModuleConfig & config ) const {

    OUT::EventWeight *= event_weight;
}

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_evt = true;

    if( !config.PassInt( "cut_el_passtrig_n", OUT::el_passtrig_n ) ) keep_evt = false;
    if( !config.PassInt( "cut_el_n", OUT::el_n ) ) keep_evt = false;
    if( !config.PassInt( "cut_mu_n", OUT::mu_n ) ) keep_evt = false;
    if( !config.PassInt( "cut_ph_n", OUT::ph_n) ) keep_evt = false;
    if( !config.PassFloat( "cut_m_lepphph", OUT::m_lepphph) ) keep_evt = false;
    if( !config.PassFloat( "cut_m_lepph1", OUT::m_lepph1) ) keep_evt = false;
    if( !config.PassFloat( "cut_m_lepph2", OUT::m_lepph2) ) keep_evt = false;
    if( !config.PassFloat( "cut_ph_phDR", OUT::ph_phDR) ) keep_evt = false;
    if( !config.PassFloat( "cut_leadPhot_leadLepDR", OUT::leadPhot_leadLepDR) ) keep_evt = false;
    if( !config.PassFloat( "cut_sublPhot_leadLepDR", OUT::sublPhot_leadLepDR) ) keep_evt = false;

    int n_phPassEleVeto = 0;
    for( int idx = 0; idx < IN::ph_n; idx++ ) {
        if( OUT::ph_hasPixSeed->at(idx) == 0 ) n_phPassEleVeto++;
    }
    
    if( !config.PassInt( "cut_nPhPassEleVeto", n_phPassEleVeto) ) keep_evt = false;

    return keep_evt;
}

void RunModule::FilterPhoton( ModuleConfig & config ) const {

    OUT::ph_n = 0;
    ClearOutputPrefix("ph_");
    
    for( int idx = 0; idx < IN::ph_n; idx++ ) {

        if( !config.PassFloat( "cut_ph_pt", IN::ph_pt->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_medium", IN::ph_passMedium->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_eleVeto", IN::ph_eleVeto->at(idx)) ) continue;
        if( !config.PassBool( "cut_ph_hasPixSeed", IN::ph_hasPixSeed->at(idx)) ) continue;

        CopyPrefixIndexBranchesInToOut( "ph_", idx );
        
        OUT::ph_n++;
    }

}

void RunModule::CalcVars( ModuleConfig & config ) const {

    OUT::m_lepphphMod = OUT::m_lepphph-91.2;
    OUT::m_lepph1Mod  = OUT::m_lepph1-91.2;
    OUT::m_lepph2Mod  = OUT::m_lepph2-91.2;
    float minzdiff;
    if( fabs( OUT::m_lepph1Mod ) < fabs(OUT::m_lepph2Mod ) ) {
        minzdiff = OUT::m_lepph1Mod;
    }
    else {
        minzdiff = OUT::m_lepph2Mod;
    }
    OUT::m_minZdifflepph = minzdiff;
    OUT::mdiff_lepphph_lepph1 = OUT::m_lepphphMod-OUT::m_lepph1Mod;
    OUT::m_lepph1Div = OUT::m_lepph1/OUT::m_lepphph;
    OUT::m_lepph2Div = OUT::m_lepph2/OUT::m_lepphph;


}

RunModule::RunModule() : event_weight(1.0)
{
}

