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

        void calc_corr_iso( float chIso, float phoIso, float neuIso, float rho, float eta, float &chisoCorr, float &phoIsoCorr, float &neuIsoCorr ) const;

        // Define modules below.
        void BuildElectron       ( ModuleConfig & config ) const;
        void BuildMuon           ( ModuleConfig & config ) const;
        void BuildPhoton         ( ModuleConfig & config ) const;
        void BuildJet            ( ModuleConfig & config ) const;
        void BuildMET            ( ModuleConfig & config ) const;
        void BuildTruth          ( ModuleConfig & config ) const;
        void BuildEvent          ( ModuleConfig & config ) const;
        void BuildTriggerBits    ( ModuleConfig & config ) const;
        void FilterGenPhoton     ( ModuleConfig & config ) const;
        void WeightEvent         ( ModuleConfig & config ) const;
        bool FilterElec          ( ModuleConfig & config ) const;
        bool FilterMuon          ( ModuleConfig & config ) const;
        bool FilterEvent         ( ModuleConfig & config ) const;
        bool FilterTrigger       ( ModuleConfig & config ) const;

        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR ) const;
        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR ) const;
        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR, TLorentzVector &matchLV ) const;
        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR, TLorentzVector &matchLV, int &matchMotherPID, int &matchParentage ) const;

    private :

        bool eval_mu_tight    ;
        bool eval_ph_tight    ;
        bool eval_ph_medium   ;
        bool eval_ph_loose    ;
        bool eval_el_tight    ;
        bool eval_el_medium   ;
        bool eval_el_loose    ;
        bool eval_el_veryloose;
        bool _needs_nlo_weght ;
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    Int_t              el_n;
    Int_t              mu_n;
    Int_t              ph_n;
    Int_t              jet_n;
    Int_t              vtx_n;
    Int_t              trueph_n;


    std::vector<float> *el_pt;
    std::vector<float> *el_eta;
    std::vector<float> *el_sceta;
    std::vector<float> *el_phi;
    std::vector<float> *el_e;
    std::vector<float> *el_d0pv;
    std::vector<float> *el_z0pv;
    std::vector<float> *el_sigmaIEIE;
    std::vector<float> *el_sigmaIEIEFull5x5;
    std::vector<float> *el_charge;
    std::vector<float> *el_ooEmooP;
    std::vector<int>   *el_passConvVeto;
    std::vector<float> *el_chHadIso;
    std::vector<float> *el_neuHadIso;
    std::vector<float> *el_phoIso;
    std::vector<float> *el_chHadIsoPuCorr;
    std::vector<float> *el_rawIso;
    std::vector<float> *el_dbIso;
    std::vector<float> *el_rhoIso;
    std::vector<float> *el_passTight;
    std::vector<float> *el_passMedium;
    std::vector<float> *el_passLoose;
    std::vector<float> *el_passVeryLoose;
    std::vector<Bool_t> *el_truthMatch_el;
    std::vector<float> *el_truthMinDR_el;
    std::vector<float> *el_truthMatchPt_el;
    std::vector<Bool_t> *el_truthMatch_ph;
    std::vector<float> *el_truthMinDR_ph;
    std::vector<float> *el_truthMatchPt_ph;

    std::vector<float>  *mu_pt;
    std::vector<float>  *mu_eta;
    std::vector<float>  *mu_phi;
    std::vector<float>  *mu_e;
    std::vector<Bool_t> *mu_isGlobal;
    std::vector<Bool_t> *mu_isPF;
    std::vector<float>  *mu_chi2;
    std::vector<int>    *mu_nHits;
    std::vector<int>    *mu_nMuStations;
    std::vector<int>    *mu_nPixHits;
    std::vector<int>    *mu_nTrkLayers;
    std::vector<float>  *mu_d0;
    std::vector<float>  *mu_z0;
    std::vector<float>  *mu_pfIso_ch;
    std::vector<float>  *mu_pfIso_nh;
    std::vector<float>  *mu_pfIso_pho;
    std::vector<float>  *mu_pfIso_db;
    std::vector<float>  *mu_rhoIso;
    std::vector<float>  *mu_corrIso;
    std::vector<float>  *mu_trkIso;
    std::vector<int>    *mu_charge;
    std::vector<Bool_t> *mu_triggerMatch;
    std::vector<Bool_t> *mu_triggerMatchDiMu;
    std::vector<Bool_t> *mu_passLoose;
    std::vector<Bool_t> *mu_passCustom;
    std::vector<Bool_t> *mu_passTight;
    std::vector<Bool_t> *mu_passTightNoIso;
    std::vector<Bool_t> *mu_passTightNoD0;
    std::vector<Bool_t> *mu_passTightNoIsoNoD0;
    std::vector<Bool_t> *mu_truthMatch;
    std::vector<float>  *mu_truthMinDR;

    std::vector<float>  *ph_pt;
    std::vector<float>  *ph_eta;
    std::vector<float>  *ph_sceta;
    std::vector<float>  *ph_phi;
    std::vector<float>  *ph_scphi;
    std::vector<float>  *ph_e;
    std::vector<float>  *ph_scE;
    std::vector<float>  *ph_HoverE;
    std::vector<float>  *ph_HoverE12;
    std::vector<float>  *ph_sigmaIEIE;
    std::vector<float>  *ph_sigmaIEIP;
    std::vector<float>  *ph_r9;
    std::vector<float>  *ph_E3x3;
    std::vector<float>  *ph_E1x5;
    std::vector<float>  *ph_E2x5;
    std::vector<float>  *ph_E5x5;
    std::vector<float>  *ph_SCetaWidth;
    std::vector<float>  *ph_SCphiWidth;
    std::vector<float>  *ph_ESEffSigmaRR;
    std::vector<float>  *ph_hcalIsoDR03;
    std::vector<float>  *ph_trkIsoHollowDR03;
    std::vector<float>  *ph_chgpfIsoDR02;
    std::vector<float>  *ph_pfChIsoWorst;
    std::vector<float>  *ph_chIso;
    std::vector<float>  *ph_neuIso;
    std::vector<float>  *ph_phoIso;
    std::vector<float>  *ph_chIsoCorr;
    std::vector<float>  *ph_neuIsoCorr;
    std::vector<float>  *ph_phoIsoCorr;
    std::vector<Bool_t> *ph_eleVeto;
    std::vector<Bool_t> *ph_hasPixSeed;
    std::vector<float>  *ph_drToTrk;
    std::vector<Bool_t> *ph_isConv;
    std::vector<int>    *ph_conv_nTrk;
    std::vector<float>  *ph_conv_vtx_x;
    std::vector<float>  *ph_conv_vtx_y;
    std::vector<float>  *ph_conv_vtx_z;
    std::vector<float>  *ph_conv_ptin1;
    std::vector<float>  *ph_conv_ptin2;
    std::vector<float>  *ph_conv_ptout1;
    std::vector<float>  *ph_conv_ptout2;
    std::vector<Bool_t> *ph_passTight;
    std::vector<Bool_t> *ph_passMedium;
    std::vector<Bool_t> *ph_passLoose;
    std::vector<Bool_t> *ph_passLooseNoSIEIE;
    std::vector<Bool_t> *ph_passHOverELoose;
    std::vector<Bool_t> *ph_passHOverEMedium;
    std::vector<Bool_t> *ph_passHOverETight;
    std::vector<Bool_t> *ph_passSIEIELoose;
    std::vector<Bool_t> *ph_passSIEIEMedium;
    std::vector<Bool_t> *ph_passSIEIETight;
    std::vector<Bool_t> *ph_passChIsoCorrLoose;
    std::vector<Bool_t> *ph_passChIsoCorrMedium;
    std::vector<Bool_t> *ph_passChIsoCorrTight;
    std::vector<Bool_t> *ph_passNeuIsoCorrLoose;
    std::vector<Bool_t> *ph_passNeuIsoCorrMedium;
    std::vector<Bool_t> *ph_passNeuIsoCorrTight;
    std::vector<Bool_t> *ph_passPhoIsoCorrLoose;
    std::vector<Bool_t> *ph_passPhoIsoCorrMedium;
    std::vector<Bool_t> *ph_passPhoIsoCorrTight;
    std::vector<Bool_t> *ph_truthMatch_el;
    std::vector<Bool_t> *ph_truthMatch_ph;
    std::vector<Bool_t> *ph_truthMatch_jet;
    std::vector<float>  *ph_truthMinDR_el;
    std::vector<float>  *ph_truthMinDR_ph;
    std::vector<float>  *ph_truthMinDR_jet;
    std::vector<float>  *ph_truthMatchPt_el;
    std::vector<float>  *ph_truthMatchPt_ph;
    std::vector<float>  *ph_truthMatchPt_jet;
    std::vector<int>    *ph_truthMatchMotherPID_ph;
    std::vector<int>    *ph_truthMatchParentage_ph;
    std::vector<Bool_t> *ph_hasSLConv;
    std::vector<Bool_t> *ph_pass_mva_presel;
    std::vector<float>  *ph_mvascore;
    std::vector<Bool_t>  *ph_IsEB;
    std::vector<Bool_t>  *ph_IsEE;

    std::vector<float>  *jet_pt;
    std::vector<float>  *jet_eta;
    std::vector<float>  *jet_phi;
    std::vector<float>  *jet_e;

    std::vector<float>  *trueph_pt;
    std::vector<float>  *trueph_eta;
    std::vector<float>  *trueph_phi;
    std::vector<int>  *trueph_motherPID;
    std::vector<int>  *trueph_status;

    Float_t met_pt;
    Float_t met_phi;

    Bool_t passTrig_Photon26_Photon16_Mass60;
    Bool_t passTrig_Photon36_Photon22_Mass15;
    Bool_t passTrig_Photon42_Photon25_Mass15;
    Bool_t passTrig_DoublePhoton85          ;
    Bool_t passTrig_Photon22Iso             ;
    Bool_t passTrig_Photon22                ;
    Bool_t passTrig_Photon30Iso             ;
    Bool_t passTrig_Photon30                ;
    Bool_t passTrig_Photon36Iso             ;
    Bool_t passTrig_Photon36                ;
    Bool_t passTrig_Photon50Iso             ;
    Bool_t passTrig_Photon50                ;
    Bool_t passTrig_Photon75Iso             ;
    Bool_t passTrig_Photon75                ;
    Bool_t passTrig_Photon90Iso             ;
    Bool_t passTrig_Photon90                ;
    Bool_t passTrig_Photon120Iso            ;
    Bool_t passTrig_Photon120               ;
    Bool_t passTrig_Photon165HE             ;
    Bool_t passTrig_Photon165Iso            ;
    Bool_t passTrig_Photon175               ;
    Bool_t passTrig_Photon250               ;
    Bool_t passTrig_Photon300               ;
    Bool_t passTrig_Photon500               ;
    Bool_t passTrig_Photon600               ;
    Bool_t passTrig_Mu27_TkMu8              ;
    Bool_t passTrig_Mu17_Mu8_DZ             ;
    Bool_t passTrig_Mu17_TkMu8_DZ           ;
    Bool_t passTrig_Mu27_eta2p1             ;
    Bool_t passTrig_IsoMu27_eta2p1          ;
    Bool_t passTrig_IsoTkMu27_eta2p1        ;
    Bool_t passTrig_IsoMu17_eta2p1          ;
    Bool_t passTrig_IsoMu20_eta2p1          ;
    Bool_t passTrig_IsoMu24_eta2p1          ;
    Bool_t passTrig_IsoTkMu20_eta2p1        ;
    Bool_t passTrig_IsoTkMu24_eta2p1        ;
    Bool_t passTrig_TkMu24_eta2p1           ;
    Bool_t passTrig_Mu45_eta2p1           ;
    Bool_t passTrig_Ele27_WPLoose_eta2p1    ;
    Bool_t passTrig_Ele27_WPTight_eta2p1    ;
    Bool_t passTrig_Ele32_WPLoose_eta2p1    ;
    Bool_t passTrig_Ele32_WPTight_eta2p1    ;
    Bool_t passTrig_Ele17_Ele12_DZ          ;
    Bool_t passTrig_Ele17_Ele12             ;
    Bool_t passTrig_Mu8_Ele23               ;
    Bool_t passTrig_Mu8_Ele17               ;
    Bool_t passTrig_Mu23_Ele12              ;
    Bool_t passTrig_Mu17_Ele12              ;

    Float_t NLOWeight;
};

#endif
