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

    outtree->Branch("tag_pt"           , &OUT::tag_pt           );
    outtree->Branch("tag_eta"          , &OUT::tag_eta          );
    outtree->Branch("tag_eta_sc"       , &OUT::tag_eta_sc       );
    outtree->Branch("tag_phi"          , &OUT::tag_phi          );
    outtree->Branch("probe_pt"         , &OUT::probe_pt         );
    outtree->Branch("probe_eta"        , &OUT::probe_eta        );
    outtree->Branch("probe_eta_sc"     , &OUT::probe_eta_sc     );
    outtree->Branch("probe_phi"        , &OUT::probe_phi        );
    outtree->Branch("probe_isPhoton"   , &OUT::probe_isPhoton   );
    outtree->Branch("probe_nConvTrk"   , &OUT::probe_nConvTrk   );
    outtree->Branch("probe_passtrig"   , &OUT::probe_passtrig   );
    outtree->Branch("m_tagprobe"       , &OUT::m_tagprobe       );
    outtree->Branch("m_tagprobe_sceta" , &OUT::m_tagprobe_sceta );


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
        }
    }
    
    // always return false, handle the tree filling locally
    return false;

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

// This is an example of a module that applies an
// event filter.  Note that it returns a bool instead
// of a void.  In principle the modules can return any
// type of variable, you just have to handle it
// in the ApplyModule function

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    int nPh = IN::ph_n;
    int nEl  = IN::el_n;

    if( !config.PassInt("cut_n_elph", nPh+nEl ) ) keep_event = false;
    if( !config.PassInt("cut_n_el_passtrig", IN::el_passtrig_n ) ) keep_event = false;

    return keep_event;
    
}

