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
        void BuildPhoton         ( ModuleConfig & config ) const;

        // tmva files for photon mva
        TMVA::Reader *TMVAReaderEB5;
        TMVA::Reader *TMVAReaderEE5;
        TMVA::Reader *TMVAReaderEB6;
        TMVA::Reader *TMVAReaderEE6;
        TMVA::Reader *TMVAReaderEB11;
        TMVA::Reader *TMVAReaderEE11;
        TMVA::Reader *TMVAReaderEB11W;
        TMVA::Reader *TMVAReaderEE11W;
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    //std::vector<float> *ph_mvascore_5var;
    //std::vector<float> *ph_mvascore_6var;
    //std::vector<float> *ph_mvascore_11var;
    std::vector<float> *ph_mvascore_11varW;
};

namespace MVAVars {

    //// EB
    //float phoPhi;
    //float phoR9;
    //float phoSigmaIEtaIEta;
    //float phoSigmaIEtaIPhi;
    //float s13;
    //float s4ratio;
    //float s25;
    //float phoSCEta;
    //float phoSCRawE;
    //float phoSCEtaWidth;
    //float phoSCPhiWidth;
    //float rho2012;
    //float phoPFPhoIso;
    //float phoPFChIso;
    //float phoPFChIsoWorst;
    //float phoPFPhoIsoPtRhoCorr;
    //float phoPFNeuIsoPtRhoCorr;
    //float phoPFChIsoPtRhoCorr;
    //float phoHoverE12;
    //float phoEt;
    //float phoEta;

    //// Additional EE
    //float phoESEnToRawE;
    //float phoESEffSigmaRR;

    float ph_r9;
    float ph_sigmaIEIE;
    float ph_sigmaIEIP;
    float ph_s4ratio;
    float ph_s13;
    float ph_s25;
    float ph_SCetaWidth;
    float ph_SCphiWidth;
    float ph_phoIsoCorr;
    float ph_chIsoCorr;
    float ph_pfChIsoWorst;
};

#endif
