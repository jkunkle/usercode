#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


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
        bool FilterEvent         ( ModuleConfig & config ) const;

};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    //Examples
    //

    Int_t HLT_DoublePhoton70_v1;
    Int_t HLT_TriPhoton302020NonIso_v0;
    Int_t HLT_TriPhoton20NonIso_v0;
    Int_t HLT_Photon33_v1;
    Int_t HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v7;
    Int_t HLT_Diphoton30_22NonIso;
    Int_t HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_NoPixelVeto_Mass55_v7;
    Int_t HLT_TriPhoton20NonIsoNoHE_v0;
    Int_t HLT_TkMu17_v2;
    Int_t HLT_TkMu27_v6;
    Int_t HLT_TriPhoton20CaloIdLCaloIsoM_v0;
    Int_t HLT_Photon50_R9Id90_HE10_IsoM_v9;
    Int_t HLT_TriPhoton20CaloIsoM_v0;
    Int_t HLT_TriPhoton302020NonIsoNoHE_v0;
    Int_t HLT_TriPhoton404010NonIso_v0;
    Int_t HLT_Mu27_v6;
    Int_t HLT_TriPhoton20CaloIdL_v0;
    Int_t HLT_TriPhoton35355NonIso_v0;
    Int_t HLT_Mu12Diphoton20NonIso_v0;
    Int_t HLT_Mu12Diphoton25_20NonIso_v0;
    Int_t HLT_Mu12Diphoton30_25NonIso_v0;
    Int_t HLT_SinglePhoton30HiggsCaloId_v0;
    Int_t HLT_SinglePhoton30HiggsCaloIsoId_v0;
    Int_t HLT_SinglePhoton30HiggsCaloIso_v0;
    Int_t HLT_SinglePhoton30NonIso_v0;
    Int_t HLT_SinglePhoton30R9Id_v0;
    Int_t HLT_SinglePhoton30CaloIdL_v0;

    Int_t HLT_Mu12_v6;
    Int_t HLT_Mu6DoubleEG17TEST4_v0;
    Int_t HLT_Mu6DoubleEG17TESTOnlyMuDiEG_v0;
    Int_t HLT_Mu6DoubleEG17TEST3_v0;
    Int_t HLT_Mu6DoubleEG17TEST5_v0;
    Int_t HLT_Mu6DoubleEG17TEST2_v0;
    Int_t HLT_Mu6DoubleEG17TEST1_v0;
    Int_t HLT_IsoMu27_v8;
    Int_t HLT_IsoMu27TEST1_v0;
    Int_t HLT_IsoMu27TEST2_v0;
    Int_t HLT_IsoTkMu27_v8;
    Int_t HLT_Mu30_TkMu0_Onia_v1;

};

#endif
