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

// Ouput namespace 
// Declare any output variables that you'll fill here
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

    //Float_t             leadLep_photDR;
    //Float_t             sublLep_photDR;

    Float_t             leadLep_leadPhotDR;
    Float_t             sublLep_leadPhotDR;
    Float_t             leadLep_sublPhotDR;
    Float_t             sublLep_sublPhotDR;
    Float_t             phot_minLepDR;
    Float_t             photPhot_lepDPhi;
    Float_t             phot_photDPhi;
    Float_t             photPhot_lepDR;
    Float_t             phot_photDR;

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
    Float_t             m_leplepph;

};

#endif
