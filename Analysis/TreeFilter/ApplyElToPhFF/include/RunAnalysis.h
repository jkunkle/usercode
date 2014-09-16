#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"
#include "BranchDefs.h"

#include <string>
#include <vector>


#include "TH2F.h"
#include "TTree.h"
#include "TChain.h"
#include "TRandom3.h"
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
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & configs) ;
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( ) ;

        bool AddEventWeight         ( ModuleConfig & config ) ;

    private :
        TFile * rfile;
        TH2F * rhist;
        TTree * outtree;
        std::string sample_key;
        std::string nconv;
        CmdOptions options;

};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    Float_t            EventWeightElFF;
    Float_t            EventErrElFF;

    Bool_t             HasElToPhFF;
};

#endif
