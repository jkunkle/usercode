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

        RunModule();

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

        bool _doMuPtScaleDown;
        bool _doMuPtScaleUp;
        bool _doElPtScaleDown;
        bool _doElPtScaleUp;
        bool _doPhPtScaleDown;
        bool _doPhPtScaleUp;

        float _muPtScaleDownBarrel;
        float _muPtScaleDownEndcap;
        float _muPtScaleUpBarrel;
        float _muPtScaleUpEndcap;

        float _elPtScaleDownBarrel;
        float _elPtScaleDownEndcap;
        float _elPtScaleUpBarrel;
        float _elPtScaleUpEndcap;

        float _phPtScaleDownBarrel;
        float _phPtScaleDownEndcap;
        float _phPtScaleUpBarrel;
        float _phPtScaleUpEndcap;

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
    Int_t   el_passtrigL_n;
    Int_t   el_passtrig28_n;
    Int_t   ph_noSIEIEiso533_n;
    Int_t   ph_noSIEIEiso855_n;
    Int_t   ph_noSIEIEiso1077_n;
    Int_t   ph_noSIEIEiso1299_n;
    Int_t   ph_noSIEIEiso151111_n;
    Int_t   ph_noSIEIEiso201616_n;
    Int_t   ph_passSIEIEiso53None_n;
    Int_t   ph_passSIEIEiso85None_n;
    Int_t   ph_passSIEIEiso107None_n;
    Int_t   ph_passSIEIEiso129None_n;
    Int_t   ph_passSIEIEiso1511None_n;
    Int_t   ph_passSIEIEiso2016None_n;
    Int_t   ph_passSIEIEiso5None3_n;
    Int_t   ph_passSIEIEiso8None5_n;
    Int_t   ph_passSIEIEiso10None7_n;
    Int_t   ph_passSIEIEiso12None9_n;
    Int_t   ph_passSIEIEiso15None11_n;
    Int_t   ph_passSIEIEiso20None16_n;
    Int_t   ph_passSIEIEisoNone33_n;
    Int_t   ph_passSIEIEisoNone55_n;
    Int_t   ph_passSIEIEisoNone77_n;
    Int_t   ph_passSIEIEisoNone99_n;
    Int_t   ph_passSIEIEisoNone1111_n;
    Int_t   ph_passSIEIEisoNone1616_n;
    Int_t   ph_failSIEIEiso53None_n;
    Int_t   ph_failSIEIEiso85None_n;
    Int_t   ph_failSIEIEiso107None_n;
    Int_t   ph_failSIEIEiso129None_n;
    Int_t   ph_failSIEIEiso1511None_n;
    Int_t   ph_failSIEIEiso2016None_n;
    Int_t   ph_failSIEIEiso5None3_n;
    Int_t   ph_failSIEIEiso8None5_n;
    Int_t   ph_failSIEIEiso10None7_n;
    Int_t   ph_failSIEIEiso12None9_n;
    Int_t   ph_failSIEIEiso15None11_n;
    Int_t   ph_failSIEIEiso20None16_n;
    Int_t   ph_failSIEIEisoNone33_n;
    Int_t   ph_failSIEIEisoNone55_n;
    Int_t   ph_failSIEIEisoNone77_n;
    Int_t   ph_failSIEIEisoNone99_n;
    Int_t   ph_failSIEIEisoNone1111_n;
    Int_t   ph_failSIEIEisoNone1616_n;
    Int_t   ph_mediumNoNeuIsoNoPhoIso_n;
    Int_t   ph_mediumNoChIsoNoPhoIso_n;
    Int_t   ph_mediumNoChIsoNoNeuIso_n;
    Int_t   ph_mediumNoSIEIENoChIso_n ;
    Int_t   ph_mediumNoSIEIENoPhoIsoNoEleVeto_n;
    Int_t   ph_mediumNoSIEIENoNeuIsoNoEleVeto_n;
    Int_t   ph_mediumNoSIEIENoChIsoNoEleVeto_n ;
    Int_t   ph_mediumNoSIEIENoPhoIsoPassPSV_n  ;
    Int_t   ph_mediumNoSIEIENoNeuIsoPassPSV_n  ;
    Int_t   ph_mediumNoSIEIENoChIsoPassPSV_n   ;
    Int_t   ph_mediumNoSIEIENoPhoIsoFailPSV_n  ;
    Int_t   ph_mediumNoSIEIENoNeuIsoFailPSV_n  ;
    Int_t   ph_mediumNoSIEIENoChIsoFailPSV_n   ;
    Int_t   ph_mediumNoSIEIENoPhoIsoPassCSEV_n ;
    Int_t   ph_mediumNoSIEIENoNeuIsoPassCSEV_n ;
    Int_t   ph_mediumNoSIEIENoChIsoPassCSEV_n  ;
    Int_t   ph_mediumNoSIEIENoPhoIsoFailCSEV_n ;
    Int_t   ph_mediumNoSIEIENoNeuIsoFailCSEV_n ;
    Int_t   ph_mediumNoSIEIENoChIsoFailCSEV_n  ;
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

    std::vector<Bool_t>  *ph_trigMatch_el;
    std::vector<float>  *ph_elMinDR;

    Float_t leadPhot_sublPhotDR;
    Float_t leadPhot_sublPhotDPhi;
    Float_t phPhot_lepDPhi;
    Float_t dphi_met_lep1;
    Float_t dphi_met_lep2;
    Float_t dphi_met_ph1;
    Float_t dphi_met_ph2;
    Float_t mt_lep_met;
    Float_t mt_lepph1_met;
    Float_t mt_lepph2_met;
    Float_t mt_lepphph_met;
    Float_t mt_trigel_met;
    Float_t mt_trigmu_met;
    Float_t m_leplep;
    Float_t m_mumu;
    Float_t m_elel;
    Float_t m_leplep_uncorr;
    Float_t m_lepph1;
    Float_t m_lepph2;
    Float_t m_trigelph1;
    Float_t m_trigelph2;
    Float_t m_lep2ph1;
    Float_t m_lep2ph2;
    Float_t m_lepphlead;
    Float_t m_lepphsubl;
    Float_t m_lep2phlead;
    Float_t m_lep2phsubl;
    Float_t m_leplepph;
    Float_t m_leplepphph;
    Float_t m_leplepph1;
    Float_t m_leplepph2;
    Float_t m_lepphph;
    Float_t m_trigelphph;
    Float_t m_phph;
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
    Float_t            leadPhot_trigElDR;
    Float_t            sublPhot_trigElDR;
    Float_t            leadPhot_trigMuDR;
    Float_t            sublPhot_trigMuDR;
    Float_t            m_leadPhot_leadLep;
    Float_t            m_leadPhot_trigEl;
    Float_t            m_sublPhot_leadLep;
    Float_t            m_sublPhot_trigEl;
    Float_t            m_leadPhot_sublPhot_trigEl;
    Float_t            dphi_met_leadPhot;
    Float_t            dphi_met_sublPhot;
    // variables that explicity use
    // the default photon order 
    Float_t            dr_ph1_leadLep;
    Float_t            dr_ph1_sublLep;
    Float_t            dr_ph2_leadLep;
    Float_t            dr_ph2_sublLep;
    Float_t            dr_ph1_trigEle;
    Float_t            dr_ph2_trigEle;
    Float_t            dr_ph1_trigMu;
    Float_t            dr_ph2_trigMu;
    Float_t            dphi_ph1_leadLep;
    Float_t            dphi_ph1_sublLep;
    Float_t            dphi_ph2_leadLep;
    Float_t            dphi_ph2_sublLep;
    Float_t            m_ph1_ph2;
    Float_t            dr_ph1_ph2;
    Float_t            dphi_ph1_ph2; 
    Float_t            pt_ph1_ph2; 
    Float_t            m_leadLep_ph1_ph2; 
    Float_t            m_leadLep_ph1; 
    Float_t            m_leadLep_ph2; 
    Float_t            m_sublLep_ph1; 
    Float_t            m_sublLep_ph2; 
    Float_t            pt_leadph12;
    Float_t            pt_sublph12;
    Float_t            eta_leadph12;
    Float_t            eta_sublph12;
    Float_t            hasPixSeed_leadph12;
    Float_t            hasPixSeed_sublph12;
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
    Bool_t             truthMatchPh_leadph12;
    Bool_t             truthMatchPh_sublph12;
    Bool_t             truthMatchPhMomPID_leadph12;
    Bool_t             truthMatchPhMomPID_sublph12;

    std::vector<float> *dphi_met_phot;
    std::vector<float> *m_leadLep_phot;
    std::vector<float> *m_sublLep_phot;
    std::vector<float> *m_trigEl_phot;
    std::vector<float> *m_trigMu_phot;
    std::vector<float> *dr_leadLep_phot;
    std::vector<float> *dr_sublLep_phot;
    std::vector<float> *dr_trigEl_phot;
    std::vector<float> *dr_trigMu_phot;
    std::vector<float> *dphi_leadLep_phot;
    std::vector<float> *dphi_sublLep_phot;
    std::vector<float> *dphi_trigEl_phot;
    std::vector<float> *dphi_trigMu_phot;
    std::vector<float> *mt_met_trigEl_phot;
    std::vector<float> *mt_met_trigMu_phot;
    std::vector<float> *m_leplep_phot;
    std::vector<float> *m_diphot;
    std::vector<float> *dr_diphot;
    std::vector<float> *dphi_diphot;
    std::vector<float> *pt_diphot;
    std::vector<float> *m_leplep_diphot;
    std::vector<float> *m_trigEl_diphot;
    std::vector<float> *m_trigMu_diphot;
    std::vector<float> *mt_met_trigEl_diphot;
    std::vector<float> *mt_met_trigMu_diphot;


    std::vector<int> *ptSorted_ph_noSIEIEiso533_idx;
    std::vector<int> *ptSorted_ph_noSIEIEiso855_idx;
    std::vector<int> *ptSorted_ph_noSIEIEiso1077_idx;
    std::vector<int> *ptSorted_ph_noSIEIEiso1299_idx;
    std::vector<int> *ptSorted_ph_noSIEIEiso151111_idx;
    std::vector<int> *ptSorted_ph_noSIEIEiso201616_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso53None_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso85None_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso107None_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso129None_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso1511None_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso2016None_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso5None3_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso8None5_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso10None7_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso12None9_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso15None11_idx;
    std::vector<int> *ptSorted_ph_passSIEIEiso20None16_idx;
    std::vector<int> *ptSorted_ph_passSIEIEisoNone33_idx;
    std::vector<int> *ptSorted_ph_passSIEIEisoNone55_idx;
    std::vector<int> *ptSorted_ph_passSIEIEisoNone77_idx;
    std::vector<int> *ptSorted_ph_passSIEIEisoNone99_idx;
    std::vector<int> *ptSorted_ph_passSIEIEisoNone1111_idx;
    std::vector<int> *ptSorted_ph_passSIEIEisoNone1616_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso53None_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso85None_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso107None_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso129None_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso1511None_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso2016None_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso5None3_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso8None5_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso10None7_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso12None9_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso15None11_idx;
    std::vector<int> *ptSorted_ph_failSIEIEiso20None16_idx;
    std::vector<int> *ptSorted_ph_failSIEIEisoNone33_idx;
    std::vector<int> *ptSorted_ph_failSIEIEisoNone55_idx;
    std::vector<int> *ptSorted_ph_failSIEIEisoNone77_idx;
    std::vector<int> *ptSorted_ph_failSIEIEisoNone99_idx;
    std::vector<int> *ptSorted_ph_failSIEIEisoNone1111_idx;
    std::vector<int> *ptSorted_ph_failSIEIEisoNone1616_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoNoPhoIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoNoPhoIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoNoNeuIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoChIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoPhoIsoNoEleVeto_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoNeuIsoNoEleVeto_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoChIsoNoEleVeto_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoPhoIsoPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoNeuIsoPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoChIsoPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoPhoIsoFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoNeuIsoFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoChIsoFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoPhoIsoPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoNeuIsoPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoChIsoPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoPhoIsoFailCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoNeuIsoFailCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoChIsoFailCSEV_idx;
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
