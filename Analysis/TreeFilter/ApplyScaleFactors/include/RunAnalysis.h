#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"
#include "include/BranchDefs.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TGraphAsymmErrors.h"
#include "TH2F.h"

// The RunModule inherits from RunModuleBase (an Abstract Base Class )
// defined in the Core package so that all
// RunModules present a common interface in a Run function
// This allows the code defined in this package
// to be run from the Core package to minimize
// code duplication in each module
//

struct ValWithErr {

    float val;
    float err_up;
    float err_dn;

};

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
        void AddElectronSF ( ModuleConfig & config ) const;
        void AddMuonSF     ( ModuleConfig & config ) const;
        void AddPhotonSF   ( ModuleConfig & config ) const;
        void AddPileupSF   ( ModuleConfig & config ) const;
        void AddMETUncert   ( ModuleConfig & config ) const;

        ValWithErr GetValsFromGraph( const TGraphAsymmErrors *, float pt, bool debug=true ) const;
        float calc_pu_weight( float puval, float mod=1.0 ) const;


    private :

        TFile *_sffile_mu_iso;
        TFile *_sffile_mu_id;
        TFile *_sffile_mu_trig;
        TFile *_sffile_pileup_data;
        TFile *_sffile_pileup_mc;

        TGraphAsymmErrors *_sfgraph_mu_iso_barrel;
        TGraphAsymmErrors *_sfgraph_mu_iso_trans;
        TGraphAsymmErrors *_sfgraph_mu_iso_endcap1;
        TGraphAsymmErrors *_sfgraph_mu_iso_endcap2;

        TGraphAsymmErrors *_sfgraph_mu_id_barrel;
        TGraphAsymmErrors *_sfgraph_mu_id_trans;
        TGraphAsymmErrors *_sfgraph_mu_id_endcap1;
        TGraphAsymmErrors *_sfgraph_mu_id_endcap2;

        TGraphAsymmErrors *_sfgraph_mu_trig_barrel;
        TGraphAsymmErrors *_sfgraph_mu_trig_trans;
        TGraphAsymmErrors *_sfgraph_mu_trig_endcap;

        TFile *_sffile_el_id;
        TFile *_sffile_el_trig;


        TH2F *_sfhist_el_trig;


        TFile *_sffile_ph_id;
        TFile *_sffile_ph_eveto;
        TFile *_sffile_ph_eveto_highpt;

        TH2F *_sfhist_ph_id;
        TH2F *_sfhist_ph_eveto;
        TH2F *_sfhist_ph_eveto_highpt;

        TH1D *_sfhist_pileup_data;
        TH1F *_sfhist_pileup_mc;



};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

#ifdef MODULE_AddElectronSF
    float el_trigSF;
    float el_trigSFUP;
    float el_trigSFDN;
#endif

#ifdef MODULE_AddPhotonSF
    float ph_idSF;
    float ph_idSFUP;
    float ph_idSFDN;

    float ph_evetoSF;
    float ph_evetoSFUP;
    float ph_evetoSFDN;
#endif

#ifdef MODULE_AddMuonSF
    float mu_trigSF;
    float mu_trigSFUP;
    float mu_trigSFDN;

    float mu_isoSF;
    float mu_isoSFUP;
    float mu_isoSFDN;

    float mu_idSF;
    float mu_idSFUP;
    float mu_idSFDN;
#endif

#ifdef MODULE_AddPileupSF

#ifndef EXISTS_PUWeightUP5
    float PUWeightUP5;
#endif
#ifndef EXISTS_PUWeightUP10
    float PUWeightUP10;
#endif
#ifndef EXISTS_PUWeightDN5
    float PUWeightDN5;
#endif
#ifndef EXISTS_PUWeightDN10
    float PUWeightDN10;
#endif
#ifndef EXISTS_PUWeight
    float PUWeight;
#endif
#endif


    //Examples
};

#endif
