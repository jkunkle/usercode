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
#include "TRandom3.h"
#include "external/CMSSW_5_3_28/src/CondFormats/JetMETObjects/interface/SimpleJetResolution.h"
#include "external/CMSSW_5_3_28/src/CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

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

        void GetTruthJets( std::vector<TLorentzVector> & jets) const;
        void GetJetsJER( const std::vector<int> &jets_index, const std::string &var, std::vector<TLorentzVector> &out_jets ) const;
        void GetJetsJES( const std::vector<int> &jets_index, const std::string &var, std::vector<TLorentzVector> &out_jets ) const;
        float FindJetJERCorr( const std::string &up_dn, float eta) const;
        float FindJetJERCorr( const std::vector<std::pair< std::pair<float, float>, float > > & corrs, float eta) const;

        void GetElectronsScaled( const std::vector<int> &eles_index, const std::string &var, std::vector<TLorentzVector> &out_eles ) const;
        void GetPhotonsScaled  ( const std::vector<int> &phots_index, const std::string &var, std::vector<TLorentzVector> &out_phots ) const;
        void GetMuonsScaled    ( const std::vector<int> &muons_index, const std::string &var, std::vector<TLorentzVector> &out_muons ) const;

        void GetNewMet( const std::vector<TLorentzVector> &objs_to_remove, const std::vector<TLorentzVector> &objs_to_add, TLorentzVector & met_orig ) const ;
        void GetUnClusNewMet( const std::vector<TLorentzVector> &hard_objs, float var, TLorentzVector & met_orig ) const ;

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

        std::vector<std::pair<std::pair<float, float>, float > > jet_res_corr_dn;
        std::vector<std::pair<std::pair<float, float>, float > > jet_res_corr_up;

        JetCorrectorParameters *AK5PFCHSPar;
        JetCorrectorParameters *AK5PFPar;
        SimpleJetResolution *ak5PFResolution;
        SimpleJetResolution *ak5PFCHSResolution;

        TRandom3 * rand;



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

#ifdef MODULE_AddMETUncert
    float pfType01METUncertMuonUP;
    float pfType01METUncertMuonDN;
    float pfType01METUncertEMUP;
    float pfType01METUncertEMDN;
    float pfType01METUncertJESUP;
    float pfType01METUncertJESDN;
    float pfType01METUncertJERUP;
    float pfType01METUncertJERDN;
    float pfType01METUncertUnClusUP;
    float pfType01METUncertUnClusDN;

    float mt_lep_metUncertMuonUP;
    float mt_lep_metUncertMuonDN;
    float mt_lep_metUncertEMUP;
    float mt_lep_metUncertEMDN;
    float mt_lep_metUncertJESUP;
    float mt_lep_metUncertJESDN;
    float mt_lep_metUncertJERUP;
    float mt_lep_metUncertJERDN;
    float mt_lep_metUncertUnClusUP;
    float mt_lep_metUncertUnClusDN;

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
