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

        TTree * _outtree;

};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    float                ph_pt;
    float                ph_eta;
    float                ph_sceta;
    float                ph_phi;
    float                ph_e;
    float                ph_HoverE;
    float                ph_HoverE12;
    float                ph_sigmaIEIE;
    float                ph_sigmaIEIP;
    float                ph_r9;
    float                ph_E1x3;
    float                ph_E2x2;
    float                ph_E5x5;
    float                ph_E2x5Max;
    float                ph_SCetaWidth;
    float                ph_SCphiWidth;
    float                ph_ESEffSigmaRR;
    float                ph_hcalIsoDR03;
    float                ph_trkIsoHollowDR03;
    float                ph_chgpfIsoDR02;
    float                ph_pfChIsoWorst;
    float                ph_chIso;
    float                ph_neuIso;
    float                ph_phoIso;
    float                ph_chIsoCorr;
    float                ph_neuIsoCorr;
    float                ph_phoIsoCorr;
    bool                ph_eleVeto;
    bool                ph_hasPixSeed;
    float                ph_drToTrk;
    bool                ph_isConv;
    int                ph_conv_nTrk;
    float                ph_conv_vtx_x;
    float                ph_conv_vtx_y;
    float                ph_conv_vtx_z;
    float                ph_conv_ptin1;
    float                ph_conv_ptin2;
    float                ph_conv_ptout1;
    float                ph_conv_ptout2;
    bool                ph_passTight;
    bool                ph_passMedium;
    bool                ph_passLoose;
    bool                ph_passLooseNoSIEIE;
    bool                ph_passSIEIELoose;
    bool                ph_passSIEIEMedium;
    bool                ph_passSIEIETight;
    bool                ph_passChIsoCorrLoose;
    bool                ph_passChIsoCorrMedium;
    bool                ph_passChIsoCorrTight;
    bool                ph_passNeuIsoCorrLoose;
    bool                ph_passNeuIsoCorrMedium;
    bool                ph_passNeuIsoCorrTight;
    bool                ph_passPhoIsoCorrLoose;
    bool                ph_passPhoIsoCorrMedium;
    bool                ph_passPhoIsoCorrTight;
    bool                ph_truthMatch_el;
    float                ph_truthMinDR_el;
    float                ph_truthMatchPt_el;
    bool                ph_truthMatch_ph;
    float                ph_truthMinDR_ph;
    float                ph_truthMatchPt_ph;
    int                         ph_truthMatchMotherPID_ph;
    bool                ph_hasSLConv;
    bool                ph_pass_mva_presel;
    float                ph_mvascore;
    bool                ph_IsEB;
    bool                ph_IsEE;

    float               ph_s13;
    float               ph_s4ratio;
    float               ph_s25;
};

#endif
