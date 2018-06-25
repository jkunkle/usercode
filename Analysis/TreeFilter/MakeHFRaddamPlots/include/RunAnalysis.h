#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


#include "TH2.h"
#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"

class EtaPhiDepth {                                                                       
                                                                                          
    public :                                                                              
        EtaPhiDepth( int ieta, int iphi, int depth );

        bool operator==( const EtaPhiDepth &B ) const { return ( (ieta==B.ieta) && ( iphi==B.iphi) && ( depth==B.depth) ); }
        bool operator<(  const EtaPhiDepth &r  )const;
        
    public :                                                                              
        int ieta;                                                                         
        int iphi;                                                                         
        int depth;                                                                        
        
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


        void PlotHF     ( ModuleConfig & config ) ;

        int _evn;

        TH2F *calib_tdc_vs_evt;
        std::map<EtaPhiDepth, TH2F*> charge_ratio_ts1_ts2;
        std::map<EtaPhiDepth, TH2F*> charge_ratio_ts2_ts3;
        std::map<EtaPhiDepth, TH2F*> tdc_time_vs_evt;
        std::map<std::pair<int,int>, TH2F*> charge_ratio_ts2_ts3_sum;
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

};

#endif
