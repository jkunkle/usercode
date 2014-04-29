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

    outtree->Branch( "leadgenph_pt", &OUT::leadgenph_pt, "leadgenph_pt/F" );
    

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

    if( config.GetName() == "FilterTruePhoton" ) {
        keep_evt &= FilterTruePhoton( config );
    }

    return keep_evt;

}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************

bool RunModule::FilterTruePhoton( ModuleConfig & config ) const {

    bool keep_evt = true;

    float leadph_pt=0;
    bool found_ph = false;
    for( int i =0; i < IN::trueph_n; i++) {
        if( abs(IN::trueph_motherPID->at(i)) < 25 ) {
            found_ph=true;
            if( IN::trueph_pt->at(i) > leadph_pt ) {
                leadph_pt = IN::trueph_pt->at(i);
            }
        }
    }

    //for( int i =0; i < IN::nMC; i++) {
    //    if( IN::mcPID->at(i) == 22 && abs(IN::mcMomPID->at(i)) < 25 ) {
    //        found_ph=true;
    //        if( IN::mcPt->at(i) > leadph_pt ) {
    //            leadph_pt = IN::mcPt->at(i);
    //        }
    //    }
    //}

    OUT::leadgenph_pt = leadph_pt;

    if( !found_ph ) {
        keep_evt = false;
        //std::cout << "No true photon" << std::endl;
        ////for( int i =0; i < IN::nMC; i++) {
        ////    if( IN::mcPID->at(i) == 22 ) {
        ////        std::cout << "ph pt, mother " << IN::mcPt->at(i) << ", " << IN::mcMomPID->at(i) << std::endl;
        ////    }
        ////}
        //for( int i =0; i < IN::trueph_n; i++) {
        //    std::cout << "ph pt, mother " << IN::trueph_pt->at(i) << ", " << IN::trueph_motherPID->at(i) << std::endl;
        //}
    }
    else {
        if( !config.PassFloat("cut_leadph_pt", leadph_pt ) ){
            keep_evt = false;
        }
    }

    return keep_evt;
}




