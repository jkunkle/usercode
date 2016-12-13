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

        bool ApplyModule         ( ModuleConfig & config ) const;

        void FilterJet         ( ModuleConfig & config ) const;
        void FilterElectron    ( ModuleConfig & config ) const;
        void FilterPhoton      ( ModuleConfig & config ) const;
        void FilterMuon        ( ModuleConfig & config ) const;
        void BuildTruth        ( ModuleConfig & config ) const;
        void CalcEventVars     ( ModuleConfig & config ) const;
        bool FilterEvent       ( ModuleConfig & config ) const;
        bool FilterBlind       ( ModuleConfig & config ) const;
        bool FilterTruth       ( ModuleConfig & config ) const;


};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    Int_t truelep_n        ;
    Int_t trueph_n         ;
    Int_t trueW_n         ;
    Int_t trueph_wmother_n ;
    Int_t truegenph_n ;
    Int_t truegenphpt15_n;

    Int_t truegenphpt15WZMom_n;
    Int_t truegenphpt15LepMom_n;
    Int_t truegenphpt15QMom_n;

    std::vector<float>  *truelep_pt        ;
    std::vector<float>  *truelep_eta       ;
    std::vector<float>  *truelep_phi       ;
    std::vector<float>  *truelep_e       ;
    std::vector<Bool_t> *truelep_isElec    ;
    std::vector<Bool_t> *truelep_isMuon   ;
    std::vector<int>    *truelep_motherPID;

    std::vector<float>  *trueph_pt       ;
    std::vector<float>  *trueph_eta      ;
    std::vector<float>  *trueph_phi      ;
    std::vector<int>    *trueph_motherPID  ;
    std::vector<int>    *trueph_parentage;
    std::vector<float>  *trueph_nearestLepDR ;
    std::vector<float>  *trueph_nearestQrkDR ;

   

    std::vector<float>  *trueW_pt       ;
    std::vector<float>  *trueW_eta      ;
    std::vector<float>  *trueW_phi      ;
    std::vector<float>  *trueW_e        ;

    Float_t trueleadlep_pt;
    Float_t truesubllep_pt;
    Float_t true_m_leplep;

    Float_t trueleadlep_leadPhotDR;
    Float_t trueleadlep_sublPhotDR;
    Float_t truesubllep_leadPhotDR;
    Float_t truesubllep_sublPhotDR;

    Float_t truephph_dr;
    Float_t truephph_dphi;
    Float_t truephph_m;
    Float_t truelepphph_m;

    Bool_t isBlinded;
    Float_t EventWeight;

    Int_t   mu_pt25_n;
    Int_t   mu_passtrig_n;
    Int_t   mu_passtrig25_n;
    Int_t   el_pt25_n;
    Int_t   el_passtrig_n;
    Int_t   el_passtrig28_n;

    Int_t   ph_mediumNoSIEIENoEleVeto_n;
    Int_t   ph_mediumNoSIEIEPassPSV_n;
    Int_t   ph_mediumNoSIEIEFailPSV_n;
    Int_t   ph_mediumNoSIEIEPassCSEV_n;
    Int_t   ph_mediumNoSIEIEFailCSEV_n;
    Int_t   ph_mediumNoEleVeto_n;
    Int_t   ph_mediumPassPSV_n;
    Int_t   ph_mediumFailPSV_n;
    Int_t   ph_mediumPassCSEV_n;
    Int_t   ph_mediumFailCSEV_n;
    Int_t   ph_mediumNoChIsoNoEleVeto_n;
    Int_t   ph_mediumNoChIsoNoSIEIENoEleVeto_n;
    Int_t   ph_mediumNoChIsoPassPSV_n;
    Int_t   ph_mediumNoChIsoFailPSV_n;
    Int_t   ph_mediumNoChIsoPassCSEV_n;
    Int_t   ph_mediumNoChIsoFailCSEV_n;
    Int_t   ph_mediumNoNeuIsoNoEleVeto_n;
    Int_t   ph_mediumNoNeuIsoPassPSV_n;
    Int_t   ph_mediumNoNeuIsoFailPSV_n;
    Int_t   ph_mediumNoNeuIsoPassCSEV_n;
    Int_t   ph_mediumNoNeuIsoFailCSEV_n;
    Int_t   ph_mediumNoPhoIsoNoEleVeto_n;
    Int_t   ph_mediumNoPhoIsoPassPSV_n;
    Int_t   ph_mediumNoPhoIsoFailPSV_n;
    Int_t   ph_mediumNoPhoIsoPassCSEV_n;
    Int_t   ph_mediumNoPhoIsoFailCSEV_n;

    Float_t mt_lep_met;
    Float_t dphi_met_lep1;
    Float_t dphi_met_lep2;
    Float_t m_leplep;
    Float_t m_mumu;
    Float_t m_elel;
    Float_t pt_leplep;
    Float_t m_3lep;
    Float_t m_4lep;

    std::vector<float> *dphi_met_phot;
    std::vector<float> *m_leadLep_phot;
    std::vector<float> *m_sublLep_phot;
    std::vector<float> *dr_leadLep_phot;
    std::vector<float> *dr_sublLep_phot;
    std::vector<float> *dphi_leadLep_phot;
    std::vector<float> *dphi_sublLep_phot;
    std::vector<float> *m_leplep_phot;
    std::vector<float> *m_diphot;
    std::vector<float> *dr_diphot;
    std::vector<float> *dphi_diphot;
    std::vector<float> *pt_diphot;
    std::vector<float> *m_leplep_diphot;

    std::vector<int> *ptSorted_ph_mediumNoSIEIENoEleVeto_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIEPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIEFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIEPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIEFailCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoEleVeto_idx;
    std::vector<int> *ptSorted_ph_mediumPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumFailCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoNoEleVeto_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoNoSIEIENoEleVeto_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoFailCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoFailCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoFailCSEV_idx;

};

#endif
