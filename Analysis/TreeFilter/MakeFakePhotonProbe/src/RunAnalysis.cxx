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
    OUT::tagph_pt                     = 0;
    OUT::tagph_eta                    = 0;
    OUT::tagph_phi                    = 0;
    OUT::tagph_e                      = 0;
    OUT::tagph_sigmaIEIE              = 0;
    OUT::tagph_chHadIso               = 0;
    OUT::tagph_neuHadIso              = 0;
    OUT::tagph_phoIso                 = 0;
    OUT::tagph_IsEB                   = 0;
    OUT::tagph_IsEE                   = 0;
    OUT::tagph_passSIEIEMedium        = 0;
    OUT::tagph_passChIsoCorrMedium    = 0;
    OUT::tagph_passNeuIsoCorrMedium   = 0;
    OUT::tagph_passPhoIsoCorrMedium   = 0;
    OUT::tagph_truthMatch_ph          = 0;
    OUT::tagph_truthMatchMotherPID_ph = 0;
    OUT::tagph_truthMatch_el          = 0;

    OUT::tagll_mll          = 0;
    OUT::tagll_pt1          = 0;
    OUT::tagll_pt2          = 0;

    OUT::tagl_mt            = 0;
    OUT::tagl_pt1           = 0;
    OUT::tagl_met           = 0;

    OUT::probeph_n                    = 0;
    OUT::probeph_pt                   = 0;
    OUT::probeph_eta                  = 0;
    OUT::probeph_phi                  = 0;
    OUT::probeph_e                    = 0;
    OUT::probeph_sigmaIEIE            = 0;
    OUT::probeph_chHadIso             = 0;
    OUT::probeph_neuHadIso            = 0;
    OUT::probeph_phoIso               = 0;
    OUT::probeph_IsEB                 = 0;
    OUT::probeph_IsEE                 = 0;
    OUT::probeph_passSIEIEMedium      = 0;
    OUT::probeph_passChIsoCorrMedium  = 0;
    OUT::probeph_passNeuIsoCorrMedium = 0;
    OUT::probeph_passPhoIsoCorrMedium = 0;
    OUT::probeph_truthMatch_ph        = 0;
    OUT::probeph_truthMatchMotherPID_ph = 0;
    OUT::probeph_truthMatch_el        = 0;

    // *************************
    // Declare Branches
    // *************************

    // Examples :
    outtree->Branch("tagph_pt"                   , &OUT::tagph_pt                , "tagph_pt/F"                                   );
    outtree->Branch("tagph_eta"                  , &OUT::tagph_eta               , "tagph_eta/F"                                  );
    outtree->Branch("tagph_phi"                  , &OUT::tagph_phi               , "tagph_phi/F"                                  );
    outtree->Branch("tagph_e"                    , &OUT::tagph_e                 , "tagph_e/F"                                    );
    outtree->Branch("tagph_sigmaIEIE"            , &OUT::tagph_sigmaIEIE         , "tagph_sigmaIEIE/F"                            );
    outtree->Branch("tagph_chHadIso"             , &OUT::tagph_chHadIso          , "tagph_chHadIso/F"                             );
    outtree->Branch("tagph_neuHadIso"            , &OUT::tagph_neuHadIso         , "tagph_neuHadIso/F"                            );
    outtree->Branch("tagph_phoIso"               , &OUT::tagph_phoIso            , "tagph_phoIso/F"                               );
    outtree->Branch("tagph_IsEB"                 , &OUT::tagph_IsEB              , "tagph_IsEB/O"                               );
    outtree->Branch("tagph_IsEE"                 , &OUT::tagph_IsEE              , "tagph_IsEE/O"                               );
    outtree->Branch("tagph_passSIEIEMedium"      , &OUT::tagph_passSIEIEMedium   , "tagph_passSIEIEMedium/O");
    outtree->Branch("tagph_passChIsoCorrMedium"  , &OUT::tagph_passChIsoCorrMedium, "tagph_passChIsoCorrMedium/O");
    outtree->Branch("tagph_passNeuIsoCorrMedium" , &OUT::tagph_passNeuIsoCorrMedium, "tagph_passNeuIsoCorrMedium/O");
    outtree->Branch("tagph_passPhoIsoCorrMedium" , &OUT::tagph_passPhoIsoCorrMedium, "tagph_passPhoIsoCorrMedium/O");
    outtree->Branch("tagph_truthMatch_ph"        , &OUT::tagph_truthMatch_ph     , "tagph_truthMatch_ph/O");
    outtree->Branch("tagph_truthMatchMotherPID_ph" , &OUT::tagph_truthMatchMotherPID_ph        , "tagph_truthMatchMotherPID_ph/O");
    outtree->Branch("tagph_truthMatch_el"        , &OUT::tagph_truthMatch_el     , "tagph_truthMatch_el/O");

    outtree->Branch("tagll_mll"        , &OUT::tagll_mll, "tagll_mll/F");
    outtree->Branch("tagll_pt1"        , &OUT::tagll_pt1, "tagll_pt1/F");
    outtree->Branch("tagll_pt2"        , &OUT::tagll_pt2, "tagll_pt2/F");

    outtree->Branch("tagl_mt"        , &OUT::tagl_mt, "tagl_mt/F");
    outtree->Branch("tagl_pt1"        , &OUT::tagl_pt1, "tagl_pt1/F");
    outtree->Branch("tagl_met"        , &OUT::tagl_met, "tagl_met/F");


    outtree->Branch("probeph_pt"                   , &OUT::probeph_pt                   , "probeph_pt/F"                                   );
    outtree->Branch("probeph_eta"                  , &OUT::probeph_eta                  , "probeph_eta/F"                                  );
    outtree->Branch("probeph_phi"                  , &OUT::probeph_phi                  , "probeph_phi/F"                                  );
    outtree->Branch("probeph_e"                    , &OUT::probeph_e                    , "probeph_e/F"                                    );
    outtree->Branch("probeph_sigmaIEIE"            , &OUT::probeph_sigmaIEIE            , "probeph_sigmaIEIE/F"                            );
    outtree->Branch("probeph_chHadIso"             , &OUT::probeph_chHadIso             , "probeph_chHadIso/F"                             );
    outtree->Branch("probeph_neuHadIso"            , &OUT::probeph_neuHadIso            , "probeph_neuHadIso/F"                            );
    outtree->Branch("probeph_phoIso"               , &OUT::probeph_phoIso               , "probeph_phoIso/F"                               );
    outtree->Branch("probeph_IsEB"                 , &OUT::probeph_IsEB                 , "probeph_IsEB/O"                               );
    outtree->Branch("probeph_IsEE"                 , &OUT::probeph_IsEE                 , "probeph_IsEE/O"                               );
    outtree->Branch("probeph_passSIEIEMedium"      , &OUT::probeph_passSIEIEMedium      , "probeph_passSIEIEMedium/O");
    outtree->Branch("probeph_passChIsoCorrMedium"  , &OUT::probeph_passChIsoCorrMedium  , "probeph_passChIsoCorrMedium/O");
    outtree->Branch("probeph_passNeuIsoCorrMedium" , &OUT::probeph_passNeuIsoCorrMedium , "probeph_passNeuIsoCorrMedium/O");
    outtree->Branch("probeph_passPhoIsoCorrMedium" , &OUT::probeph_passPhoIsoCorrMedium , "probeph_passPhoIsoCorrMedium/O");
    outtree->Branch("probeph_truthMatch_ph"        , &OUT::probeph_truthMatch_ph        , "probeph_truthMatch_ph/O");
    outtree->Branch("probeph_truthMatchMotherPID_ph" , &OUT::probeph_truthMatchMotherPID_ph        , "probeph_truthMatchMotherPID_ph/O");
    outtree->Branch("probeph_truthMatch_el"        , &OUT::probeph_truthMatch_el        , "probeph_truthMatch_el/O");

}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // first run the event filter
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        if( mod_conf.GetName() == "FilterEvent" ) {
            save_event &= FilterEvent( mod_conf );
        }
    }

    // if the event passes the filter, run the ntuple making
    if( save_event ) {
        BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
            if( mod_conf.GetName() == "MakeGJNtuple" ) {
                MakeGJNtuple( mod_conf );
            }
            if( mod_conf.GetName() == "MakeZmumuNtuple" ) {
                MakeZmumuNtuple( mod_conf );
            }
            if( mod_conf.GetName() == "MakeWmunuNtuple" ) {
                MakeWmunuNtuple( mod_conf );
            }
        }
    }

    // always return true, but supply --disableOutputTree
    // This will count every input event so that
    // we know we ran over all input events
    return true;
}

void RunModule::MakeGJNtuple( ModuleConfig & config ) const {

    // first find the tag index
    std::vector<int> tag_indices;
    for( int i = 0 ; i < IN::ph_n; ++i) {
        if( IN::ph_passMedium->at(i) ) {
            tag_indices.push_back( i );
        }
    }

    BOOST_FOREACH( int tagidx, tag_indices ) {

        OUT::tagph_pt = IN::ph_pt->at(tagidx);
        OUT::tagph_eta = IN::ph_eta->at(tagidx);
        OUT::tagph_phi = IN::ph_phi->at(tagidx);
        OUT::tagph_e = IN::ph_e->at(tagidx);

        OUT::tagph_sigmaIEIE = IN::ph_sigmaIEIE->at(tagidx);
        OUT::tagph_chHadIso = IN::ph_chIsoCorr->at(tagidx);
        OUT::tagph_neuHadIso = IN::ph_neuIsoCorr->at(tagidx);
        OUT::tagph_phoIso = IN::ph_phoIsoCorr->at(tagidx);

        OUT::tagph_IsEB = IN::ph_IsEB->at(tagidx);
        OUT::tagph_IsEE = IN::ph_IsEE->at(tagidx);

        OUT::tagph_passSIEIEMedium = IN::ph_passSIEIEMedium->at(tagidx);
        OUT::tagph_passChIsoCorrMedium = IN::ph_passChIsoCorrMedium->at(tagidx);
        OUT::tagph_passNeuIsoCorrMedium = IN::ph_passNeuIsoCorrMedium->at(tagidx);
        OUT::tagph_passPhoIsoCorrMedium = IN::ph_passPhoIsoCorrMedium->at(tagidx);

        OUT::tagph_truthMatch_ph = IN::ph_truthMatch_ph->at(tagidx);
        OUT::tagph_truthMatch_el = IN::ph_truthMatch_el->at(tagidx);

        for( int probeidx = 0 ; probeidx < IN::ph_n; ++probeidx) {

            if ( probeidx == tagidx ) continue;

            FillProbe( probeidx );

            CopyInputVarsToOutput();
            outtree->Fill();

        }
    }
}

void RunModule::MakeZmumuNtuple( ModuleConfig & config ) const {

        
    if( IN::mu_n>1 ) { 
        OUT::tagll_mll = IN::m_mumu;
        OUT::tagll_pt1 = IN::mu_pt->at(0);
        OUT::tagll_pt2 = IN::mu_pt->at(1);

        for( int idx = 0; idx < IN::ph_n; ++idx) {
            FillProbe( idx );
            CopyInputVarsToOutput();
            outtree->Fill();
        }
    }
        
}


void RunModule::MakeWmunuNtuple( ModuleConfig & config ) const {
        
    if( IN::mu_n>1 ) { 
        OUT::tagl_mt  = IN::mt_lep_met;
        OUT::tagl_pt1 = IN::mu_pt->at(0);
        OUT::tagl_met = IN::METPt->at(0);

        for( int idx = 0; idx < IN::ph_n; ++idx) {
            FillProbe( idx );
            CopyInputVarsToOutput();
            outtree->Fill();
        }
    }
        
}


void RunModule::MakeQCDNtuple( ModuleConfig & config ) const {
        
    for( int idx = 0; idx < IN::ph_n; ++idx) {
        FillProbe( idx );
        CopyInputVarsToOutput();
        outtree->Fill();
    }
        
}


void RunModule::FillProbe( int probeidx ) const {

    OUT::probeph_pt = IN::ph_pt->at(probeidx);
    OUT::probeph_eta = IN::ph_eta->at(probeidx);
    OUT::probeph_phi = IN::ph_phi->at(probeidx);
    OUT::probeph_e = IN::ph_e->at(probeidx);

    OUT::probeph_sigmaIEIE = IN::ph_sigmaIEIE->at(probeidx);
    OUT::probeph_chHadIso = IN::ph_chIsoCorr->at(probeidx);
    OUT::probeph_neuHadIso = IN::ph_neuIsoCorr->at(probeidx);
    OUT::probeph_phoIso = IN::ph_phoIsoCorr->at(probeidx);

    OUT::probeph_IsEB = IN::ph_IsEB->at(probeidx);
    OUT::probeph_IsEE = IN::ph_IsEE->at(probeidx);

    OUT::probeph_passSIEIEMedium = IN::ph_passSIEIEMedium->at(probeidx);
    OUT::probeph_passChIsoCorrMedium = IN::ph_passChIsoCorrMedium->at(probeidx);
    OUT::probeph_passNeuIsoCorrMedium = IN::ph_passNeuIsoCorrMedium->at(probeidx);
    OUT::probeph_passPhoIsoCorrMedium = IN::ph_passPhoIsoCorrMedium->at(probeidx);

    OUT::probeph_truthMatch_ph = IN::ph_truthMatch_ph->at(probeidx);
    OUT::probeph_truthMatchMotherPID_ph = IN::ph_truthMatchMotherPID_ph->at(probeidx);
    OUT::probeph_truthMatch_el = IN::ph_truthMatch_el->at(probeidx);
}
        



bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    int ph_medium_n = 0;

    for( int i = 0 ; i < IN::ph_n; ++i) {
        if( IN::ph_passMedium->at(i) ) {
            ph_medium_n++;
        }
    }
    if( !config.PassInt("cut_ph_medium_n", ph_medium_n) ) keep_event = false;
    if( !config.PassInt("cut_ph_n", IN::ph_n) ) keep_event = false;
    if( !config.PassInt("cut_mu_n", IN::mu_n) ) keep_event = false;
    if( !config.PassInt("cut_el_n", IN::el_n) ) keep_event = false;

    return keep_event;
    
}


