#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"

class RunModule : public virtual RunModuleBase {

    public :

        RunModule() {}

        void Run( TChain * chain, TTree *outtree, std::vector<ModuleConfig> & config, const CmdOptions & options, int minevt=0, int maxevt=0) const;

        bool ApplyModule      ( ModuleConfig & config ) const;
        void BuildLepton      ( ModuleConfig & config ) const;
        //void BuildMuon      ( ModuleConfig & config ) const;
        void BuildPhoton      ( ModuleConfig & config ) const;
        void BuildNeutrino    ( ModuleConfig & config ) const;
        void BuildWboson      ( ModuleConfig & config ) const;
        void BuildEvent       ( ModuleConfig & config ) const;
        bool FilterElec       ( ModuleConfig & config ) const;
        bool FilterMuon       ( ModuleConfig & config ) const;
        bool FilterEvent      ( ModuleConfig & config ) const;
        bool FilterTauEvent   ( ModuleConfig & config ) const;
        bool FilterBasicEvent ( ModuleConfig & config ) const;

};

namespace OUT {

    Int_t              lep_n;
    Int_t              phot_n;
    Int_t              nu_n;
    Int_t              w_n;

    std::vector<float>  *lep_pt;
    std::vector<float>  *lep_eta;
    std::vector<float>  *lep_phi;
    std::vector<float>  *lep_e;
    std::vector<int>    *lep_motherPID;
    std::vector<Bool_t> *lep_isElec;
    std::vector<Bool_t> *lep_isMuon;
    std::vector<Bool_t> *lep_isPos;

    std::vector<float>  *phot_pt;
    std::vector<float>  *phot_eta;
    std::vector<float>  *phot_phi;
    std::vector<float>  *phot_e;
    std::vector<int>    *phot_motherPID;

    std::vector<float>  *nu_pt;
    std::vector<float>  *nu_eta;
    std::vector<float>  *nu_phi;
    std::vector<float>  *nu_e;
    std::vector<int>    *nu_motherPID;

    std::vector<float>  *w_pt;
    std::vector<float>  *w_eta;
    std::vector<float>  *w_phi;
    std::vector<float>  *w_e;
    std::vector<Bool_t>  *w_isPos;

    Float_t             leadPhot_pt;
    Float_t             sublPhot_pt;

    Float_t             leadPhot_lepDR;
    Float_t             sublPhot_lepDR;
    Float_t             phot_photDR;
    Float_t             photPhot_lepDR;
    Float_t             leadPhot_lepDPhi;
    Float_t             sublPhot_lepDPhi;
    Float_t             phot_photDPhi;
    Float_t             photPhot_lepDPhi;

    Float_t             mt_lepnu;
    Float_t             mt_lepphot1nu;
    Float_t             mt_lepphot2nu;
    Float_t             mt_lepphotphotnu;

    Float_t             m_lepnu;
    Float_t             m_leplep;
    Float_t             m_lepphot1nu;
    Float_t             m_lepphot2nu;
    Float_t             m_lepphotphotnu;
    Float_t             m_lepphot1;
    Float_t             m_lepphot2;
    Float_t             m_lepphotphot;
    Float_t             m_photphot;

};

#endif
