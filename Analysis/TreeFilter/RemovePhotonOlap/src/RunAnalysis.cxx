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

    if( config.GetName() == "RemoveOlap" ) {
        RemoveOlap( config );
    }
    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }

    return keep_evt;

}

void RunModule::RemoveOlap( ModuleConfig & config) const {

    OUT::ph_n = 0;
    ClearOutputPrefix("ph_");
    for( int idx = 0; idx < IN::ph_n; idx++ ) {

        // electron overlap removal
        TLorentzVector phlv;
        phlv.SetPtEtaPhiE( IN::ph_pt->at(idx), 
                           IN::ph_eta->at(idx), 
                           IN::ph_phi->at(idx), 
                           IN::ph_e->at(idx) );

        float min_el_dr = 100.0;
        float min_trigel_dr = 100.0;
        bool found_trigel = false;

        for( int eidx = 0; eidx < IN::el_n; eidx++ ) {
            TLorentzVector ellv;
            ellv.SetPtEtaPhiE( IN::el_pt->at(eidx), 
                               IN::el_eta->at(eidx), 
                               IN::el_phi->at(eidx), 
                               IN::el_e->at(eidx) );

            float dr = phlv.DeltaR( ellv );
            if( dr < min_el_dr ) {
                min_el_dr = dr;
            }

            // count the leading trigger
            // matched electron which
            // will be the first in the list
            if( IN::el_triggerMatch->at(eidx) && IN::el_passMvaTrig->at(eidx) && ellv.Pt() > 30 && dr < min_trigel_dr ) {
                if( !found_trigel ) {
                    min_trigel_dr = dr;
                    found_trigel = true;
                }
            }
        }

        if( !config.PassFloat( "cut_el_ph_dr"    , min_el_dr    ) ) continue;
        if( !config.PassFloat( "cut_trigel_ph_dr", min_trigel_dr) ) continue;

        CopyPrefixIndexBranchesInToOut( "ph_", idx );
        OUT::ph_n++;

    }

}

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    if( !config.PassInt( "cut_n_ph", OUT::ph_n ) ) {
        keep_event = false;
    }

    return keep_event;
    
}

