#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TRandom3.h"
#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"

class MuScleFitCorrector;
class EnergyScaleCorrection_class;

// The RunModule inherits from RunModuleBase (an Abstract Base Class )
// defined in the Core package so that all
// RunModules present a common interface in a Run function
// This allows the code defined in this package
// to be run from the Core package to minimize
// code duplication in each module

struct correctionValues
{
    int nRunMin;
    int nRunMax;
    double corrCat0;
    double corrCat1;
    double corrCat2;
    double corrCat3;
    double corrCat4;
    double corrCat5;
    double corrCat6;
    double corrCat7;
};

struct linearityCorrectionValues
{
    double ptMin;
    double ptMax;
    double corrCat0;
    double corrCat1;
    double corrCat2;
    double corrCat3;
    double corrCat4;
    double corrCat5;
};

class RunModule : public virtual RunModuleBase {

    public :

        RunModule();

        // The run function must exist and be defined exactly as this
        // because it is defined in RunModuleBase 
        // in src/RunModule.cxx all the analysis is defind in this RunModule function
        void initialize(TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & configs);
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( ) ;

        // The ApplyModule function calls any other module defined below
        // in src/RunModule.cxx.  This funciton is not strictly required
        // but its a consistent way to apply modules
        bool ApplyModule         ( ModuleConfig & config ) ;


        // Define modules below.
        // There is no restriction on the naming
        // return values, or inputs to these functions, but
        // you must of course handle them in the source file
        // Examples :
        void BuildElectron       ( ModuleConfig & config ) ;
        void BuildMediumElectron ( ModuleConfig & config ) const;
        void BuildMuon           ( ModuleConfig & config ) const;
        void BuildPhoton         ( ModuleConfig & config ) const;
        void BuildJet            ( ModuleConfig & config ) const;
        void BuildEvent          ( ModuleConfig & config ) const;
        void BuildTriggerBits    ( ModuleConfig & config ) const;
        void WeightEvent         ( ModuleConfig & config ) const;
        bool FilterElec          ( ModuleConfig & config ) const;
        bool FilterMuon          ( ModuleConfig & config ) const;
        bool FilterEvent         ( ModuleConfig & config ) const;
        bool FilterTrigger       ( ModuleConfig & config ) const;

        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR ) const;
        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR ) const;
        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR, TLorentzVector &matchLV ) const;
        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR, TLorentzVector &matchLV, int &matchMotherPID ) const;
        void calc_corr_iso( float chIso, float phoIso, float neuIso, float rho, float eta, float &chisoCorr, float &phoIsoCorr, float &neuIsoCorr ) const;
        float get_ph_el_mindr( const TLorentzVector &jetlv ) const;
        float get_jet_el_mindr( const TLorentzVector &jetlv ) const;
        float get_jet_ph_mindr( const TLorentzVector &jetlv ) const;

        float GetElectronMomentumCorrection( float pt, float sceta, float eta, float r9, bool isData, int runNumber) ;
        void extractElectronCorrections( const std::string & filename );
        void extractElectronLinCorrections( const std::string & filename );

     private :

        bool eval_el_tight      ;
        bool eval_el_medium     ;
        bool eval_el_loose      ;
        bool eval_el_veryloose  ;
        bool eval_el_tightTrig  ;
        bool eval_el_mva_trig   ;
        bool eval_el_mva_nontrig;

        bool eval_ph_tight    ;
        bool eval_ph_medium   ;
        bool eval_ph_loose    ;

        bool apply_electron_corrections;
        std::string ele_correction_path;
        std::string ele_smearing_path;


        // Old
        std::vector<correctionValues> electron_corr_vals;
        std::vector<linearityCorrectionValues> electron_lincorr_vals;



        bool apply_muon_corrections;
        std::string muon_correction_path;

        bool apply_photon_corrections;
        std::string pho_correction_path;
        std::string pho_smearing_path;

        bool apply_jet_corrections;

        // tmva files for photon mva
        TMVA::Reader *TMVAReaderEB;
        TMVA::Reader *TMVAReaderEE;


        TRandom3 _rand;
        MuScleFitCorrector * muCorr;
        EnergyScaleCorrection_class * eleCorr;

        TFile *puweight_sample_file;
        TFile *puweight_data_file;
        TH1F *puweight_sample_hist;
        TH1D *puweight_data_hist;


};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    Int_t              el_n;
    Int_t              mu_n;
    Int_t              ph_n;
    Int_t              jet_n;
    Int_t              vtx_n;

    std::vector<float>  *el_pt;
    std::vector<float>  *el_eta;
    std::vector<float>  *el_sceta;
    std::vector<float>  *el_phi;
    std::vector<float>  *el_e;
    std::vector<float>  *el_pt_uncorr;
    std::vector<float>  *el_e_uncorr;
    std::vector<float>  *el_mva_trig;
    std::vector<float>  *el_mva_nontrig;
    std::vector<float>  *el_d0pv;
    std::vector<float>  *el_z0pv;
    std::vector<float>  *el_sigmaIEIE;
    std::vector<float>  *el_pfiso30;
    std::vector<float>  *el_pfiso40;
    std::vector<Bool_t> *el_triggerMatch;
    std::vector<Bool_t> *el_hasMatchedConv;
    std::vector<Bool_t> *el_passTight;
    std::vector<Bool_t> *el_passMedium;
    std::vector<Bool_t> *el_passLoose;
    std::vector<Bool_t> *el_passVeryLoose;
    std::vector<Bool_t> *el_passTightTrig;
    std::vector<Bool_t> *el_passMvaNonTrig;
    std::vector<Bool_t> *el_passMvaTrig;
    std::vector<Bool_t> *el_truthMatch_el;
    std::vector<float>  *el_truthMatchPt_el;
    std::vector<float>  *el_truthMinDR_el;

    std::vector<float>  *mu_pt;
    std::vector<float>  *mu_eta;
    std::vector<float>  *mu_phi;
    std::vector<float>  *mu_e;
    std::vector<float>  *mu_pt_uncorr;
    std::vector<float>  *mu_eta_uncorr;
    std::vector<float>  *mu_phi_uncorr;
    std::vector<float>  *mu_e_uncorr;
    std::vector<float>  *mu_pfIso_ch;
    std::vector<float>  *mu_pfIso_nh;
    std::vector<float>  *mu_pfIso_pho;
    std::vector<float>  *mu_pfIso_pu;
    std::vector<float>  *mu_corrIso;
    std::vector<Bool_t> *mu_triggerMatch;
    std::vector<Bool_t> *mu_truthMatch;
    std::vector<float>  *mu_truthMinDR;

    std::vector<float>  *ph_pt;
    std::vector<float>  *ph_eta;
    std::vector<float>  *ph_sceta;
    std::vector<float>  *ph_phi;
    std::vector<float>  *ph_e;
    std::vector<float>  *ph_pt_uncorr;
    std::vector<float>  *ph_HoverE;
    std::vector<float>  *ph_HoverE12;
    std::vector<float>  *ph_sigmaIEIE;
    std::vector<float>  *ph_sigmaIEIP;
    std::vector<float>  *ph_r9;
    std::vector<float>  *ph_E1x3;
    std::vector<float>  *ph_E2x2;
    std::vector<float>  *ph_E5x5;
    std::vector<float>  *ph_E2x5Max;
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
    std::vector<float>  *ph_SCRChIso;
    std::vector<float>  *ph_SCRPhoIso;
    std::vector<float>  *ph_SCRNeuIso;
    std::vector<float>  *ph_SCRChIso04;
    std::vector<float>  *ph_SCRPhoIso04;
    std::vector<float>  *ph_SCRNeuIso04;
    std::vector<float>  *ph_RandConeChIso;
    std::vector<float>  *ph_RandConePhoIso;
    std::vector<float>  *ph_RandConeNeuIso;
    std::vector<float>  *ph_RandConeChIso04;
    std::vector<float>  *ph_RandConePhoIso04;
    std::vector<float>  *ph_RandConeNeuIso04;

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
    std::vector<float>  *ph_truthMinDR_el;
    std::vector<float>  *ph_truthMinDR_ph;
    std::vector<float>  *ph_truthMatchPt_el;
    std::vector<float>  *ph_truthMatchPt_ph;
    std::vector<int>    *ph_truthMatchMotherPID_ph;
    std::vector<Bool_t> *ph_hasSLConv;
    std::vector<Bool_t> *ph_pass_mva_presel;
    std::vector<float>  *ph_mvascore;
    std::vector<Bool_t>  *ph_IsEB;
    std::vector<Bool_t>  *ph_IsEE;

    std::vector<float>  *jet_pt;
    std::vector<float>  *jet_eta;
    std::vector<float>  *jet_phi;
    std::vector<float>  *jet_e;

    Bool_t              passTrig_ele27WP80;
    Bool_t              passTrig_mu24eta2p1;
    Bool_t              passTrig_mu24;


    Float_t             avgPU; 
    Float_t             PUWeight;
};

namespace MVAVars {

    // EB
    float phoPhi;
    float phoR9;
    float phoSigmaIEtaIEta;
    float phoSigmaIEtaIPhi;
    float s13;
    float s4ratio;
    float s25;
    float phoSCEta;
    float phoSCRawE;
    float phoSCEtaWidth;
    float phoSCPhiWidth;
    float rho2012;
    float phoPFPhoIso;
    float phoPFChIso;
    float phoPFChIsoWorst;
    float phoEt;
    float phoEta;

    // Additional EE
    float phoESEnToRawE;
    float phoESEffSigmaRR;

};
#endif
