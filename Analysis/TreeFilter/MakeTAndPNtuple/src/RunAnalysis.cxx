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
                            const CmdOptions & options, std::vector<ModuleConfig> & configs ) {

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

    // *************************
    // Declare Branches
    // *************************
    //

    outtree->Branch("PUWeight"         , &OUT::PUWeight         , "PUWeight/F" );
    outtree->Branch("event"            , &OUT::event            , "event/I" );
    outtree->Branch("run"              , &OUT::run              , "run/I" );

    outtree->Branch("tag_pt"           , &OUT::tag_pt           , "tag_pt/F" );
    outtree->Branch("tag_eta"          , &OUT::tag_eta          , "tag_eta/F");
    outtree->Branch("tag_eta_sc"       , &OUT::tag_eta_sc       , "tag_eta_sc/F");
    outtree->Branch("tag_phi"          , &OUT::tag_phi          , "tag_phi/F");
    outtree->Branch("probe_pt"         , &OUT::probe_pt         , "probe_pt/F");
    outtree->Branch("probe_eta"        , &OUT::probe_eta        , "probe_eta/F");
    outtree->Branch("probe_eta_sc"     , &OUT::probe_eta_sc     , "probe_eta_sc/F");
    outtree->Branch("probe_phi"        , &OUT::probe_phi        , "probe_phi/F");
    outtree->Branch("probe_isPhoton"   , &OUT::probe_isPhoton   , "probe_isPhoton/O");
    outtree->Branch("probe_nConvTrk"   , &OUT::probe_nConvTrk   , "probe_nConvTrk/O");
    outtree->Branch("probe_passtrig"   , &OUT::probe_passtrig   , "probe_passtrig/O");
    outtree->Branch("m_tagprobe"       , &OUT::m_tagprobe       , "m_tagprobe/F");
    outtree->Branch("dr_tagprobe"      , &OUT::dr_tagprobe      , "dr_tagprobe/F");
    outtree->Branch("m_tagprobe_sceta" , &OUT::m_tagprobe_sceta , "m_tagprobe_sceta/F");

    outtree->Branch("mutag_pt"           , &OUT::mutag_pt           , "mutag_pt/F" );
    outtree->Branch("mutag_eta"          , &OUT::mutag_eta          , "mutag_eta/F");
    outtree->Branch("mutag_phi"          , &OUT::mutag_phi          , "mutag_phi/F");
    outtree->Branch("muprobe_pt"         , &OUT::muprobe_pt         , "muprobe_pt/F");
    outtree->Branch("muprobe_eta"        , &OUT::muprobe_eta        , "muprobe_eta/F");
    outtree->Branch("muprobe_phi"        , &OUT::muprobe_phi        , "muprobe_phi/F");
    outtree->Branch("muprobe_passTight"  , &OUT::muprobe_passTight  , "muprobe_passTight/O");
    outtree->Branch("muprobe_triggerMatch"  , &OUT::muprobe_triggerMatch, "muprobe_triggerMatch/O");
    outtree->Branch("m_mutagprobe"       , &OUT::m_mutagprobe       , "m_mutagprobe/F");
    outtree->Branch("dr_mutagprobe"      , &OUT::dr_mutagprobe      , "dr_mutagprobe/F");

    outtree->Branch("eltag_pt"           , &OUT::eltag_pt           , "eltag_pt/F" );
    outtree->Branch("eltag_eta"          , &OUT::eltag_eta          , "eltag_eta/F");
    outtree->Branch("eltag_phi"          , &OUT::eltag_phi          , "eltag_phi/F");
    outtree->Branch("elprobe_pt"         , &OUT::elprobe_pt         , "elprobe_pt/F");
    outtree->Branch("elprobe_eta"        , &OUT::elprobe_eta        , "elprobe_eta/F");
    outtree->Branch("elprobe_phi"        , &OUT::elprobe_phi        , "elprobe_phi/F");
    outtree->Branch("elprobe_matchElDR"  , &OUT::elprobe_matchElDR  , "elprobe_matchElDR/F");
    outtree->Branch("elprobe_isPh"       , &OUT::elprobe_isPh       , "elprobe_isPh/O");
    outtree->Branch("elprobe_isEl"       , &OUT::elprobe_isEl       , "elprobe_isEl/O");
    outtree->Branch("elprobe_passMVATrig"  , &OUT::elprobe_passMVATrig, "elprobe_passMVATrig/O");
    outtree->Branch("elprobe_passMVANonTrig"  , &OUT::elprobe_passMVANonTrig, "elprobe_passMVANonTrig/O");
    outtree->Branch("elprobe_triggerMatch"  , &OUT::elprobe_triggerMatch, "elprobe_triggerMatch/O");
    outtree->Branch("m_eltagprobe"       , &OUT::m_eltagprobe       , "m_eltagprobe/F");
    outtree->Branch("dr_eltagprobe"      , &OUT::dr_eltagprobe      , "dr_eltagprobe/F");


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
            if( mod_conf.GetName() == "MakeNtuple" ) {
                MakeNtuple( mod_conf );
            }
            if( mod_conf.GetName() == "MakeGGNtuple" ) {
                MakeGGNtuple( mod_conf );
            }
            if( mod_conf.GetName() == "MakeMuMuNtuple" ) {
                MakeMuMuNtuple( mod_conf );
            }
            if( mod_conf.GetName() == "MakeEENtuple" ) {
                MakeEENtuple( mod_conf );
            }
        }
    }

    // always return true, but supply --disableOutputTree
    // This will count every input event so that
    // we know we ran over all input events
    return true;
    
}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//

void RunModule::MakeNtuple( ModuleConfig & config ) const {


    // collect objects
    std::vector< TLorentzVector> objects;
    std::vector< TLorentzVector> objects_sceta;
    std::vector<bool> obj_isElec;
    std::vector<int> obj_index;
    for( int eidx = 0; eidx < IN::el_n; ++eidx ) {
        TLorentzVector ellv;
        ellv.SetPtEtaPhiE( IN::el_pt->at(eidx),
                           IN::el_eta->at(eidx),
                           IN::el_phi->at(eidx),
                           IN::el_e->at(eidx)    );
        objects.push_back( ellv );
        //ellv.SetPtEtaPhiE( ellv.Pt(), IN::el_sceta->at(eidx), ellv.Phi(), ellv.E() );
        //objects_sceta.push_back( ellv );
        obj_isElec.push_back(true);
        obj_index.push_back( eidx );
    }

    for( int pidx = 0; pidx < IN::ph_n; ++pidx ) {
        TLorentzVector phlv;
        phlv.SetPtEtaPhiE( IN::ph_pt->at(pidx),
                           IN::ph_eta->at(pidx),
                           IN::ph_phi->at(pidx),
                           IN::ph_e->at(pidx)    );
        objects.push_back( phlv );
        obj_isElec.push_back(false);
        obj_index.push_back( pidx );
        //phlv.SetPtEtaPhiE( phlv.Pt(), IN::ph_sceta->at(pidx), phlv.Phi(), phlv.E() );
        //objects_sceta.push_back( phlv );
    }

    if( objects.size() == 2 ) {
        for( unsigned i = 0; i < objects.size(); ++i) {
            OUT::probe_nConvTrk = -1;
            if( obj_isElec[i] ) { // if its an electron
                bool pass_tag_cuts = true;
                if( !config.PassFloat( "cut_tag_pt", objects[i].Pt() ) ) pass_tag_cuts = false;
                if( !config.PassBool( "cut_tag_triggerMatch", IN::el_triggerMatch->at(obj_index[i]) ) ) pass_tag_cuts = false;
                if( !config.PassBool( "cut_tag_passMvaTrig", IN::el_passMvaTrig->at(obj_index[i]) ) ) pass_tag_cuts = false;

                if( !pass_tag_cuts ) {
                    continue;
                }

                // fill tag info
                OUT::tag_pt = objects[i].Pt();
                OUT::tag_eta = objects[i].Eta();
                OUT::tag_phi = objects[i].Phi();
                //OUT::tag_eta_sc = objects_sceta[i].Eta();

                // now loop over the objects again
                for( unsigned j = 0; j < objects.size(); ++j) {
                    if( j == i ) continue; // but don't  use the same object
                    //this is a probe
                    OUT::probe_pt  = objects[j].Pt();
                    OUT::probe_eta = objects[j].Eta();
                    OUT::probe_phi = objects[j].Phi();
                    //OUT::probe_eta_sc = objects_sceta[j].Eta();
                    OUT::probe_isPhoton = !obj_isElec[j];
                    //if( OUT::probe_isPhoton ) {
                    //    OUT::probe_nConvTrk = IN::ph_conv_nTrk->at(obj_index[j]);
                    //}
                    OUT::probe_passtrig=false;
                    if( !OUT::probe_isPhoton   && 
                        objects[j].Pt() > 27   && 
                        IN::el_triggerMatch->at(obj_index[j])    && 
                        IN::el_passMvaTrig->at(obj_index[j])      ) {
                            OUT::probe_passtrig = true;
                    }

                    OUT::m_tagprobe = (objects[i] + objects[j]).M();
                    //OUT::m_tagprobe_sceta = ( objects_sceta[i] + objects_sceta[j] ).M();
                }

                outtree->Fill();
            }
        }
    }

}

void RunModule::MakeGGNtuple( ModuleConfig & config ) const {


    // collect objects
    std::vector< TLorentzVector> objects;
    std::vector<int> obj_index;
    std::vector<bool> obj_hasPixSeed;
    std::vector<bool> obj_hasTriggerMatch;
    for( int pidx = 0; pidx < IN::ph_n; ++pidx ) {
        TLorentzVector phlv;
        phlv.SetPtEtaPhiM( IN::ph_pt->at(pidx),
                           IN::ph_sceta->at(pidx),
                           IN::ph_phi->at(pidx),
                           0.0    );
        objects.push_back( phlv );
        obj_hasPixSeed.push_back( IN::ph_hasPixSeed->at(pidx) ); 
        obj_index.push_back( pidx );

        bool ph_has_trig_match = false;
        for( int eidx = 0 ; eidx < IN::el_n; ++eidx ) {

            TLorentzVector ellv;
            ellv.SetPtEtaPhiE( IN::el_pt->at(eidx),
                               IN::el_eta->at(eidx),
                               IN::el_phi->at(eidx),
                               IN::el_e->at(eidx)    );

            if( ( IN::el_triggerMatch->at(eidx) ) && ( ellv.DeltaR( phlv ) < 0.2 ) ) {
                ph_has_trig_match=true;
                break;
            }
        }

        obj_hasTriggerMatch.push_back( ph_has_trig_match );
                

    }

    if( objects.size() == 2 ) {
        for( unsigned i = 0; i < objects.size(); ++i) {
            bool pass_tag_cuts = true;
            if( !config.PassFloat( "cut_tag_pt", objects[i].Pt() ) ) pass_tag_cuts = false;
            if( !config.PassBool( "cut_tag_triggerMatch", obj_hasTriggerMatch[i] ) ) pass_tag_cuts = false;

            if( !pass_tag_cuts ) {
                continue;
            }

            // fill tag info
            OUT::tag_pt = objects[i].Pt();
            OUT::tag_eta = objects[i].Eta();
            OUT::tag_phi = objects[i].Phi();
            //OUT::tag_eta_sc = objects_sceta[i].Eta();

            // now loop over the objects again
            for( unsigned j = 0; j < objects.size(); ++j) {
                if( j == i ) continue; // but don't  use the same object
                //this is a probe
                OUT::probe_pt  = objects[j].Pt();
                OUT::probe_eta = objects[j].Eta();
                OUT::probe_phi = objects[j].Phi();
                //OUT::probe_eta_sc = objects_sceta[j].Eta();
                OUT::probe_isPhoton = (obj_hasPixSeed[j]==0);
                //if( OUT::probe_isPhoton ) {
                //    OUT::probe_nConvTrk = IN::ph_conv_nTrk->at(obj_index[j]);
                //}

                OUT::m_tagprobe = (objects[i] + objects[j]).M();
                OUT::dr_tagprobe = objects[i].DeltaR(objects[j]);
            }

            OUT::PUWeight = IN::PUWeight;
            OUT::run      = IN::run;
            OUT::event    = IN::event;

            outtree->Fill();
        
        }
    }

}

void RunModule::MakeMuMuNtuple( ModuleConfig & config ) const {

    // collect objects
    std::vector< TLorentzVector> muons;
    std::vector<int> mu_index;
    std::vector<bool> mu_hasTriggerMatch;
    std::vector<bool> mu_passTight;
    for( int idx = 0; idx < IN::mu_n; ++idx ) {
        TLorentzVector mulv;
        mulv.SetPtEtaPhiE( IN::mu_pt->at(idx),
                           IN::mu_eta->at(idx),
                           IN::mu_phi->at(idx),
                           IN::mu_e->at(idx)    );

        muons.push_back( mulv );
        mu_hasTriggerMatch.push_back( IN::mu_triggerMatch->at(idx) ); 
        mu_passTight.push_back( IN::mu_passTight->at(idx) ); 
        mu_index.push_back( idx );

    }

    if( muons.size() > 1 ) {
        for( unsigned i = 0; i < muons.size(); ++i) {
            bool pass_tag_cuts = true;
            if( !config.PassFloat( "cut_tag_pt", muons[i].Pt() ) ) pass_tag_cuts = false;
            if( !config.PassBool( "cut_tag_triggerMatch", mu_hasTriggerMatch[i] ) ) pass_tag_cuts = false;
            if( !config.PassBool( "cut_tag_tight", mu_passTight[i] ) ) pass_tag_cuts = false;

            if( !pass_tag_cuts ) {
                continue;
            }

            // fill tag info
            OUT::mutag_pt  = muons[i].Pt();
            OUT::mutag_eta = muons[i].Eta();
            OUT::mutag_phi = muons[i].Phi();

            // now loop over the objects again
            for( unsigned j = 0; j < muons.size(); ++j) {
                if( j == i ) continue; // but don't  use the same object
                //this is a probe
                OUT::muprobe_pt  = muons[j].Pt();
                OUT::muprobe_eta = muons[j].Eta();
                OUT::muprobe_phi = muons[j].Phi();
                OUT::muprobe_passTight = mu_passTight[j];
                OUT::muprobe_triggerMatch = mu_hasTriggerMatch[j];

                OUT::m_mutagprobe = (muons[i] + muons[j]).M();
                OUT::dr_mutagprobe = muons[i].DeltaR(muons[j]);

                OUT::PUWeight = IN::PUWeight;
                OUT::run      = IN::run;
                OUT::event    = IN::event;
                outtree->Fill();
        
            }

        }
    }

}


void RunModule::MakeEENtuple( ModuleConfig & config ) const {

    // collect objects
    std::vector< TLorentzVector> objects;
    std::vector<bool> obj_isEl;
    std::vector<bool> obj_isPh;
    std::vector<float> obj_matchElDR;
    std::vector<float> obj_mindr;
    std::vector<bool> obj_matchTrig;
    std::vector<bool> obj_passMVATrig;
    std::vector<bool> obj_passMVANonTrig;

    for( int phidx = 0 ; phidx < IN::ph_n; ++phidx) {

        TLorentzVector phlv;
        phlv.SetPtEtaPhiM( IN::ph_pt->at(phidx), 
                           IN::ph_eta->at(phidx),
                           IN::ph_phi->at(phidx),
                           0.0
                         );
        objects.push_back( phlv );
        obj_isPh.push_back( true );
        obj_matchTrig.push_back( false );
        obj_passMVANonTrig.push_back( false );
        obj_passMVATrig.push_back( false );

        bool match_el = false;
        float match_dr = 100;
        float mindr = 100;
        for( int eidx = 0; eidx < IN::el_n; ++eidx ) {

            TLorentzVector ellv;
            ellv.SetPtEtaPhiE( IN::el_pt->at(eidx),
                               IN::el_eta->at(eidx),
                               IN::el_phi->at(eidx),
                               IN::el_e->at(eidx)    );
            float dr = ellv.DeltaR( phlv );
            if( dr < 0.2 ) {
                match_el = true;
                match_dr = dr;
                break;
            }
            if( dr < mindr ) {
                mindr = dr;
            }
        }
        obj_isEl.push_back( match_el );
        obj_matchElDR.push_back( match_dr );
        obj_mindr.push_back( mindr );
    }

    for( int eidx = 0; eidx < IN::el_n; ++eidx ) {
        TLorentzVector ellv;
        ellv.SetPtEtaPhiE( IN::el_pt->at(eidx),
                           IN::el_eta->at(eidx),
                           IN::el_phi->at(eidx),
                           IN::el_e->at(eidx)    );
        objects.push_back( ellv );
        obj_isEl.push_back(true);
        obj_matchElDR.push_back(0);
        obj_mindr.push_back(0);
        obj_isPh.push_back(false);
        obj_matchTrig.push_back( IN::el_triggerMatch->at( eidx ) );
        obj_passMVATrig.push_back( IN::el_passMvaTrig->at( eidx ) );
        obj_passMVANonTrig.push_back( IN::el_passMvaNonTrig->at( eidx ) );
               
    }

    if( objects.size() > 1  ) {
        for( unsigned i = 0; i < objects.size(); ++i) {
            bool pass_tag_cuts = true;
            if( !config.PassFloat( "cut_tag_pt", objects[i].Pt() ) ) pass_tag_cuts = false;
            if( !config.PassBool( "cut_tag_triggerMatch", obj_matchTrig[i] ) ) pass_tag_cuts = false;
            if( !config.PassBool( "cut_tag_passMvaTrig", obj_passMVATrig[i] ) ) pass_tag_cuts = false;

            if( obj_isPh[i] ) pass_tag_cuts = false;
            if( !obj_isEl[i] ) pass_tag_cuts = false;

            if( !pass_tag_cuts ) {
                continue;
            }


            // now loop over the objects again
            for( unsigned j = 0; j < objects.size(); ++j) {
                if( j == i ) continue; // but don't  use the same object
                // fill tag info
                OUT::eltag_pt = objects[i].Pt();
                OUT::eltag_eta = objects[i].Eta();
                OUT::eltag_phi = objects[i].Phi();
                //this is a probe
                OUT::elprobe_pt  = objects[j].Pt();
                OUT::elprobe_eta = objects[j].Eta();
                OUT::elprobe_phi = objects[j].Phi();
                OUT::elprobe_isEl = obj_isEl[j];
                OUT::elprobe_matchElDR = obj_matchElDR[j];
                OUT::elprobe_mindr= obj_mindr[j];
                OUT::elprobe_isPh = obj_isPh[j];
                OUT::elprobe_triggerMatch   = obj_matchTrig[j];
                OUT::elprobe_passMVANonTrig = obj_passMVANonTrig[j];
                OUT::elprobe_passMVATrig    = obj_passMVATrig[j];

                OUT::m_eltagprobe = (objects[i] + objects[j]).M();
                OUT::dr_eltagprobe = objects[i].DeltaR(objects[j]);
                //OUT::m_tagprobe_sceta = ( objects_sceta[i] + objects_sceta[j] ).M();
                
                OUT::PUWeight = IN::PUWeight;
                OUT::run      = IN::run;
                OUT::event    = IN::event;
                outtree->Fill();
            }

        }
    }
}

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    int nPh = IN::ph_n;
    int nEl  = IN::el_n;
    int nMu  = IN::mu_n;

    int el_passtrig_n = 0;
    for( int i = 0 ; i < nEl; ++i ) {
        if( IN::el_triggerMatch->at(i) && IN::el_pt->at(i) > 30 && IN::el_passMvaTrig->at(i) ) {
            el_passtrig_n++;
        }
    }

    int mu_passtrig_n = 0;
    for( int i = 0 ; i < nMu; ++i ) {
        if( IN::mu_triggerMatch->at(i) && IN::mu_pt->at(i) > 25 && IN::mu_passTight->at(i) ) {
            mu_passtrig_n++;
        }
    }


    if( !config.PassInt("cut_n_mu", nMu ) ) keep_event = false;
    if( !config.PassInt("cut_n_ph", nPh ) ) keep_event = false;
    if( !config.PassInt("cut_n_elph", nPh+nEl ) ) keep_event = false;
    if( !config.PassInt("cut_n_el_passtrig", el_passtrig_n ) ) keep_event = false;
    if( !config.PassInt("cut_n_mu_passtrig", mu_passtrig_n ) ) keep_event = false;

    return keep_event;
    
}

