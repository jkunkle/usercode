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
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & configs) ;
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
        void FilterJet         ( ModuleConfig & config ) const;
        void FilterElectron    ( ModuleConfig & config ) const;
        void FilterPhoton      ( ModuleConfig & config ) const;
        void FilterMuon        ( ModuleConfig & config ) const;
        void SortPhotonByMVAScore( ModuleConfig & config ) const;
        void BuildTruth        ( ModuleConfig & config ) const;
        void CalcEventVars     ( ModuleConfig & config ) const;
        bool FilterEvent       ( ModuleConfig & config ) const;
        bool FilterBlind       ( ModuleConfig & config ) const;
        bool FilterTruth       ( ModuleConfig & config ) const;

        std::vector<int> get_ph_sorted_by_id() const;

    private :
        bool _isData;
        bool sort_photons_by_id;
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

    Float_t trueleadlep_leadPhotDR;
    Float_t trueleadlep_sublPhotDR;
    Float_t truesubllep_leadPhotDR;
    Float_t truesubllep_sublPhotDR;

    Bool_t isBlinded;
    Float_t EventWeight;

    Int_t   mu_pt25_n;
    Int_t   mu_passtrig_n;
    Int_t   mu_passtrig25_n;
    Int_t   el_pt25_n;
    Int_t   el_passtrig_n;
    Int_t   el_passtrig28_n;
    Int_t   ph_mediumNoSIEIE_n;
    Int_t   ph_medium_n;
    Int_t   ph_mediumNoEleVeto_n;
    Int_t   ph_mediumNoSIEIENoEleVeto_n;
    Int_t   ph_mediumNoIso_n;
    Int_t   ph_mediumNoChIso_n;
    Int_t   ph_mediumNoNeuIso_n;
    Int_t   ph_mediumNoPhoIso_n;
    Int_t   ph_mediumNoChIsoNoNeuIso_n;
    Int_t   ph_mediumNoChIsoNoPhoIso_n;
    Int_t   ph_mediumNoNeuIsoNoPhoIso_n;
    Int_t   ph_iso533_n;
    Int_t   ph_iso855_n;
    Int_t   ph_iso1077_n;
    Int_t   ph_iso1299_n;
    Int_t   ph_iso151111_n;
    Int_t   ph_iso201616_n;
    std::vector<Bool_t>  *ph_trigMatch_el;
    std::vector<float>  *ph_elMinDR;

    Float_t leadPhot_pt;
    Float_t sublPhot_pt;
    Float_t leadPhot_lepDR;
    Float_t sublPhot_lepDR;
    Float_t ph_phDR;
    Float_t phPhot_lepDR;
    Float_t leadPhot_lepDPhi;
    Float_t sublPhot_lepDPhi;
    Float_t ph_phDPhi;
    Float_t phPhot_lepDPhi;
    Float_t dphi_met_lep1;
    Float_t dphi_met_lep2;
    Float_t dphi_met_ph1;
    Float_t dphi_met_ph2;
    Float_t mt_lep_met;
    Float_t mt_lepph1_met;
    Float_t mt_lepph2_met;
    Float_t mt_lepphph_met;
    Float_t m_leplep;
    Float_t m_leplep_uncorr;
    Float_t m_lepph1;
    Float_t m_lepph2;
    Float_t m_leplepph;
    Float_t m_lepphph;
    Float_t m_phph;
    Float_t m_leplepZ;
    Float_t m_3lep;
    Float_t m_4lep;
    Float_t pt_phph;
    Float_t pt_leplep;
    Float_t pt_lepph1;
    Float_t pt_lepph2;
    Float_t pt_lepphph;
    Float_t pt_leplepph;
    Float_t pt_secondLepton;
    Float_t pt_thirdLepton;

    Float_t            leadPhot_leadLepDR;
    Float_t            leadPhot_sublLepDR;
    Float_t            sublPhot_leadLepDR;
    Float_t            sublPhot_sublLepDR;
    // variables that explicity use
    // the default photon order 
    Float_t            dr_ph1_leadLep;
    Float_t            dr_ph1_sublLep;
    Float_t            dr_ph2_leadLep;
    Float_t            dr_ph2_sublLep;
    Float_t            m_ph1_ph2;
    Float_t            dr_ph1_ph2;
    Float_t            dphi_ph1_ph2; 
    Float_t            pt_ph1_ph2; 
    Float_t            m_leadLep_ph1_ph2; 
    Float_t            m_leadLep_ph1; 
    Float_t            m_leadLep_ph2; 
    Float_t            pt_leadph12;
    Float_t            pt_sublph12;
    Float_t            sieie_leadph12;
    Float_t            sieie_sublph12;
    Float_t            chIsoCorr_leadph12;
    Float_t            chIsoCorr_sublph12;
    Float_t            neuIsoCorr_leadph12;
    Float_t            neuIsoCorr_sublph12;
    Float_t            phoIsoCorr_leadph12;
    Float_t            phoIsoCorr_sublph12;

    Bool_t             isEB_leadph12;
    Bool_t             isEE_leadph12;
    Bool_t             isEB_sublph12;
    Bool_t             isEE_sublph12;


    Float_t m_nearestToZ;
    Float_t m_minZdifflepph;

    //Examples
};

#endif
