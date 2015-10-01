#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"
#include "include/BranchDefs.h"

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
        bool ApplyModule         ( ModuleConfig & config ) const;


        // Define modules below.
        // There is no restriction on the naming
        // return values, or inputs to these functions, but
        // you must of course handle them in the source file
        // Examples :
        void FilterPhoton     ( ModuleConfig & config ) const;
        void FilterMuon       ( ModuleConfig & config ) const;
        void FilterElectron   ( ModuleConfig & config ) const;
        void FilterJet        ( ModuleConfig & config ) const;
        bool FilterEvent      ( ModuleConfig & config ) const;
        bool FilterBlind      ( ModuleConfig & config ) const;
        void CalcEventVars    ( ModuleConfig & config ) const;
        void CalcDiJetVars    ( ModuleConfig & config ) const;

        bool _isData;

   private :

        float _m_w;
        bool get_wgamma_nu_pz( const TLorentzVector lepton, TLorentzVector &metlv ) const;
        bool calc_constrained_nu_momentum( const TLorentzVector lepton, const TLorentzVector met, float & result) const;
        bool solve_quadratic( float Aval, float Bval, float Cval, float &solution1, float &solution2) const;
                

};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    float zeppenfeld_w;
    bool zeppenfeld_w_pos_desc;
    float zeppenfeld_z;
    float dphi_wg_jj;
    float dphi_zg_jj;
    float deta_j_j;
    float m_j_j;
    float dr_j_j;
    float dphi_j1_met;
    float dphi_j2_met;
    float dr_ph_j1;
    float dr_ph_j2;
    float dr_lep_j1;
    float dr_lep_j2;

};

#endif
