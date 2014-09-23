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

void RunModule::initialize( TChain * chain, TTree * _outtree, TFile *outfile,
                            const CmdOptions & _options, std::vector<ModuleConfig> & configs ) {

    // store tree for local use
    outtree = _outtree;
    options = _options;
    rfile = 0;
    rhist = 0;
    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    outtree->Branch("EventWeightElFF"  , &OUT::EventWeightElFF, "EventWeightElFF/F" );
    outtree->Branch("EventErrElFF"     , &OUT::EventErrElFF     , "EventErrElFF/F"    );
    outtree->Branch("HasElToPhFF"      , &OUT::HasElToPhFF      , "HasElToPhFF/O"     );

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        if( mod_conf.GetName() == "AddEventWeight" ) {

            std::map<std::string, std::string> data = mod_conf.GetInitData();

            std::string root_file;
            std::string hist_name_norm;
            std::string hist_name_pt;
            std::string hist_name_eta;
            std::string nconv;

            if( data.find( "root_file" ) != data.end() ) {
                std::string root_file = data["root_file"];
                rfile = TFile::Open( root_file.c_str() );
            }
            else {
                std::cout << "RunModule::AddEventWeight : ERROR - No root file was provided" << std::endl;
                return;
            }
            if( data.find( "hist_name" ) != data.end() ) {
                rhist = dynamic_cast<TH2F*>(rfile->Get(data["hist_name"].c_str()));
            }
        }
    }

}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    // Don't do this here
    //CopyInputVarsToOutput();

    // loop over configured modules
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {

        if( mod_conf.GetName() == "AddEventWeight" ) {
            AddEventWeight( mod_conf );
        }
    }

    // always return true -- save every event
    return true;

}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//
bool RunModule::AddEventWeight( ModuleConfig & config) {

    OUT::HasElToPhFF = false;

    //if( options.sample.empty() ) return true; 
    //// if the string is not empty, then try to match
    //    
    //// if no match, then return, otherwise get the histo
    //if( options.sample.find( sample_key ) == std::string::npos ) {
    //    return true;
    //}

    // Require one electron and two photons
    if( !config.PassInt( "cut_elpasstrig_n", IN::el_passtrig_n ) ) return false;
    if( !config.PassInt( "cut_el_n", IN::el_n ) ) return false;
    if( !config.PassInt( "cut_ph_n", IN::ph_n ) ) return false;
    if( !config.PassInt( "cut_ph_leadPixSeed", IN::ph_hasPixSeed->at(0) ) ) return false;
    if( !config.PassInt( "cut_ph_sublPixSeed", IN::ph_hasPixSeed->at(1) ) ) return false;

    // copy the event
    CopyInputVarsToOutput();

    if( IN::ph_hasPixSeed->at(0) == 1 && IN::ph_hasPixSeed->at(1)==0 ) {
        OUT::EventWeightElFF = rhist->GetBinContent( rhist->FindBin( IN::ph_pt->at(0), fabs(IN::ph_eta->at(0)) ) );
        OUT::EventErrElFF    = rhist->GetBinError(   rhist->FindBin( IN::ph_pt->at(0), fabs(IN::ph_eta->at(0)) ) );
        OUT::HasElToPhFF = true;
    }
       
    if( IN::ph_hasPixSeed->at(0) == 0 && IN::ph_hasPixSeed->at(1)== 1 ) {
        OUT::EventWeightElFF = rhist->GetBinContent( rhist->FindBin( IN::ph_pt->at(1), fabs(IN::ph_eta->at(1)) ) );
        OUT::EventErrElFF    = rhist->GetBinError(   rhist->FindBin( IN::ph_pt->at(1), fabs(IN::ph_eta->at(1)) ) );
        OUT::HasElToPhFF = true;
    }


    return true;
}


void RunModule::finalize() {

    if( rfile && rfile->IsOpen() ) {
        rfile->Close();
    }

}
