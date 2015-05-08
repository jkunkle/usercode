#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H
#include "../../../Analysis/TreeFilter/Core/Core/AnalysisBase.h"
#include <string>
#include <vector>
#include "TTree.h"
#include "TChain.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TLorentzVector.h"
class RunModule : public virtual RunModuleBase {
    public :
        RunModule() {}
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & configs) ;
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( ) ;
        void Drawpt_leadph12_sieie_sublph12 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_0 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_1 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_2 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_3 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_4 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_5 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_6 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_7 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_8 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_9 ( ) const;
        void Drawpt_leadph12_sieie_sublph12_10 ( ) const;
        TH2F * hist_pt_leadph12_sieie_sublph12; 
        TH2F * hist_pt_leadph12_sieie_sublph12_0; 
        TH2F * hist_pt_leadph12_sieie_sublph12_1; 
        TH2F * hist_pt_leadph12_sieie_sublph12_2; 
        TH2F * hist_pt_leadph12_sieie_sublph12_3; 
        TH2F * hist_pt_leadph12_sieie_sublph12_4; 
        TH2F * hist_pt_leadph12_sieie_sublph12_5; 
        TH2F * hist_pt_leadph12_sieie_sublph12_6; 
        TH2F * hist_pt_leadph12_sieie_sublph12_7; 
        TH2F * hist_pt_leadph12_sieie_sublph12_8; 
        TH2F * hist_pt_leadph12_sieie_sublph12_9; 
        TH2F * hist_pt_leadph12_sieie_sublph12_10; 
            TFile * f;
 };
namespace OUT {
};
#endif
