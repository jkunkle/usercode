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
                            const CmdOptions & options, std::vector<ModuleConfig> &configs ) {

    // store the output tree locally
    outtree = _outtree;

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Set defaults for added output variables
    // *************************
    // Examples :
    OUT::muprobe_pt                               = 0; 
    OUT::muprobe_eta                              = 0; 
    OUT::muprobe_phi                              = 0; 
    OUT::muprobe_passTight                        = 0; 
    OUT::truemu_n                                 = 0; 
    OUT::truemu_pt                                = 0; 
    OUT::truemu_eta                               = 0; 
    OUT::truemu_phi                               = 0; 

    OUT::elprobe_pt                               = 0; 
    OUT::elprobe_eta                              = 0; 
    OUT::elprobe_phi                              = 0; 
    OUT::elprobe_passTight                        = 0; 
    OUT::elprobe_passMedium                       = 0; 
    OUT::elprobe_passLoose                        = 0; 
    OUT::trueel_n                                 = 0; 
    OUT::trueel_pt                                = 0; 
    OUT::trueel_eta                               = 0; 
    OUT::trueel_phi                               = 0; 

    OUT::phprobe_pt                               = 0; 
    OUT::phprobe_eta                              = 0; 
    OUT::phprobe_phi                              = 0; 
    OUT::phprobe_passTight                        = 0; 
    OUT::phprobe_passMedium                       = 0; 
    OUT::phprobe_passLoose                        = 0; 
    OUT::phprobe_eleVeto                          = 0; 
    OUT::phprobe_hasPixSeed                       = 0; 
    OUT::truephot_n                               = 0; 
    OUT::truephot_pt                              = 0; 
    OUT::truephot_eta                             = 0; 
    OUT::truephot_phi                             = 0; 

    OUT::hasTruthMatch                            = 0; 
    OUT::passTrig_IsoMu24                     = 0;
    OUT::passTrig_IsoTkMu24                   = 0;
    OUT::passTrig_Ele27_eta2p1_WPTight_Gsf    = 0;
    OUT::passTrig_Mu17_Photon30_CaloIdL_L1ISO = 0;
    OUT::recomet_pt                               = 0;
    OUT::truemet_pt                               = 0;

    // *************************
    // Declare Branches
    // *************************

    // Examples :
#ifdef MODULE_BuildMCMuon
    outtree->Branch("muprobe_pt"         , &OUT::muprobe_pt         , "muprobe_pt/F");
    outtree->Branch("muprobe_eta"        , &OUT::muprobe_eta        , "muprobe_eta/F");
    outtree->Branch("muprobe_phi"        , &OUT::muprobe_phi        , "muprobe_phi/F");
    outtree->Branch("muprobe_passTight"  , &OUT::muprobe_passTight  , "muprobe_passTight/O");
    outtree->Branch("truemu_n"         , &OUT::truemu_n         , "truemu_n/I");
    outtree->Branch("truemu_pt"         , &OUT::truemu_pt         , "truemu_pt/F");
    outtree->Branch("truemu_eta"        , &OUT::truemu_eta        , "truemu_eta/F");
    outtree->Branch("truemu_phi"        , &OUT::truemu_phi        , "truemu_phi/F");
#endif

#ifdef MODULE_BuildMCElectron
    outtree->Branch("elprobe_pt"         , &OUT::elprobe_pt         , "elprobe_pt/F");
    outtree->Branch("elprobe_eta"        , &OUT::elprobe_eta        , "elprobe_eta/F");
    outtree->Branch("elprobe_phi"        , &OUT::elprobe_phi        , "elprobe_phi/F");
    outtree->Branch("elprobe_passTight"  , &OUT::elprobe_passTight  , "elprobe_passTight/O");
    outtree->Branch("elprobe_passMedium"  , &OUT::elprobe_passMedium  , "elprobe_passMedium/O");
    outtree->Branch("elprobe_passLoose"  , &OUT::elprobe_passLoose  , "elprobe_passLoose/O");
    outtree->Branch("trueel_n"         , &OUT::trueel_n         , "trueel_n/I");
    outtree->Branch("trueel_pt"         , &OUT::trueel_pt         , "trueel_pt/F");
    outtree->Branch("trueel_eta"        , &OUT::trueel_eta        , "trueel_eta/F");
    outtree->Branch("trueel_phi"        , &OUT::trueel_phi        , "trueel_phi/F");

#endif

#ifdef MODULE_BuildMCPhoton
    outtree->Branch("phprobe_pt"         , &OUT::phprobe_pt         , "phprobe_pt/F");
    outtree->Branch("phprobe_eta"        , &OUT::phprobe_eta        , "phprobe_eta/F");
    outtree->Branch("phprobe_phi"        , &OUT::phprobe_phi        , "phprobe_phi/F");
    outtree->Branch("phprobe_passTight"  , &OUT::phprobe_passTight  , "phprobe_passTight/O");
    outtree->Branch("phprobe_passMedium"  , &OUT::phprobe_passMedium  , "phprobe_passMedium/O");
    outtree->Branch("phprobe_passLoose"  , &OUT::phprobe_passLoose  , "phprobe_passLoose/O");
    outtree->Branch("phprobe_eleVeto"  , &OUT::phprobe_eleVeto  , "phprobe_eleVeto/O");
    outtree->Branch("phprobe_hasPixSeed"  , &OUT::phprobe_hasPixSeed  , "phprobe_hasPixSeed/O");
    outtree->Branch("truephot_n"         , &OUT::truephot_n         , "truephot_n/I");
    outtree->Branch("truephot_pt"         , &OUT::truephot_pt         , "truephot_pt/F");
    outtree->Branch("truephot_eta"        , &OUT::truephot_eta        , "truephot_eta/F");
    outtree->Branch("truephot_phi"        , &OUT::truephot_phi        , "truephot_phi/F");

#endif
    outtree->Branch("hasTruthMatch"  , &OUT::hasTruthMatch, "hasTruthMatch/O");

    outtree->Branch("passTrig_IsoMu24"                     , &OUT::passTrig_IsoMu24, "passTrig_IsoMu24/O");
    outtree->Branch("passTrig_IsoTkMu24"                   , &OUT::passTrig_IsoTkMu24, "passTrig_IsoTkMu24/O");
    outtree->Branch("passTrig_Ele27_eta2p1_WPTight_Gsf"    , &OUT::passTrig_Ele27_eta2p1_WPTight_Gsf, "passTrig_Ele27_eta2p1_WPTight_Gsf/O");
    outtree->Branch("passTrig_Mu17_Photon30_CaloIdL_L1ISO" , &OUT::passTrig_Mu17_Photon30_CaloIdL_L1ISO, "passTrig_Mu17_Photon30_CaloIdL_L1ISO/O");
    outtree->Branch("recomet_pt"                               , &OUT::recomet_pt, "recomet_pt/F");
    outtree->Branch("truemet_pt"                               , &OUT::truemet_pt, "truemet_pt/F");

}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    CopyInputVarsToOutput();

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        if( mod_conf.GetName() == "FilterEvent" ) {
            save_event &= FilterEvent( mod_conf );
        }

    }

    if( save_event ) {
        BOOST_FOREACH( ModuleConfig & config, configs ) {
            if( config.GetName() == "BuildMCMuon" ) {
                BuildMCMuon( config );
            }
        }
        BOOST_FOREACH( ModuleConfig & config, configs ) {
            if( config.GetName() == "BuildMCElectron" ) {
                BuildMCElectron( config );
            }
        }
        BOOST_FOREACH( ModuleConfig & config, configs ) {
            if( config.GetName() == "BuildMCPhoton" ) {
                BuildMCPhoton( config );
            }
        }
    }

    return true;
    

}


// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//
bool RunModule::FilterEvent( ModuleConfig & config) const {

    bool keep_event = true;

    if( !config.PassBool( "cut_isWMuDecay", IN::isWMuDecay ) ) keep_event = false;
    if( !config.PassBool( "cut_isWElDecay", IN::isWElDecay ) ) keep_event = false;

    return keep_event;

}

void RunModule::BuildMCMuon( ModuleConfig & config ) const {

    bool has_truthmatch = false;
    for( int muidx=0; muidx < IN::mu_n; muidx++ ) {

        if( IN::mu_truthMatch_mu->at(muidx) ) {

            has_truthmatch = true;
         
            OUT::muprobe_pt  = IN::mu_pt->at(muidx);
            OUT::muprobe_eta = IN::mu_eta->at(muidx);
            OUT::muprobe_phi = IN::mu_phi->at(muidx);
            OUT::muprobe_passTight   = IN::mu_passTight->at(muidx);
        }
    }
    OUT::hasTruthMatch = has_truthmatch;

    std::vector<std::pair<float, int> > sorted_tmus;
    for( int tidx = 0; tidx < IN::truelep_n; ++tidx ) {

        if( abs(IN::truelep_Id->at(tidx) ) == 13 ) {

            sorted_tmus.push_back( std::make_pair( IN::truelep_pt->at(tidx ), tidx ) );
        }
    }

    std::sort( sorted_tmus.rbegin(), sorted_tmus.rend() );

    OUT::truemu_n = sorted_tmus.size();

    if( OUT::truemu_n > 0 ) {
        OUT::truemu_pt  = IN::truelep_pt ->at( sorted_tmus[0].second );
        OUT::truemu_eta = IN::truelep_eta->at( sorted_tmus[0].second );
        OUT::truemu_phi = IN::truelep_phi->at( sorted_tmus[0].second );
    }
       
    CalcCommonVars();
    outtree->Fill();

}

void RunModule::BuildMCElectron( ModuleConfig & config ) const {

    bool has_truthmatch = false;
    for( int elidx=0; elidx < IN::el_n; elidx++ ) {

        if( IN::el_truthMatch_el->at(elidx) ) {

            has_truthmatch = true;
         
            OUT::elprobe_pt  = IN::el_pt->at(elidx);
            OUT::elprobe_eta = IN::el_eta->at(elidx);
            OUT::elprobe_phi = IN::el_phi->at(elidx);
            OUT::elprobe_passTight   = IN::el_passTight->at(elidx);
            OUT::elprobe_passMedium   = IN::el_passMedium->at(elidx);
            OUT::elprobe_passLoose   = IN::el_passLoose->at(elidx);
        }
    }
    OUT::hasTruthMatch = has_truthmatch;

    std::vector<std::pair<float, int> > sorted_tels;
    for( int tidx = 0; tidx < IN::truelep_n; ++tidx ) {

        if( abs(IN::truelep_Id->at(tidx) ) == 11 ) {

            sorted_tels.push_back( std::make_pair( IN::truelep_pt->at(tidx ), tidx ) );
        }
    }

    std::sort( sorted_tels.rbegin(), sorted_tels.rend() );

    OUT::trueel_n = sorted_tels.size();

    if( OUT::trueel_n > 0 ) {
        OUT::trueel_pt  = IN::truelep_pt ->at( sorted_tels[0].second );
        OUT::trueel_eta = IN::truelep_eta->at( sorted_tels[0].second );
        OUT::trueel_phi = IN::truelep_phi->at( sorted_tels[0].second );
    }
       
    CalcCommonVars();
    outtree->Fill();

}

void RunModule::BuildMCPhoton( ModuleConfig & config ) const {

    bool has_truthmatch = false;
    for( int phidx=0; phidx < IN::ph_n; phidx++ ) {

        if( IN::ph_truthMatch_ph->at(phidx) ) {

            has_truthmatch = true;
         
            OUT::phprobe_pt  = IN::ph_pt->at(phidx);
            OUT::phprobe_eta = IN::ph_eta->at(phidx);
            OUT::phprobe_phi = IN::ph_phi->at(phidx);
            OUT::phprobe_passTight   = IN::ph_passTight->at(phidx);
            OUT::phprobe_passMedium   = IN::ph_passMedium->at(phidx);
            OUT::phprobe_passLoose   = IN::ph_passLoose->at(phidx);
            OUT::phprobe_eleVeto   = IN::ph_eleVeto->at(phidx);
            OUT::phprobe_hasPixSeed   = IN::ph_hasPixSeed->at(phidx);
        }
    }
    OUT::hasTruthMatch = has_truthmatch;

    std::vector<std::pair<float, int> > sorted_tphs;
    for( int tidx = 0; tidx < IN::trueph_n; ++tidx ) {

        sorted_tphs.push_back( std::make_pair( IN::trueph_pt->at(tidx ), tidx ) );
    }

    std::sort( sorted_tphs.rbegin(), sorted_tphs.rend() );

    OUT::truephot_n = sorted_tphs.size();

    if( OUT::truephot_n > 0 ) {
        OUT::truephot_pt  = IN::trueph_pt ->at( sorted_tphs[0].second );
        OUT::truephot_eta = IN::trueph_eta->at( sorted_tphs[0].second );
        OUT::truephot_phi = IN::trueph_phi->at( sorted_tphs[0].second );
    }

    CalcCommonVars();
       
    outtree->Fill();

}

void RunModule::CalcCommonVars( ) const {

    OUT::recomet_pt = IN::met_pt;

    OUT::passTrig_Mu17_Photon30_CaloIdL_L1ISO = IN::passTrig_HLT_Mu17_Photon30_CaloIdL_L1ISO;
    OUT::passTrig_Ele27_eta2p1_WPTight_Gsf    = IN::passTrig_HLT_Ele27_eta2p1_WPTight_Gsf;
    OUT::passTrig_Mu17_Photon30_CaloIdL_L1ISO = IN::passTrig_HLT_Mu17_Photon30_CaloIdL_L1ISO;
    OUT::passTrig_IsoMu24                     = IN::passTrig_HLT_IsoMu24;
    OUT::passTrig_IsoTkMu24                   = IN::passTrig_HLT_IsoTkMu24;

    TLorentzVector nusum;
    for( int lidx = 0 ; lidx < IN::truelep_n; ++lidx ){ 

        int pid = IN::truelep_Id->at(lidx);

        if( abs( pid) == 12 || abs(pid) == 14 || abs(pid) == 16 ) {

            TLorentzVector nulv;
            nulv.SetPtEtaPhiM( IN::truelep_pt->at(lidx),
                               IN::truelep_eta->at(lidx),
                               IN::truelep_phi->at(lidx),
                               0.0 
                               );

            nusum = nusum + nulv;
        }
    }

    OUT::truemet_pt = nusum.Pt();

}
