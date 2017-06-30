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
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & config) ;
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( ) {};

        // The ApplyModule function calls any other module defined below
        // in src/RunModule.cxx.  This funciton is not strictly required
        // but its a consistent way to apply modules
        bool ApplyModule         ( ModuleConfig & config ) ;


        // Define modules below.
        // There is no restriction on the naming
        // return values, or inputs to these functions, but
        // you must of course handle them in the source file
        // Examples :
        void FilterMuon         ( ModuleConfig & config );
        void FilterElectron     ( ModuleConfig & config );
        void FilterPhoton       ( ModuleConfig & config );
        void FilterJet          ( ModuleConfig & config ) const;
        bool FilterEvent        ( ModuleConfig & config ) const;
        bool FilterBlind        ( ModuleConfig & config ) const;
        void BuildEventVars     ( ModuleConfig & config ) const;


        bool get_constriained_nu_pz( const TLorentzVector lepton, TLorentzVector & metlv ) const ;
        bool calc_constrained_nu_momentum( const TLorentzVector lepton, const TLorentzVector metlv, float &result ) const ;
        bool solve_quadratic( float Aval, float Bval, float Cval, float & solution1, float &solution2 ) const; 


    private :
        float _m_w;
        bool _isData;
        std::vector<TLorentzVector> _selectedMuons;
        std::vector<TLorentzVector> _selectedElectrons;
        std::vector<TLorentzVector> _selectedPhotons;


};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    Float_t m_lep_ph;
    Float_t m_lep_met_ph;
    Float_t m_mt_lep_met_ph;
    Float_t m_mt_lep_met_ph_forcewmass;
    Float_t mt_w;
    Float_t mt_res;
    Float_t mt_lep_ph;
    Float_t dphi_lep_ph;
    Float_t dr_lep_ph;
    Float_t m_lep_met;
    Float_t mt_lep_met;
    Float_t pt_lep_met;
    Float_t dphi_lep_met;
    Float_t mt_lep_met_ph;
    Float_t mt_lep_met_ph_inv;
    Float_t RecoWMass;
    Float_t recoM_lep_nu_ph;
    Float_t recoMet_eta;
    Float_t recoW_pt;
    Float_t recoW_eta;
    Float_t recoW_phi;
    Float_t m_ll;
    Bool_t nu_z_solution_success;
    Bool_t isBlinded;

    Float_t leadjet_pt;
    Float_t subljet_pt;
    Float_t leaddijet_m;
    Float_t leaddijet_pt;
    Float_t massdijet_m;
    Float_t massdijet_pt;
 

};

#endif
