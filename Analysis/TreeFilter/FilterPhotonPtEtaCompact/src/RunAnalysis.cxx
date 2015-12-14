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
#include <boost/tokenizer.hpp>

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
    

    std::string ptbinsstr;
    std::string etabinsstr;

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        std::map<std::string, std::string>::const_iterator eitr;
        if( mod_conf.GetName() == "FilterPhoton" ) { 
            eitr = mod_conf.GetInitData().find( "ptbins" );
            if( eitr != mod_conf.GetInitData().end() ) {
                ptbinsstr = eitr->second();
            }
            eitr = mod_conf.GetInitData().find( "etabins" );
            if( eitr != mod_conf.GetInitData().end() ) {
                etabinsstr = eitr->second();
            }
        }
    }
    boost::char_separator<char> sep(",");
    boost::tokenizer< boost::char_separator<char> > ptbinstok(ptbinsstr, sep);
    boost::tokenizer< boost::char_separator<char> > etabinstok(etabinsstr, sep);

    BOOST_FOREACH (const std::string& t, ptbinstok) {
        int ptval;
        ptval << t;
        _ptbins.push_back(ptval);
    }
    BOOST_FOREACH (const std::string& t, etabinstok) {
        float etaval;
        etaval << t;
        _etabins.push_back(etaval);
    }

    for( int ptidx = 0; ptidx < _ptbins.size() - 1 ; ++ptidx ) {
        int ptmin = _ptbins[ptidx];
        int ptmax = _ptbins[ptidx+1];

        for( int etaidx = 0; etaidx < _etabins.size() - 1 ; ++etaidx ) {
            float etamin = _etabins[ptidx];
            float etamax = _etabins[ptidx+1];

            std::pair<int, int> ptpair = std::make_pair( ptmin, ptmax );
            std::pair<float, float> etapair = std::make_pair( etamin, etamax );

            std::pair< std::pair<int, int> , std::pair<float, float> > ptetapair = std::make_pair( ptpair, etapair );


            std::vector< std::pair< std::pair< std::pair<int, int>, std::pair< float, float > >, TTree * > >


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

// This is an example of a module that applies an
// event filter.  Note that it returns a bool instead
// of a void.  In principle the modules can return any
// type of variable, you just have to handle it
// in the ApplyModule function

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    #ifdef EXISTS_nPho
    int nPho = IN::nPho;
    if( !config.PassInt("cut_nPho", nPho ) ) keep_event = false;

    #endif
    return keep_event;
    
}

