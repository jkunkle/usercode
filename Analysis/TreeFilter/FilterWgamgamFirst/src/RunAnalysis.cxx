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
    
    //// *************************
    //// Set defaults for added output variables
    //// *************************
    //OUT::eleD0LepVtx = 0;
    //OUT::eleDzLepVtx = 0;
    //OUT::muD0LepVtx = 0;
    //OUT::muDzLepVtx = 0;

    //// *************************
    //// Declare Branches
    //// *************************
    //outtree->Branch("eleD0LepVtx", &OUT::eleD0LepVtx);
    //outtree->Branch("eleDzLepVtx", &OUT::eleDzLepVtx);
    //outtree->Branch("muD0LepVtx",  &OUT::muD0LepVtx);
    //outtree->Branch("muDzLepVtx",  &OUT::muDzLepVtx);
  
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

    // This part is a bit hacked.  For each module that
    // you write below, you have to put a call to that
    // function with a matching name here.
    // The name is used to match the name used
    // in the python configuration.
    // There are fancy ways to do this, but it
    // would require the code to be much more complicated
    //
    // Example :
    if( config.GetName() == "FilterElec" ) {
        FilterElec( config );
    }
    if( config.GetName() == "FilterMuon" ) {
        FilterMuon( config );
    }
    if( config.GetName() == "FilterJet" ) {
        FilterJet( config );
    }
    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }
    if( config.GetName() == "FilterTrigger" ) {
        keep_evt &= FilterTrigger( config );
    }
    if( config.GetName() == "CalcLeptonVtxVars" ) {
        CalcLeptonVtxVars( config );
    }


    // If the module applies a filter the filter decision
    // is passed back to here.  There is no requirement
    // that a function returns a bool, but
    // if you want the filter to work you need to do this
    //
    // Example :

    return keep_evt;

}

void RunModule::FilterElec( ModuleConfig & config ) const {

    OUT::nEle = 0;
    ClearOutputPrefix("ele");

    for( int idx = 0; idx < IN::nEle; ++idx ) {
        
        float elePt = IN::elePt->at(idx);

        if( !config.PassFloat( "cut_pt", elePt ) ) continue;

        OUT::nEle++;
        CopyPrefixIndexBranchesInToOut( "ele", idx );
    }

}     

void RunModule::CalcLeptonVtxVars( ModuleConfig & /*config*/ ) const { 

    //OUT::eleD0LepVtx->clear();
    //OUT::eleDzLepVtx->clear();
    //OUT::muD0LepVtx->clear();
    //OUT::muDzLepVtx->clear();

    //for( int idx = 0; idx < IN::nEle; ++idx ) {
    //    bool found_nearest = false;
    //    unsigned nearestIdx=0;
    //    float mindz = 1000;
    //    for( int vidx = 0; vidx < IN::nVtxBS; ++vidx ) {
    //        float dz = fabs(IN::vtxbs_z->at(vidx)-IN::eleVtx_z->at(idx));
    //        if( dz < mindz ) {
    //            mindz = dz;
    //            nearestIdx = vidx;
    //            found_nearest = true;
    //        }
    //    }
    //    if( !found_nearest ) {
    //        std::cout << "WARNING -- no nearest vertex found" << std::endl;
    //    }
    //    if( IN::eleD0Vtx->at(idx).size() ) {
    //        OUT::eleD0LepVtx->push_back(IN::eleD0Vtx->at(idx).at(nearestIdx));
    //    }
    //    if( IN::eleDzVtx->at(idx).size() ) {
    //        OUT::eleDzLepVtx->push_back(IN::eleDzVtx->at(idx).at(nearestIdx));
    //    }
    //    
    //}

    //for( int idx = 0; idx < IN::nMu; ++idx ) {
    //    bool found_nearest = false;
    //    unsigned nearestIdx=0;
    //    float mindz = 1000;
    //    for( int vidx = 0; vidx < IN::nVtxBS; ++vidx ) {
    //        float dz = fabs(IN::vtxbs_z->at(vidx)-IN::muVtx_z->at(idx));
    //        if( dz < mindz ) {
    //            mindz = dz;
    //            nearestIdx = vidx;
    //            found_nearest = true;
    //        }
    //    }
    //    if( !found_nearest ) {
    //        std::cout << "WARNING -- no nearest vertex found" << std::endl;
    //    }
    //    if( IN::muD0Vtx->at(idx).size() ) {
    //        OUT::muD0LepVtx->push_back(IN::muD0Vtx->at(idx).at(nearestIdx));
    //    }
    //    if( IN::muDzVtx->at(idx).size() ) {
    //        OUT::muDzLepVtx->push_back(IN::muDzVtx->at(idx).at(nearestIdx));
    //    }
    //    
    //}

}



void RunModule::FilterJet( ModuleConfig & config ) const {

    // NOTE this assumes that the jets are 
    // sorted in descending order


    OUT::nJet = 0;
    ClearOutputPrefix("jet");
    for( int idx = 0; idx < IN::nJet; ++idx ) {
        
        float jetPt = IN::jetPt->at(idx);

        if( !config.PassFloat( "cut_pt", jetPt ) ) continue;

        OUT::nJet++;

        CopyPrefixIndexBranchesInToOut( "jet", idx );
    }

}     

void RunModule::FilterMuon( ModuleConfig & config ) const {



    OUT::nMu = 0;
    for( int idx = 0; idx < IN::nMu; ++idx ) {
        
        float muPt = IN::muPt->at(idx);

        if( !config.PassFloat( "cut_pt", muPt ) ) continue;

        OUT::nMu++;
        CopyPrefixIndexBranchesInToOut( "mu", idx );
            
    }


}     

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    int nMu = OUT::nMu;
    int nEl = OUT::nEle;
    int nPho = OUT::nPho;
    int nLep = nMu + nEl;
    int nLepPho = nLep + nPho;

    bool keep_evt = true;

    if( !config.PassInt( "cut_nEl", nEl ) ) keep_evt = false;
    if( !config.PassInt( "cut_nMu", nMu ) ) keep_evt = false;
    if( !config.PassInt( "cut_nPho", nPho ) ) keep_evt = false;
    if( !config.PassInt( "cut_nLep", nLep ) ) keep_evt = false;
    if( !config.PassInt( "cut_nLepPho", nLepPho ) ) keep_evt = false;
    

    if( config.HasCut( "cut_el_ph_mindr" ) ) {
       
        std::vector<TLorentzVector> electrons;
        std::vector<TLorentzVector> photons;

        int nElOlap = 0;
        int nElOlapPt5 = 0;
        for( int eidx = 0 ; eidx < nEl; ++eidx) {
            TLorentzVector el;
            el.SetPtEtaPhiE( OUT::elePt->at(eidx), OUT::eleEta->at(eidx), OUT::elePhi->at(eidx), OUT::eleEn->at(eidx) );

            float min_dr = 100.0;
            for( int pidx = 0 ; pidx < nPho; ++pidx) {

                TLorentzVector ph;
                ph.SetPtEtaPhiM( OUT::phoEt->at(pidx), OUT::phoEta->at(pidx), OUT::phoPhi->at(pidx), 0.0 );

                float dr = el.DeltaR(ph);
                if( dr < min_dr  ) min_dr = dr;
            }

            if( !config.PassFloat( "cut_el_ph_mindr", min_dr ) ) {
                nElOlap++;
                if( el.Pt() > 5 ) {
                    nElOlapPt5++;
                }
            }
        }

        if( !config.PassInt( "cut_nElOlap", nElOlap ) ) keep_evt = false;
        if( !config.PassInt( "cut_nMunElOlap", nElOlap+nMu ) ) keep_evt = false;
        if( !config.PassInt( "cut_nMunElOlapPt5", nElOlapPt5+nMu ) ) keep_evt = false;

    }


    return keep_evt;

}     

bool RunModule::FilterTrigger( ModuleConfig & config ) const {
    
    bool keep_evt = false;
    BOOST_FOREACH( const Cut & cut, config.GetCut("cut_trigger").GetCuts() ) {
       if( IN::HLT[IN::HLTIndex[cut.val_int] ] > 0 ) keep_evt = true;
    }

    return keep_evt;
}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//
// Examples :


