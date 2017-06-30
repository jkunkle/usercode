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
        void BuildMCMuon         ( ModuleConfig & config ) const;
        void BuildMCElectron     ( ModuleConfig & config ) const;
        void BuildMCPhoton       ( ModuleConfig & config ) const;
        bool FilterEvent         ( ModuleConfig & config ) const;

        void CalcCommonVars       ( ) const;

    TTree* outtree;

};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    Float_t muprobe_pt; 
    Float_t muprobe_eta; 
    Float_t muprobe_phi; 
    Bool_t muprobe_passTight; 
    Int_t truemu_n; 
    Float_t truemu_pt; 
    Float_t truemu_eta; 
    Float_t truemu_phi; 

    Float_t elprobe_pt; 
    Float_t elprobe_eta; 
    Float_t elprobe_phi; 
    Bool_t elprobe_passTight; 
    Bool_t elprobe_passMedium; 
    Bool_t elprobe_passLoose; 
    Int_t trueel_n; 
    Float_t trueel_pt; 
    Float_t trueel_eta; 
    Float_t trueel_phi; 

    Float_t phprobe_pt; 
    Float_t phprobe_eta; 
    Float_t phprobe_phi; 
    Bool_t phprobe_passTight; 
    Bool_t phprobe_passMedium; 
    Bool_t phprobe_passLoose; 
    Bool_t phprobe_eleVeto; 
    Bool_t phprobe_hasPixSeed; 
    Int_t truephot_n; 
    Float_t truephot_pt; 
    Float_t truephot_eta; 
    Float_t truephot_phi; 

    Bool_t hasTruthMatch; 
    Bool_t passTrig_IsoMu24;
    Bool_t passTrig_IsoTkMu24;
    Bool_t passTrig_Ele27_eta2p1_WPTight_Gsf;
    Bool_t passTrig_Mu17_Photon30_CaloIdL_L1ISO;
    Float_t recomet_pt;
    Float_t truemet_pt;

};

#endif
