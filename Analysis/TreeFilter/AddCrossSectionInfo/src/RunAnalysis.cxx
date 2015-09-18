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
    OUT::EffectiveLumi              = 0;

    // Examples :
    outtree->Branch("EffectiveLumi"             , &OUT::EffectiveLumi, "EffectiveLumi/F");

    _eff_lumi = -1.;

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {

        if( mod_conf.GetName() == "AddWeight" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "EffectiveLumi" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::cout << eitr->second << std::endl;
                _eff_lumi = atof( (eitr->second).c_str() );
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

    if( config.GetName() == "AddWeight" ) {
        AddWeight( config );
    }

    return true;

}

void RunModule::AddWeight( ModuleConfig & config ) const {

    //if( _eff_lumi < 0 ) {
    //    std::cout << "WARNING : Effecive luminosity was not set!" << std::endl;
    //}

    OUT::EffectiveLumi = _eff_lumi;

}


