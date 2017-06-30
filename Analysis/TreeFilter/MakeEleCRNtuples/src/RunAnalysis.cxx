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
#include "CalcWggEventVars.h"
#include "MakePhotonSorting.h"

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
    OUT::isDuplicated              = 0;

    // *************************
    // Declare Branches
    // *************************

    // Examples :
    outtree->Branch("isDuplicated"             , &OUT::isDuplicated , "isDuplicated/O"    );

}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    // Don't copy at the beginning
    //CopyInputVarsToOutput();

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        save_event &= ApplyModule( mod_conf );
    }

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    if( config.GetName() == "RunNtupleProcessing" ) {
        RunNtupleProcessing( config );
    }

    //never save the event ouside of this module
    return false;

}

void RunModule::RunNtupleProcessing( ModuleConfig & config ) const {

    OUT::isDuplicated          = 0;

    if( IN::el_passtrig_n == 0 ) {
        return;
    }

    std::vector<TLorentzVector> trigelelv;
    // save the indices of the triggered electrons
    std::vector<int> trigele_idx;

    for( int eidx = 0; eidx < IN::el_n; ++eidx ) {

        if( IN::el_pt->at(eidx) > 30 && IN::el_triggerMatch->at(eidx) && IN::el_passMvaTrig->at(eidx) ) {

            TLorentzVector elv;
            elv.SetPtEtaPhiE( IN::el_pt->at(eidx),
                              IN::el_eta->at(eidx),
                              IN::el_phi->at(eidx),
                              IN::el_e->at(eidx)
                            );

            trigelelv.push_back( elv );
            trigele_idx.push_back( eidx );
        }

    }
    for( unsigned tidx = 0; tidx < trigelelv.size(); ++tidx ) {
        
        // copy the branches over
        CopyInputVarsToOutput();

        // set the duplicated status
        if( tidx > 0 ) {
            OUT::isDuplicated = 1;
        }
        else {
            OUT::isDuplicated = 0;
        }

        // we'll always have only one triggered electron now
        OUT::el_passtrig_n = 1;
        // remove any other triggered electrons from the collection
        OUT::el_n = 0;
        ClearOutputPrefix( "el_" );
        for( int eidx = 0; eidx < IN::el_n; ++eidx ) {

            // save all of the electrons except for any
            // triggered electrons that are not this one
            if( eidx != trigele_idx[tidx] ) {
                if( std::find( trigele_idx.begin(), trigele_idx.end(), eidx ) != trigele_idx.end() ) {
                    continue;
                }
            }

            OUT::el_n++;
            CopyPrefixIndexBranchesInToOut( "el_", eidx );
        }

        // now filter the photons
        OUT::ph_n = 0;
        ClearOutputPrefix("ph_");


        for( int pidx = 0; pidx < IN::ph_n; ++pidx ) {

            TLorentzVector phlv;

            phlv.SetPtEtaPhiE( IN::ph_pt->at(pidx), 
                               IN::ph_eta->at(pidx), 
                               IN::ph_phi->at(pidx), 
                               IN::ph_e->at(pidx) );

            if( phlv.DeltaR( trigelelv[tidx] ) < 0.4 ) {
                continue;
            }

            if( !config.PassBool( "cut_hasPixSeed_singlePhot", IN::ph_hasPixSeed->at(pidx) ) ) continue;
            
            OUT::ph_n++;
            CopyPrefixIndexBranchesInToOut( "ph_", pidx );
        }

        bool keep_event = true;

        if( !config.PassInt( "cut_nph", OUT::ph_n ) ) keep_event = false;

        // Make photon cuts
        if( OUT::ph_n > 1 ) {
            if( OUT::ph_pt->at(0) > OUT::ph_pt->at(1) ) {
                if( !config.PassBool( "cut_hasPixSeed_leadph12", OUT::ph_hasPixSeed->at(0) ) ) keep_event = false;
                if( !config.PassBool( "cut_hasPixSeed_sublph12", OUT::ph_hasPixSeed->at(1) ) ) keep_event = false;
                if( !config.PassBool( "cut_csev_leadph12", OUT::ph_eleVeto->at(0) ) ) keep_event = false;
                if( !config.PassBool( "cut_csev_sublph12", OUT::ph_eleVeto->at(1) ) ) keep_event = false;
                if( !config.PassBool( "cut_eleOlap_leadph12", ( OUT::ph_elMinDR->at(0) < 0.4) ) ) keep_event = false;
                if( !config.PassBool( "cut_eleOlap_sublph12", ( OUT::ph_elMinDR->at(1) < 0.4) ) ) keep_event = false;
            }
            else {
                if( !config.PassBool( "cut_hasPixSeed_leadph12", OUT::ph_hasPixSeed->at(1) ) ) keep_event = false;
                if( !config.PassBool( "cut_hasPixSeed_sublph12", OUT::ph_hasPixSeed->at(0) ) ) keep_event = false;
                if( !config.PassBool( "cut_csev_leadph12", OUT::ph_eleVeto->at(1) ) ) keep_event = false;
                if( !config.PassBool( "cut_csev_sublph12", OUT::ph_eleVeto->at(0) ) ) keep_event = false;
                if( !config.PassBool( "cut_eleOlap_leadph12", ( OUT::ph_elMinDR->at(1) < 0.4) ) ) keep_event = false;
                if( !config.PassBool( "cut_eleOlap_sublph12", ( OUT::ph_elMinDR->at(0) < 0.4) ) ) keep_event = false;
            }
        }


        if( !keep_event ) continue;

        // now collect all objects to calculate
        // event level quantities
        std::vector<TLorentzVector> photons;
        std::vector<TLorentzVector> muons;
        std::vector<TLorentzVector> electrons;
        std::vector<TLorentzVector> trigelectrons;
        std::vector<TLorentzVector> trigmuons;
        std::vector<std::pair<float, int> > sorted_photons;

        for( int idx = 0; idx < OUT::mu_n; idx++ ) {

            TLorentzVector lv;
            lv.SetPtEtaPhiM(  OUT::mu_pt->at(idx),
                              OUT::mu_eta->at(idx),
                              OUT::mu_phi->at(idx),
                              0.1057
                            );
            muons.push_back( lv );
            if( lv.Pt() > 25 && fabs(lv.Eta()) < 2.1 && OUT::mu_triggerMatch->at(idx) ) {
                trigmuons.push_back(lv);
            }
        }

        trigelectrons.push_back( trigelelv[tidx] );

        for( int idx = 0; idx < OUT::ph_n; idx++ ) {

            TLorentzVector lv;
            lv.SetPtEtaPhiE(  OUT::ph_pt->at(idx),
                              OUT::ph_eta->at(idx),
                              OUT::ph_phi->at(idx),
                              OUT::ph_e->at(idx)
                            );
            photons.push_back( lv );
            sorted_photons.push_back( std::make_pair( lv.Pt(), idx ) );
        } 

        TLorentzVector metlv;
        metlv.SetPtEtaPhiM( OUT::pfType01MET, 0.0, OUT::pfType01METPhi, 0.0 );

            
        std::map<std::string, float> results;
        std::map<std::string, std::vector<float> > vector_results;

        Wgg::CalcEventVars( photons, electrons, muons, trigelectrons, trigmuons, metlv, results, vector_results );

        CopyMapVarsToOut( results );
        CopyVectorMapVarsToOut( vector_results );

        std::map<std::string, int> sort_results;
        std::map<std::string, std::vector<int> > vector_sort_results;
        Wgg::MakePhotonSorting( photons, OUT::ph_sigmaIEIE, OUT::ph_chIsoCorr, OUT::ph_phoIsoCorr, OUT::ph_neuIsoCorr, OUT::ph_passHOverEMedium, OUT::ph_passSIEIEMedium, OUT::ph_passChIsoCorrMedium, OUT::ph_passNeuIsoCorrMedium, OUT::ph_passPhoIsoCorrMedium, OUT::ph_hasPixSeed, OUT::ph_eleVeto, sort_results, vector_sort_results );

        CopyIntMapVarsToOut( sort_results );
        CopyIntVectorMapVarsToOut( vector_sort_results );

        std::sort(sorted_photons.rbegin(), sorted_photons.rend());
        if( sorted_photons.size() > 1 ) {
            int leadidx = sorted_photons[0].second;
            int sublidx = sorted_photons[1].second;
            OUT::hasPixSeed_leadph12 = OUT::ph_hasPixSeed->at(leadidx);
            OUT::hasPixSeed_sublph12 = OUT::ph_hasPixSeed->at(sublidx);
            OUT::sieie_leadph12 = OUT::ph_sigmaIEIE->at(leadidx);
            OUT::sieie_sublph12 = OUT::ph_sigmaIEIE->at(sublidx);
            OUT::chIsoCorr_leadph12 = OUT::ph_chIsoCorr->at(leadidx);
            OUT::chIsoCorr_sublph12 = OUT::ph_chIsoCorr->at(sublidx);
            OUT::neuIsoCorr_leadph12 = OUT::ph_neuIsoCorr->at(leadidx);
            OUT::neuIsoCorr_sublph12 = OUT::ph_neuIsoCorr->at(sublidx);
            OUT::phoIsoCorr_leadph12 = OUT::ph_phoIsoCorr->at(leadidx);
            OUT::phoIsoCorr_sublph12 = OUT::ph_phoIsoCorr->at(sublidx);
            OUT::isEB_leadph12 = OUT::ph_IsEB->at(leadidx);
            OUT::isEB_sublph12 = OUT::ph_IsEB->at(sublidx);
            OUT::isEE_leadph12 = OUT::ph_IsEE->at(leadidx);
            OUT::isEE_sublph12 = OUT::ph_IsEE->at(sublidx);
            OUT::truthMatchPh_leadph12 = OUT::ph_truthMatch_ph->at(leadidx);
            OUT::truthMatchPh_sublph12 = OUT::ph_truthMatch_ph->at(sublidx);
            OUT::truthMatchPhMomPID_leadph12 = OUT::ph_truthMatchMotherPID_ph->at(leadidx);
            OUT::truthMatchPhMomPID_sublph12 = OUT::ph_truthMatchMotherPID_ph->at(sublidx);
        }

        // fill the tree
        outtree->Fill();

    }

}

