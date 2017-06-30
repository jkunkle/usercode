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
        void MakeGJNtuple ( ModuleConfig & config ) const;
        void MakeZmumuNtuple ( ModuleConfig & config ) const;
        void MakeWmunuNtuple ( ModuleConfig & config ) const;
        void MakeQCDNtuple ( ModuleConfig & config ) const;
        bool FilterEvent         ( ModuleConfig & config ) const;

        void FillProbe ( int idx ) const;

        TTree * outtree;
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    Float_t tagph_pt                     ;
    Float_t tagph_eta                    ;
    Float_t tagph_phi                    ;
    Float_t tagph_e                      ;
    Float_t tagph_sigmaIEIE              ;
    Float_t tagph_chHadIso               ;
    Float_t tagph_neuHadIso              ;
    Float_t tagph_phoIso                 ;
    Bool_t tagph_IsEB                   ;
    Bool_t tagph_IsEE                   ;
    Bool_t tagph_passSIEIEMedium        ;
    Bool_t tagph_passChIsoCorrMedium    ;
    Bool_t tagph_passNeuIsoCorrMedium   ;
    Bool_t tagph_passPhoIsoCorrMedium   ;
    Bool_t tagph_truthMatch_ph          ;
    Bool_t tagph_truthMatchMotherPID_ph ;
    Bool_t tagph_truthMatch_el          ;

    Float_t tagll_mll                   ;
    Float_t tagll_pt1                   ;
    Float_t tagll_pt2                   ;

    Float_t tagl_mt                     ;
    Float_t tagl_pt1                    ;
    Float_t tagl_met                    ;

    Float_t probeph_n                    ;
    Float_t probeph_pt                   ;
    Float_t probeph_eta                  ;
    Float_t probeph_phi                  ;
    Float_t probeph_e                    ;
    Float_t probeph_sigmaIEIE            ;
    Float_t probeph_chHadIso             ;
    Float_t probeph_neuHadIso            ;
    Float_t probeph_phoIso               ;
    Bool_t probeph_IsEB                 ;
    Bool_t probeph_IsEE                 ;
    Bool_t probeph_passSIEIEMedium      ;
    Bool_t probeph_passChIsoCorrMedium  ;
    Bool_t probeph_passNeuIsoCorrMedium ;
    Bool_t probeph_passPhoIsoCorrMedium ;
    Bool_t probeph_truthMatch_ph        ;
    Bool_t probeph_truthMatchMotherPID_ph ;
    Bool_t probeph_truthMatch_el        ;
};

#endif
