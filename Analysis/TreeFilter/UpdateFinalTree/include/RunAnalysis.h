#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TRandom3.h"

// The RunModule inherits from RunModuleBase (an Abstract Base Class )
// defined in the Core package so that all
// RunModules present a common interface in a Run function
// This allows the code defined in this package
// to be run from the Core package to minimize
// code duplication in each module
class RunModule : public virtual RunModuleBase {

    public :

        RunModule();

        // The run function must exist and be defined exactly as this
        // because it is defined in RunModuleBase 
        // in src/RunModule.cxx all the analysis is defind in this RunModule function
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & config) ;
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( ) {};

        // The ApplyModule function calls any other module defined below
        // in src/RunModule.cxx.  This funciton is not strictly required
        // but its a consistent way to apply modules
        bool ApplyModule         ( ModuleConfig & config, const CmdOptions & options ) ;


        // Define modules below.
        // There is no restriction on the naming
        // return values, or inputs to these functions, but
        // you must of course handle them in the source file
        // Examples :
        void CalcEventVars ( ModuleConfig & config ) const;
        bool AddEventWeight( ModuleConfig & config, const CmdOptions & options );
        bool ApplyPUBiasWeight( ModuleConfig & config );

    private :

        TFile * rfile;
        TH1F * rhist;
        TH1F * whist_eb;
        TH1F * whist_ee;
        TRandom3 * rand;
        CmdOptions options;
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    //Examples
    //Int_t              mu_pt25_n;
    //Int_t              el_pt25_n;
    //Float_t            EventWeight;
    //Bool_t             HasElToPhFF;

    //Float_t            leadPhot_leadLepDR;
    //Float_t            leadPhot_sublLepDR;
    //Float_t            sublPhot_leadLepDR;
    //Float_t            sublPhot_sublLepDR;

    Float_t              PUBiasWeight_ee;
    Float_t              PUBiasWeight_eb;
};

#endif
