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

    outtree->Branch( "n_gen_photon"       , &OUT::n_gen_photon, "n_gen_photon/I" );
    outtree->Branch( "n_gen_photon_pt10"  , &OUT::n_gen_photon_pt10, "n_gen_photon_pt10/I" );
    outtree->Branch( "n_non_prompt_photon", &OUT::n_non_prompt_photon, "n_non_prompt_photon/I" );
    outtree->Branch( "n_ewk_photon"       , &OUT::n_ewk_photon, "n_ewk_photon/I" );
    outtree->Branch( "n_lep_photon"       , &OUT::n_lep_photon, "n_lep_photon/I" );
    outtree->Branch( "n_qcd_photon"       , &OUT::n_qcd_photon, "n_qcd_photon/I" );
    outtree->Branch( "n_lep_photon_raw"   , &OUT::n_lep_photon_raw, "n_lep_photon_raw/I" );

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

    // This bool is used for filtering
    // If a module implements an event filter
    // update this variable and return it
    // to apply the filter
    bool keep_evt = true;

    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }

    if( config.GetName() == "FilterPhotonsMother" ) {
        keep_evt &= FilterPhotonsMother( config );
    }

    return keep_evt;

}

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_evt = true;

    int non_prompt_mask = 0x4;
    int ewk_parent_mask = 0x8;
    int lep_parent_mask = 0x10; 
    int qcd_parent_mask = 0x2; 

    //int gen_photon_mask = lep_parent_mask | qcd_parent_mask;
    int gen_photon_mask = 0x12;

    OUT::n_gen_photon = 0;
    OUT::n_gen_photon_pt10 = 0;
    OUT::n_non_prompt_photon = 0;
    OUT::n_ewk_photon = 0;
    OUT::n_lep_photon = 0;
    OUT::n_qcd_photon = 0;
    OUT::n_lep_photon_raw = 0;

    std::vector<int> matched_idx;
    std::vector<int> matched_pdgid;
    //std::cout << "EVENT" << std::endl;
    for( int idx = 0; idx < IN::nMC; ++idx ) {

        if( IN::mcPID->at(idx) == 22 ) {

            TLorentzVector phlv;
            phlv.SetPtEtaPhiE( IN::mcPt->at(idx), 
                               IN::mcEta->at(idx), 
                               IN::mcPhi->at(idx), 
                               IN::mcE->at(idx) );

            bool is_gen_photon        = ( (IN::mcParentage->at(idx) & gen_photon_mask ) == gen_photon_mask );
            bool is_non_prompt_photon = ( (IN::mcParentage->at(idx) & non_prompt_mask ) == non_prompt_mask);
            bool is_ewk_photon        = ( (IN::mcParentage->at(idx) & ewk_parent_mask ) == ewk_parent_mask);
            bool is_lep_photon        = ( (IN::mcParentage->at(idx) & lep_parent_mask ) == lep_parent_mask);
            bool is_qcd_photon        = ( (IN::mcParentage->at(idx) & qcd_parent_mask ) == qcd_parent_mask);

            // find potential mother particles
            // and calculate the dR with respect to those
            // particles.  If the minimum dR is greater than 0.4
            // then count it as a gen photon
            float mindr = 100;
            for( int midx = 0; midx < IN::nMC; ++midx ) {
                if( abs(IN::mcPID->at(midx)) == 11 || abs(IN::mcPID->at(midx)) == 13 ||  abs(IN::mcPID->at(midx)) == 15 ) {
                //if( IN::mcMomPID->at(idx) == IN::mcPID->at(midx) ) {
                    TLorentzVector leplv;
                    leplv.SetPtEtaPhiE( IN::mcPt->at(midx), 
                                        IN::mcEta->at(midx), 
                                        IN::mcPhi->at(midx), 
                                        IN::mcE->at(midx) );
                    float dr = leplv.DeltaR(phlv);

                    if( dr < mindr ) {
                        mindr = dr;
                    }
                }
            }
            if( is_lep_photon ) {
                OUT::n_lep_photon_raw++;
            }

            //if( mindr > 0.3 ) {
            if( !is_lep_photon || mindr > 0.3 ) {
                    //if( is_gen_photon || is_qcd_photon ) {
                    if( ! is_non_prompt_photon ) {
                        OUT::n_gen_photon++;
                        if( phlv.Pt() > 10 ) {
                            OUT::n_gen_photon_pt10++;
                        }

                    }
                    if( is_non_prompt_photon ) OUT::n_non_prompt_photon++;
                    if( is_ewk_photon ) {
                        //std::cout << "is EWk " << std::endl;
                        OUT::n_ewk_photon++;
                    }
                    if( is_lep_photon ) {
                        //std::cout << "is lep " << std::endl;
                        OUT::n_lep_photon++;
                    }
                    if( is_qcd_photon ) {
                        //std::cout << "is qcd " << std::endl;
                        OUT::n_qcd_photon++;
                    }
                }
                //else {
                //    if( is_gen_photon ) {
                //    std::cout << "Is gen and Did not find mother " << std::endl;
                //    std::cout << "Mother " << IN::mcMomPID->at(idx) << " GMom " << IN::mcGMomPID->at(idx) << std::endl;
                //    }
                //}
            //}
            
        }
    }

    if( !config.PassInt( "cut_n_gen_photons", OUT::n_gen_photon ) ) keep_evt = false;
    if( !config.PassInt( "cut_n_gen_photons_pt10", OUT::n_gen_photon_pt10 ) ) keep_evt = false;
    if( !config.PassInt( "cut_n_true_photons_pt15", OUT::truegenphpt15_n) ) keep_evt = false;
    if( !config.PassInt( "cut_n_lep_photons", OUT::n_lep_photon_raw) ) keep_evt = false;

    return keep_evt;

}

bool RunModule::FilterPhotonsMother( ModuleConfig & config ) const {

    bool keep_evt = true;

    OUT::n_gen_photon = 0;
    OUT::n_non_prompt_photon = 0;
    OUT::n_ewk_photon = 0;
    OUT::n_lep_photon = 0;
    OUT::n_qcd_photon = 0;

    int n_non_prompt_photon_pt15 = 0;
    int n_ewk_photon_pt15 = 0;
    int n_lep_photon_pt15 = 0;
    int n_qcd_photon_pt15 = 0;

    for( int idx = 0; idx < IN::nMC; ++idx ) {

        if( IN::mcPID->at(idx) == 22 ) {

            int momPID = IN::mcMomPID->at(idx);

            if( fabs(momPID) == 23 || fabs(momPID) ==24 ) { 
                OUT::n_ewk_photon++;
                if( IN::mcPt->at(idx) > 15 ) n_ewk_photon_pt15++;
            }
            else if( fabs(momPID) < 6 || momPID == 21) {
                OUT::n_qcd_photon++;
                if( IN::mcPt->at(idx) > 15 ) n_qcd_photon_pt15++;
            }
            else if( fabs(momPID) >= 11 && fabs(momPID) <= 15 ) {
                OUT::n_lep_photon++;
                if( IN::mcPt->at(idx) > 15 ) n_lep_photon_pt15++;
            }
            else {
                OUT::n_non_prompt_photon++;
                if( IN::mcPt->at(idx) > 15 ) n_non_prompt_photon_pt15++;
            }

        }
    }
    if( !config.PassInt( "cut_n_ewklepqcd_photons", OUT::n_ewk_photon+OUT::n_lep_photon+OUT::n_qcd_photon ) ) keep_evt = false;
    if( !config.PassInt( "cut_n_ewklepqcd_photons_pt15", n_ewk_photon_pt15+n_lep_photon_pt15+n_qcd_photon_pt15 ) ) keep_evt = false;

    return keep_evt;

}

