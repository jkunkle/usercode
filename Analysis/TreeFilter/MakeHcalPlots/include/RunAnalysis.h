#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


#include "TH2.h"
#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"

class RunLsOrn {

    public :

        RunLsOrn(int, int, int);

        bool operator==( const RunLsOrn &B ) const { return ( (run==B.run) && (orn == B.orn ) ); }
        bool operator<( const RunLsOrn& B ) const;


    public :

        int run;
        int ls;
        int orn;
};


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
        void finalize( ) ;

        // The ApplyModule function calls any other module defined below
        // in src/RunModule.cxx.  This funciton is not strictly required
        // but its a consistent way to apply modules
        bool ApplyModule         ( ModuleConfig & config ) ;


        void PlotHBHE     ( ModuleConfig & config ) ;

        TH1F * avg_adc_HBHE;
        TH1F * avg_adc_HF;
        TH1F * laser_user_word;
        TH2F * avg_adc_HF_vs_umnqie1;
        TH2F * avg_adc_HF_vs_umnqie2;
        TH2F * avg_adc_umnqie1_vs_umnqie2;
        TH2F * avg_adc_HBHE_vs_umnqie1;
        TH2F * avg_adc_HBHE_vs_umnqie2;
        TH2F * adc_umnqie1_vs_umnqie2_laserHF;
        TH2F * adc_umnqie1_vs_umnqie2_laserHBHE;
        TH2F * adc_depth_highadc;
        TH2F * adc_depth_bxadc;
        TH2F * adc_depth;
        TH1F * adc_HBHE;
        TH1F * adc_HF;
        TH1F * adc_umnqie1;
        TH1F * adc_umnqie2;
        TH1F * totdiff_HF;
        TH1F * totdiff_HBHE;

        TH1F * bx_HBHE_highadc;
        TH1F * bx_HF_highadc;

        TH1F * n_fires_orn_hf;
        TH1F * n_fires_orn_hbhe;

        TFile * _outfile;

        int _evn;

        std::map<std::pair<int, int>, TH1F > ch_bxadc_map;
        std::map<std::pair<int, int>, TH1F > ch_adc_map;
        std::map<std::pair<int, int>, TH1F > ch_highadc_map;

        std::vector<TH2F> adc_depth_highadc_outbx_list;
        std::vector<TH2F> umnqie_highadc_outbx_list;

        std::map<int, TH1F> orn_ls_run296609_HBHE;
        std::map<int, TH1F> orn_ls_run296609_HF;

        std::vector<std::pair<unsigned,unsigned> > match_list_hf;
        std::vector<std::pair<unsigned,unsigned> > match_list_hbhe;

        std::map<std::pair<unsigned,unsigned>, TH1F> runorn_bx_hists_hf;
        std::map<std::pair<unsigned,unsigned>, TH1F> runorn_bx_hists_hbhe;

        unsigned _lastLS;
        int _lastORN;
        int _lastBX;
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

};

#endif
