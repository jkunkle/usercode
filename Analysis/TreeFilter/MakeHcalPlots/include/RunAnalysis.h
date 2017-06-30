#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


#include "TH2.h"
#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"

// The RunModule inherits from RunModuleBase (an Abstract Base Class )
// defined in the Core package so that all
// RunModules present a common interface in a Run function
// This allows the code defined in this package
// to be run from the Core package to minimize
// code duplication in each module
class RunModule : public virtual RunModuleBase {

    public :

        RunModule() {}

        // The run function must exist and be defined exactly as this
        // because it is defined in RunModuleBase 
        // in src/RunModule.cxx all the analysis is defind in this RunModule function
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & config) ;
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( ) ;

        // The ApplyModule function calls any other module defined below
        // in src/RunModule.cxx.  This funciton is not strictly required
        // but its a consistent way to apply modules
        bool ApplyModule         ( ModuleConfig & config ) ;


        void PlotHBHE     ( ModuleConfig & config ) ;
        void PlotHF       ( ModuleConfig & config ) ;

        TH1F * avg_adc_event_HBHE;
        TH1F * avg_adc_event_HF;
        TH1F * avg_adc_HBHE;
        TH1F * avg_adc_HF;
        TH2F * adc_depth_highadc;
        TH2F * adc_depth;
        TH1F * adc_HBHE;
        TH1F * adc_HF;

        TH1F * bx_HBHE_highadc;
        TH1F * bx_HF_highadc;

        TFile * _outfile;

        int _evn;

        std::map<std::pair<int, int>, TH1F > ch_adc_map;
        std::map<std::pair<int, int>, TH1F > ch_highadc_map;
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

};

#endif
