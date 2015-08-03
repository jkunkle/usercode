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
        void AddMETUncert    ( ModuleConfig & config ) const;
        void VaryEGammaScale ( ModuleConfig & config ) const;
        void VaryMuonScale   ( ModuleConfig & config ) const;


    private :

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

        std::vector<std::pair<std::pair<float, float>, float > > jet_res_corr_dn;
        std::vector<std::pair<std::pair<float, float>, float > > jet_res_corr_up;

        JetCorrectorParameters *AK5PFCHSPar;
        JetCorrectorParameters *AK5PFPar;
        SimpleJetResolution *ak5PFResolution;
        SimpleJetResolution *ak5PFCHSResolution;

        TRandom3 * rand;

        std::string _muon_var;
        std::string _egamma_var;

};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

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


    //Examples
};

#endif
