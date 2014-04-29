#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"

#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"


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
        void finalize( ) {};

        // The ApplyModule function calls any other module defined below
        // in src/RunModule.cxx.  This funciton is not strictly required
        // but its a consistent way to apply modules
        bool ApplyModule         ( ModuleConfig & config ) const;


        // Define modules below.
        // There is no restriction on the naming
        // return values, or inputs to these functions, but
        // you must of course handle them in the source file
        // Examples :
        void EvalMVA ( ModuleConfig & config ) const;

        TMVA::Reader *TMVAReaderEl;
        TMVA::Reader *TMVAReaderMu;
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    //Examples
    Float_t              zrej_mvascore;
};

namespace MVAVars {

    float m_lepphph;
    float m_lepph1;
    float m_lepph2;
    float m_phph;
    float leadPhot_leadLepDR;
    float sublPhot_leadLepDR;
    float ph_phDR;
    float dphi_met_lep1;
    float dphi_met_ph1;
    float dphi_met_ph2;
}

#endif
